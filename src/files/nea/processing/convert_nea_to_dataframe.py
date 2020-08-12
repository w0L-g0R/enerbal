import pandas as pd
from pathlib import Path
from typing import Union, List

import numpy as np
import pickle

# from settings import provinces

from files.nea.processing.get_nea_sheets import (
    sectors,
    energy_usage_types,
    energy_sources_93_98,
    energy_sources_99_plus,
    energy_sources_nea_df,
    energy_sources_nea_df_reindex,
)

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice


def create_nea_col_midx(
    last_year: int, sectors: List, energy_usage_types: List,
) -> pd.MultiIndex:

    provinces = [
        "Bgd",
        "Ktn",
        "Noe",
        "Ooe",
        "Sbg",
        "Stk",
        "Tir",
        "Vbg",
        "Wie",
        "AT",
    ]

    years = [x for x in range(1993, last_year + 1, 1)]

    midx = pd.MultiIndex.from_product(
        [provinces, sectors, energy_usage_types, years],
        names=["BL", "SECTOR", "USAGE", "YEAR"],
    )

    return midx


def convert_nea_to_df(
    balances_directory_path: Union[str, Path],
    sectors: List,
    energy_usage_types: List,
    energy_sources: List,
    last_year: int,
):

    # //////////////////////////////////////////////////// CREATE MULTI INDEX

    nea_col_midx = create_nea_col_midx(
        last_year=last_year, sectors=sectors, energy_usage_types=energy_usage_types
    )
    # ////////////////////////////////////////////////////// CREATE STORAGE DFS

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    nea_df = pd.DataFrame(index=energy_sources[">=1999"], columns=nea_col_midx)

    # ////////////////////////////////////// COLLECT ENERGY BALANCES FILE PATHS

    # Array to store energy balance file paths as pathlib objects
    nea_file_paths = []

    for _path in balances_directory_path.glob("*.xlsx"):
        nea_file_paths.append(str(Path(_path)))

    for province in provinces:

        f"//////////////////////////  {province}  /////////////////////////"

        # ////////////////////////////////////////////////////// FIND PATH

        try:
            # Find corresponding excel file for province
            balances_file_path = list(
                filter(lambda x: province in x, nea_file_paths)
            )[0]

        # CHECK 1: Xlxs file not found or not existing
        except Exception as e:
            raise e

        # //////////////////////////////////////////////////// FETCH_SHEETS

        # Extract all sheets (=energieträger) from file at once and save them
        # to a dictionary
        sheets = pd.read_excel(
            io=str(balances_file_path), sheet_name=None, na_filter=False, usecols="A:I",
        )

        # Delete unnecessary sheets
        del sheets["Deckblatt"]

        try:
            del sheets["Check"]
        except BaseException:
            pass

        # Iter over balance file sheets
        for nea_year in sheets:

            print("\nYEAR: ", nea_year)

            # Header number with first sector information
            starting_row = 3

            # Convert sheet year information to integer
            year = int("".join(c for c in nea_year if c.isdigit()))

            # Add leading digits to year if missing
            if len(str(year)) == 2:
                year = int("".join(["19", str(year)]))

            # Iter over sectors
            for sector in sectors:

                # Check sector information on sheet
                _sector = sheets[nea_year].iloc[starting_row, 0]

                print("_sector: ", _sector)

                # Extract sector data from sheet
                sector_data = sheets[nea_year].iloc[
                    starting_row + 2: starting_row + 24, :
                ]

                # Set first col as index
                sector_data.set_index(sector_data.iloc[:, 0], inplace=True)

                # Convert all to numeric and round
                sector_data = (
                    sector_data.iloc[:, 1:]
                    .apply(pd.to_numeric, errors="coerce")
                    .round(2)
                )

                # Assign columns
                sector_data.columns = energy_usage_types

                # Extract index
                sources_index = energy_sources[">=1999"]

                # Replace index if year < 1999
                if year < 1999:
                    sector_data.index = pd.Index(energy_sources["<1999"])
                    sources_index = energy_sources["<1999"]
                else:
                    # Set to nan (gets overwritten with "Braunkohlebriketts"
                    # for df data greater than 1999)
                    sector_data.loc["Sonstige ET", :] = np.nan

                # Iter over usage types
                for enum, usage_type in enumerate(energy_usage_types):

                    # Assign values
                    _usage_type = sheets[nea_year].iloc[starting_row, enum + 1]
                    nea_df.loc[
                        IDX[sources_index], IDX[province,
                                                sector, usage_type, year]
                    ] = sector_data[usage_type]

                # Increase counter variable
                starting_row += 26

    # Replace "Sonstige ET" with "Braunkohlebriketts"
    nea_df.index = pd.Index(energy_sources["nea_df"])

    # Apply different order of energy sources in final df
    nea_df = nea_df.reindex(pd.Index(energy_sources_nea_df_reindex), axis=0)

    pickle.dump(nea_df, open("nea_df.p", "wb"))

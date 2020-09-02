import datetime
import logging
import pickle
from pathlib import Path
from typing import List, Union

import numpy as np
import pandas as pd

from enspect.aggregates.common import provinces
from enspect.aggregates.nea import *
from enspect.conversion.nea.utils import (
    create_nea_col_midx,
    fetch_from_xlsx,
    write_to_log_file,
)
from enspect.paths import file_paths
from enspect.utils import timeit

IDX = pd.IndexSlice


@timeit
def convert_nea_to_dataframe(
    last_year: int,
):

    # //////////////////////////////////////////////////// CREATE MULTI INDEX

    nea_col_midx = create_nea_col_midx(
        last_year=last_year,
        sectors=nea_data_structures["sectors"],
        energy_usage_types=nea_data_structures["energy_usage_types"],
    )
    # ////////////////////////////////////////////////////// CREATE STORAGE DFS

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    nea_df = pd.DataFrame(
        index=nea_data_structures["energy_sources_99_plus"], columns=nea_col_midx
    )
    # ////////////////////////////////////// COLLECT ENERGY BALANCES FILE PATHS

    # Array to store energy balance file paths as pathlib objects
    files = list(file_paths["files_nea"].glob("*.xlsx"))

    write_to_log_file(
        log_file=file_paths["conversion_logs"] / "nutzenergieanalyse.log",
        files=files,
    )

    for file in files:

        # nea_file_paths.append(str(Path(_path)))

        filename = Path(file).stem

        province = filename.split("_")[1]

        # files.remove(file)

        if province in provinces:

            # ////////////////////////////////////////////////////////// FETCH
            logging.getLogger().warning(
                "{}\n\n{} Province: {} - File: {}\n\n{}".format(
                    "/" * 79, "\t" * 4, province, filename, "/" * 79
                )
            )

            sheets = fetch_from_xlsx(file=file)

            # Iter over balance file sheets
            for nea_year in sheets:

                logging.getLogger().warning(
                    "{}\n\n{}Year: {}\n{}\n".format(
                        "_" * 79, "\t" * 4, nea_year, "_" * 79
                    )
                )

                # Header number with first sector information
                starting_row = 3

                # Convert sheet year information to integer
                year = int("".join(c for c in nea_year if c.isdigit()))

                # Add leading digits to year if missing
                if len(str(year)) == 2:
                    year = int("".join(["19", str(year)]))

                # Iter over sectors
                for sector in nea_data_structures["sectors"]:

                    # Check sector information on sheet
                    _sector = sheets[nea_year].iloc[starting_row, 0]

                    logging.getLogger().warning(
                        "{}{}-Sector: {}".format(
                            "\t" * 4,
                            province,
                            sector,
                        )
                    )

                    # Extract sector data from sheet
                    sector_data = sheets[nea_year].iloc[
                        starting_row + 2 : starting_row + 24, :
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
                    sector_data.columns = nea_data_structures["energy_usage_types"]

                    # Extract index
                    sources_index = nea_data_structures["energy_sources_99_plus"]

                    # Replace index if year < 1999
                    if year < 1999:
                        sector_data.index = pd.Index(
                            nea_data_structures["energy_sources_93_98"]
                        )
                        sources_index = nea_data_structures["energy_sources_93_98"]
                    else:
                        # Set to nan (gets overwritten with "Braunkohlebriketts"
                        # for df data greater than 1999)
                        sector_data.loc["Sonstige ET", :] = np.nan

                    # Iter over usage types
                    for enum, usage_type in enumerate(
                        nea_data_structures["energy_usage_types"]
                    ):

                        # Assign values
                        _usage_type = sheets[nea_year].iloc[starting_row, enum + 1]
                        nea_df.loc[
                            IDX[sources_index], IDX[province, sector, usage_type, year]
                        ] = sector_data[usage_type]

                    # Increase counter variable
                    starting_row += 26

    # Replace "Sonstige ET" with "Braunkohlebriketts"
    nea_df.index = pd.Index(nea_data_structures["energy_sources_nea_df"])

    # Apply different order of energy sources in final df
    nea_df = nea_df.reindex(
        pd.Index(nea_data_structures["energy_sources_nea_df_reindex"]), axis=0
    )
    # Assign index name
    nea_df.index.name = "ES"

    # Rearrange column and row indices (new row idx == SECTOR)
    nea_df = nea_df.unstack(level="ES")

    # New Column_midx
    nea_df = nea_df.unstack(level=["PROV", "ES", "UC", "YEAR"])

    # Remove existing file if exists
    pickle_file = file_paths["db_pickles"] / Path("nea.p")

    if pickle_file.exists():

        pickle_file.unlink()

        logging.getLogger().warning(
            "\n{}\n\n{} Removed existing file \n\n{}".format(
                "/" * 79, "\t" * 6, "/" * 79
            )
        )

    with open(pickle_file, "wb") as file:
        pickle.dump(nea_df, file)

    logging.getLogger().warning(
        "\n{}\n\n{} Finished NEA file conversion \n\n{}".format(
            "/" * 79, "\t" * 6, "/" * 79
        )
    )

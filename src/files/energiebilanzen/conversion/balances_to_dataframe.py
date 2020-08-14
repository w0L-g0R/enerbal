from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np
import time

from files.energiebilanzen.conversion.eb_data_structures import eb_sheets

from files.energiebilanzen.conversion.utils import (
    get_indices
)
#     # create_eev_col_midx,
#     # create_renewables_col_midx,
# )
# from files.energiebilanzen.convert.create_dfs import (
#     create_eb_storage_dfs,
#     create_idx_check_dfs,
# )
# from files.energiebilanzen.convert.assign_table_data import (
#     assign_eev_table,
#     assign_renewables_table,
#     # assign_sectors_consumption_table,
#     # assign_sector_energy_consumption_table,
# )

from files.energiebilanzen.convert.fetch_from_excel import fetch_energy_sources

from paths import file_paths

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice

# //////////////////////////////////////////////////////////// CONVERT_EB_TO_DF


def eb_to_df(
    # balances_directory_path: Union[str, Path],
    # row_indices_file_path: Union[str, Path],
    last_year: int,
):
    # Don't use the settings variable here
    provinces = [
        # "Bgd",
        # "Ktn",
        # "Noe",
        # "Ooe",
        # "Sbg",
        # "Stk",
        # "Tir",
        # "Vbg",
        # "Wie",
        "AT",
    ]

    # ///////////////////////////////////////////////////////////// GET INDICES
    eb_row_midx, \
    res_row_midx, \
    eb_col_midx,\
    res_col_midx = get_indices(
        provinces=provinces,
        last_year=last_year
    )

    # ////////////////////////////////////////////////////// CREATE STORAGE DFS

    (
        eb_df,
        res_df,
        # sectors_df,
        # sector_energy_df,
        ) = create_eb_storage_dfs(
        eb_col_midx=eb_col_midx,
        res_col_midx=res_col_midx,
        row_indices=row_indices,
        )

    # ////////////////////////////////////// COLLECT ENERGY BALANCES FILE PATHS

    # Array to store energy balance file paths as pathlib objects
    eb_file_paths = []

    for _path in balances_directory_path.glob("*.xlsx"):
            eb_file_paths.append(str(Path(_path)))

        for province in provinces:

            print(
                "//////////////////////////  {}  /////////////////////////".format(
                    province)
            )

            # /////////////////////////////////////////////////////////// FIND PATH
            try:
                # Find corresponding excel file for province
                balances_file_path=list(
                    filter(
                        lambda x: province in x,
                        eb_file_paths))[0]

            # CHECK 1: Xlxs file not found or not existing
            except Exception as e:
                raise e

            # ////////////////////////////////////////////////////////// FETCH DATA
            years_range_data=pd.Series(data=eev_df.columns.unique(level="YEAR")).astype(
                "object"
            )

            dfs, renewables_sheet=fetch_energy_sources(
                balances_file_path=balances_file_path,
                eb_sheets=eb_sheets,
                years_range_data=years_range_data,
            )

            # //////////////////////////////////////////////////////////// CHECK DF

            (
                eev_idx_check_df,
                renewables_idx_check_df,
                sector_idx_check_df,
                sector_energy_idx_check_df,
            )=create_idx_check_dfs(row_indices=row_indices)

            if province != "AT":

                # ////////////////////////////////////////////////////// RENEWABLES
                assign_renewables_table(
                    renewables_df=renewables_df,
                    renewables_sheet=renewables_sheet,
                    row_indices=row_indices,
                    province=province,
                    renewables_idx_check_df=renewables_idx_check_df,
                    years_range_data=years_range_data,
                )

            # for energy_source in ["Steinkohle"]:
            for energy_source in dfs:
                print("\nenergy_source: ", energy_source)

                # ///////////////////////////////////////////////////////////// EEV
                assign_eev_table(
                    eev_df=eev_df,
                    dfs=dfs,
                    row_indices=row_indices,
                    province=province,
                    energy_source=energy_source,
                    eev_idx_check_df=eev_idx_check_df,
                    years_range_data=years_range_data,
                )

                # ///////////////////////////////////////////// SECTORS CONSUMPTION
                assign_sectors_consumption_table(
                    sectors_df=sectors_df,
                    dfs=dfs,
                    province=province,
                    energy_source=energy_source,
                    sector_idx_check_df=sector_idx_check_df,
                    years_range_data=years_range_data,
                )

                # /////////////////////////////////////// SECTOR ENERGY CONSUMPTION
                assign_sector_energy_consumption_table(
                    sector_energy_df=sector_energy_df,
                    dfs=dfs,
                    province=province,
                    energy_source=energy_source,
                    sector_energy_idx_check_df=sector_energy_idx_check_df,
                    years_range_data=years_range_data,
                )

            # ////////////////////////////////////////////////////////////// CHECKS

            renewables_idx_check_df.to_excel(
                balances_directory_path.parent
                / "checks"
                / "_".join([province, "renewables_idx_check_df.xlsx"])
            )

            eev_idx_check_df.to_excel(
                balances_directory_path.parent
                / Path("checks")
                / "_".join([province, "eev_idx_check_df.xlsx"])
            )

            sector_idx_check_df.to_excel(
                balances_directory_path.parent
                / "checks"
                / "_".join([province, "sector_idx_check_df.xlsx"])
            )

            sector_energy_idx_check_df.to_excel(
                balances_directory_path.parent
                / "checks"
                / "_".join([province, "sector_energy_idx_check_df.xlsx"])
            )

        # //////////////////////////////////////////////////// ADD MIDX ROW INDICES

        eev_df.set_index(eev_row_midx, inplace=True)
        eev_df.sort_index(inplace=True, axis="columns")

        renewables_df.set_index(renewables_row_midx, inplace=True)
        renewables_df.sort_index(inplace=True, axis="columns")

        # ////////////////////////////////////////////////////////////////// PICKLE

        pickle.dump(
            eev_df, open(balances_directory_path.parent /
                        Path("pickles/eev_df.p"), "wb")
        )

        pickle.dump(
            sectors_df,
            open(
                balances_directory_path.parent /
                Path("pickles/sectors_df.p"),
                "wb",
            ),
        )

        pickle.dump(
            sector_energy_df,
            open(
                balances_directory_path.parent
                / Path("pickles/sector_energy_df.p"),
                "wb",
            ),
        )

        pickle.dump(
            renewables_df,
            open(balances_directory_path.parent /
                Path("pickles/renewables_df.p"), "wb"),
        )

        return

import logging
from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np
from utils import timeit

from converter.energiebilanzen.data_structures import eb_sheet_names

from converter.energiebilanzen.utils import (
    create_indices,
    create_index_template,
    fetch_from_xlsx,
    get_sectors_data,
    add_missing_row_indices,
    preprocess_res_sheet,
    copy_eb_data,
    copy_res_data,
    write_to_log_file,
)

from converter.energiebilanzen.check_errors import check_index_errors
from paths import file_paths


IDX = pd.IndexSlice

# //////////////////////////////////////////////////////////// CONVERT_EB_TO_DF


@timeit
def convert_energy_balances_to_dataframe(
    # balances_directory_path: Union[str, Path],
    # row_indices_file_path: Union[str, Path],
    last_year: int,
):

    """
    Make sure energy balance files follow the name convention: prefix "EB" + provinces_name + year_start(last two digits only) + year_end(last two digits only) , connected with underlines, eg. EB_Bgd_88_18
    """
    provinces = [
        "Bgd",
        # "Ktn",
        # "Noe",
        # "Ooe",
        # "Sbg",
        # "Stk",
        # "Tir",
        # "Vbg",
        # "Wie",
        # "AT",
    ]

    years = [year for year in range(1988, last_year + 1, 1)]

    # ///////////////////////////////////////////////////////////// GET INDICES

    # ___________________________________________________________ MULTI INDICES
    (
        eb_row_midx,
        res_row_midx,
        eb_col_midx,
        res_col_midx,
        res_conversion_factors,
    ) = create_indices(provinces=provinces, last_year=last_year)

    # ________________________________________________ TEMPLATES (SINGLE INDEX)

    eb_idx_template = create_index_template(midx=eb_row_midx, data_type="eb")
    res_idx_template = create_index_template(midx=res_row_midx, data_type="res")

    # ////////////////////////////////////////////////////// CREATE STORAGE DFS

    # df's to be pickled finally
    eb_df = pd.DataFrame(index=eb_row_midx, columns=eb_col_midx)
    res_df = pd.DataFrame(index=res_row_midx, columns=res_col_midx)

    # ////////////////////////////////////// COLLECT ENERGY BALANCES FILE PATHS
    files = file_paths["files_eb"].glob("*.xlsx")

    # ///////////////////////////////////// COPY VALUES FROM EXCEL TO LOCAL DFS

    # Search for balance files @ EB file folder
    for file in file_paths["files_eb"].glob("*.xlsx"):

        filename = Path(file).stem

        # Filter for actual balances files
        if filename.startswith("EB"):

            file = str(Path(file))

            province = filename.split("_")[1]

        # Only unpack values for selected provinces
        if province in provinces:

            write_to_log_file(
                log_file=province, files=files, filename=filename,
            )

            eb_sheets, res_sheet = fetch_from_xlsx(file=file, years=years)

            # d = {"eb": eb_sheets, "res": res_sheet}
            # pickle.dump(d, open("AT_sheets.pkl", "wb"))

            # d = pickle.load(open("AT_sheets.pkl", "rb"))

            # eb_sheets, res_sheet = d.values()

            eb_df = copy_eb_data(
                province=province,
                eb_df=eb_df,
                eb_sheets=eb_sheets,
                eb_idx_template=eb_idx_template,
                eb_row_midx=eb_row_midx,
            )

            if province != "AT":

                preprocess_res_sheet(
                    res_sheet=res_sheet, res_conversion_factors=res_conversion_factors,
                )

                res_df = copy_res_data(
                    province=province,
                    res_df=res_df,
                    res_sheet=res_sheet,
                    res_idx_template=res_idx_template,
                    res_row_midx=res_row_midx,
                    res_col_midx=res_col_midx,
                )
    else:
        logging.getLogger().debug("\n=> No files left to convert!")

    pickle.dump(
        eb_df, open(file_paths["pickles"] / Path("eb_df.pkl"), "wb"),
    )

    pickle.dump(
        res_df, open(file_paths["pickles"] / Path("res_df.pkl"), "wb"),
    )
    return


# loc[
#   IDX[:], IDX[:, :, :]
# ]#

# g = eb_df.loc[IDX[:191], IDX[province, energy_source, 1999]]
# print("g: ", g)

# # Last double-check
# pd.testing.assert_index_equal(
#     left=eb_data.index, right=eb_row_midx, check_names=False,
# )

# Last double-check
# pd.testing.assert_index_equal(
#     left=eb_data.columns, right=eb_col_midx, check_names=False,
# )

# print("eb_data: ", eb_data)
# eb_data.sort_index(inplace=True, axis="columns")

# renewables_df.set_index(renewables_row_midx, inplace=True)
# renewables_df.sort_index(inplace=True, axis="columns")

# ////////////////////////////////////////////////////////////////// PICKLE

# pickle.dump(
#     sectors_df,
#     open(
#         balances_directory_path.parent / Path("pickles/sectors_df.p"),
#         "wb",
#     ),
# )

# print("eb_data: ", eb_data.index)

# print("df: ", df)
# break

# for index, index_template in zip([eev_data.index, sectors_data,index], [e]):
#     check_index_errors(data=data)

# # Check if sheet has rows for sectors consumption
# if sectors_index == [-1] or df.index[1] == "in Tonnen":

#     # Set sector consumption rows to "NaN" for this e-source
#     eb_df.loc[190:, IDX[province, energy_source, :]] = float("NaN")

#     logging.getLogger().debug(
#         "No sector consumption for: {}-{}".format(
#             province, energy_source
#         )
#     )
# else:

#     # Extract data from sheet
#     sector_consumptions_data = df.iloc[sectors_index : sectors_index + 27, 1:32]

#     # Check if last row has the right index
#     assert sector_consumptions_data.index[-1] == "Sonstige", "Row slicing mismatch"

#     logging.getLogger().debug(
#         "{}: Sectors consumptions starts at {}".format(
#             energy_source, sectors_index
#         )
#     )

# sector_idx_check_df[energy_source] = False

# # Only proceed if consumption rows starts with "in Terajoules"
# if df.index[1] == "in Tonnen":
#     continue

#     print("\nenergy_source: ", energy_source)

# # /////////////////////////////////////////////////////// FIND PATH
# try:
#     # Find corresponding excel file for province
#     balance_file_path = list(filter(lambda x: province in x, files))[0]

# # CHECK 1: Xlxs file not found or not existing
# except FileNotFoundError as e:
#     raise e

# //////////////////////////////////////////////////////// CHECK DF

# (
#     eev_idx_check_df,
#     renewables_idx_check_df,
#     # sector_idx_check_df,
#     # sector_energy_idx_check_df,
# ) = create_idx_check_dfs(row_indices=row_indices)

# if province != "AT":

#     # ////////////////////////////////////////////////////// RENEWABLES
#     assign_renewables_table(
#         renewables_df=renewables_df,
#         renewables_sheet=renewables_sheet,
#         row_indices=row_indices,
#         province=province,
#         renewables_idx_check_df=renewables_idx_check_df,
#         years_range_data=years_range_data,
#     )

# # for energy_source in ["Steinkohle"]:
# for energy_source in dfs:
#     print("\nenergy_source: ", energy_source)

#     # ///////////////////////////////////////////////////////////// EEV
#     assign_eev_table(
#         eev_df=eev_df,
#         dfs=dfs,
#         row_indices=row_indices,
#         province=province,
#         energy_source=energy_source,
#         eev_idx_check_df=eev_idx_check_df,
#         years_range_data=years_range_data,
#     )

#     # ///////////////////////////////////////////// SECTORS CONSUMPTION
#     assign_sectors_consumption_table(
#         sectors_df=sectors_df,
#         dfs=dfs,
#         province=province,
#         energy_source=energy_source,
#         sector_idx_check_df=sector_idx_check_df,
#         years_range_data=years_range_data,
#     )

#     # /////////////////////////////////////// SECTOR ENERGY CONSUMPTION
#     assign_sector_energy_consumption_table(
#         sector_energy_df=sector_energy_df,
#         dfs=dfs,
#         province=province,
#         energy_source=energy_source,
#         sector_energy_idx_check_df=sector_energy_idx_check_df,
#         years_range_data=years_range_data,
#     )

# ////////////////////////////////////////////////////////////// CHECKS

# renewables_idx_check_df.to_excel(
#     balances_directory_path.parent
#     / "checks"
#     / "_".join([province, "renewables_idx_check_df.xlsx"])
# )

# eev_idx_check_df.to_excel(
#     balances_directory_path.parent
#     / Path("checks")
#     / "_".join([province, "eev_idx_check_df.xlsx"])
# )

# sector_idx_check_df.to_excel(
#     balances_directory_path.parent
#     / "checks"
#     / "_".join([province, "sector_idx_check_df.xlsx"])
# )

# sector_energy_idx_check_df.to_excel(
#     balances_directory_path.parent
#     / "checks"
#     / "_".join([province, "sector_energy_idx_check_df.xlsx"])
# )

# //////////////////////////////////////////////////// ADD MIDX ROW INDICES

# eev_df.set_index(eev_row_midx, inplace=True)
# eev_df.sort_index(inplace=True, axis="columns")

# renewables_df.set_index(renewables_row_midx, inplace=True)
# renewables_df.sort_index(inplace=True, axis="columns")

# # ////////////////////////////////////////////////////////////////// PICKLE

# pickle.dump(
#     eev_df,
#     open(balances_directory_path.parent / Path("pickles/eev_df.p"), "wb"),
# )

# pickle.dump(
#     sectors_df,
#     open(balances_directory_path.parent / Path("pickles/sectors_df.p"), "wb",),
# )

# pickle.dump(
#     sector_energy_df,
#     open(
#         balances_directory_path.parent / Path("pickles/sector_energy_df.p"),
#         "wb",
#     ),
# )

# pickle.dump(
#     renewables_df,
#     open(
#         balances_directory_path.parent / Path("pickles/renewables_df.p"), "wb"
#     ),
# )

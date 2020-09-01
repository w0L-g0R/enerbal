import logging
from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np
from utils import timeit

from enspect.files.energiebilanzen.data_structures import eb_sheet_names

from enspect.files.energiebilanzen.utils import (
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

from enspect.files.energiebilanzen.check_errors import check_index_errors
from enspect.paths import file_paths

from pprint import pprint

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
    files = list(file_paths["files_eb"].glob("*.xlsx"))
    pprint(files)

    # ///////////////////////////////////// COPY VALUES FROM EXCEL TO LOCAL DFS

    # Search for balance files @ EB file folder
    for file in files:
        print("file: ", file)

        filename = Path(file).stem

        # Filter current balances files
        if filename.startswith("EB"):

            file = str(Path(file))

            province = filename.split("_")[1]

        else:
            continue

        # Only unpack values for selected provinces
        if province in provinces:

            print("Province: ", province)

            write_to_log_file(
                log_file="EB_" + province, files=files, filename=filename,
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

                res_sheet = preprocess_res_sheet(
                    res_sheet=res_sheet,
                    res_conversion_factors=res_conversion_factors,
                    template_index=res_idx_template,
                    years=years,
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
        eb_df, open(file_paths["db_pickles"] / Path("eb.p"), "wb"),
    )

    pickle.dump(
        res_df, open(file_paths["db_pickles"] / Path("res.p"), "wb"),
    )
    return

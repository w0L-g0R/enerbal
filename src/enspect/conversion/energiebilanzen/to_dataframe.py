import logging
import pickle
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Union

import numpy as np
import pandas as pd
from utils import timeit

from enspect.aggregates.common import provinces
from enspect.aggregates.eb import eb_sheet_names
from enspect.conversion.energiebilanzen.check_errors import check_index_errors
from enspect.conversion.energiebilanzen.utils import (
    add_missing_row_indices,
    copy_eb_data,
    copy_res_data,
    create_index_template,
    create_indices,
    fetch_from_xlsx,
    get_sectors_data,
    preprocess_res_sheet,
    write_to_log_file,
)
from enspect.paths import file_paths

from pandas import IndexSlice as IDX

# //////////////////////////////////////////////////////////// CONVERT_EB_TO_DF


@timeit
def convert_energy_balances_to_dataframe(last_year: int,):
    """
    Make sure energy balance files follow the name convention: prefix "EB" + provinces_name + year_start(last two digits only) + year_end(last two digits only) , connected with underlines, eg. EB_Bgl_88_18. Use the province abbrevations as given in enspect.settings!
    """
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
    files = list(file_paths["folder_eb"].glob("*.xlsx"))
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
                log_file=file_paths["conversion_logs"]
                / "energiebilanzen"
                / ".".join((province, "log")),
                files=files,
                filename=filename,
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

    # Remove existing file if exists
    pickle_file = file_paths["pickle_eb"] / Path("eb.p")

    if pickle_file.exists():

        pickle_file.unlink()

        logging.getLogger().warning(
            "\n{}\n\n{} Removed existing file \n\n{}".format(
                "/" * 79, "\t" * 6, "/" * 79
            )
        )

    with open(pickle_file, "wb") as file:
        pickle.dump(eb_df, file)

    # Remove existing file if exists
    pickle_file = file_paths["pickle_res"]

    if pickle_file.exists():

        pickle_file.unlink()

        logging.getLogger().warning(
            "\n{}\n\n{} Removed existing file \n\n{}".format(
                "/" * 79, "\t" * 6, "/" * 79
            )
        )

    with open(pickle_file, "wb") as file:
        pickle.dump(eb_df, file)

    return

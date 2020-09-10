import logging
import pickle
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Union

import numpy as np
import pandas as pd
from enspect.utils import timeit
from enspect.aggregates.common import provinces
from enspect.paths import file_paths
from pandas import IndexSlice as IDX
from enspect.settings import set_pd_options

# //////////////////////////////////////////////////////////// CONVERT_EB_TO_DF


@timeit
def convert_stats_to_dataframe(xlsx_file_path: Path, pickle_path: Path):
    """
    TODO: Update for stats
    Assure dataframe template starts with "DF_" follows by a short, descriptive declararion. Same name as for the xlsx file gets used for pickling, e.g.: "DF_AREA.xlsx" -> area.p
    """
    set_pd_options()

    df = pd.read_excel(xlsx_file_path, index_col=0).iloc[3:, :-2]
    name = str(xlsx_file_path.stem).split("_")[1].rsplit(".xlsx")

    df.columns = pd.MultiIndex.from_product(
        iterables=[name, [np.nan], provinces], names=["BAGG_0", "ES", "PROV"]
    )

    # Have BAGG_0 as the index
    if df.index.name != "BAGG_0":
        df = df.T.unstack(["ES", "PROV"])

    if pickle_path.exists():

        pickle_path.unlink()

        logging.getLogger().warning(
            "\n{}\n\n{} Removed existing file \n\n{}".format(
                "/" * 79, "\t" * 6, "/" * 79
            )
        )

    with open(pickle_path, "wb") as f:
        pickle.dump(df, f)

    return

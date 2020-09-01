import datetime
import logging
from pathlib import Path
from typing import Dict, List, Union

import numpy as np
import pandas as pd
from logger.setup import setup_logging
from paths import file_paths
from utils import timeit


@timeit
def fetch_from_xlsx(file: str):

    return pd.read_excel(
        io=file, sheet_name=None, na_filter=False, index_col=0, header=0
    )


def create_thg_col_midx(
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
        [provinces, sectors, energy_usage_types, years], names=["PROV", "SRC", "CLS"],
    )

    return midx

# /////////////////////////////////////////////////////// CREATE_EEV_COL_MIDX


from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np


def create_eev_col_midx(last_year: int, sheets: List) -> pd.MultiIndex:

    bundeslaender = [
        "AT",
        "Bgd",
        "Ktn",
        "Noe",
        "Ooe",
        "Sbg",
        "Stk",
        "Tir",
        "Vbg",
        "Wie",
    ]

    years = [x for x in range(1988, last_year + 1, 1)]

    midx = pd.MultiIndex.from_product(
        [bundeslaender, sheets, years], names=["BL", "ET", "YEAR"]
    )

    return midx


# ////////////////////////////////////////////////// CREATE_RENEWABLES_COL_MIDX


def create_renewables_col_midx(last_year: int) -> pd.MultiIndex:

    bundeslaender = [
        "AT",
        "Bgd",
        "Ktn",
        "Noe",
        "Ooe",
        "Sbg",
        "Stk",
        "Tir",
        "Vbg",
        "Wie",
    ]

    years = [x for x in range(1970, last_year + 1, 1)]

    midx = pd.MultiIndex.from_product(
        [bundeslaender, years], names=["BL", "YEAR"])

    return midx

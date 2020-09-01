# %%
from enspect.paths import file_paths
import pickle
from pathlib import Path
from typing import List, Union

import numpy as np
import pandas as pd

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice


nea_df = pickle.load(
    open(
        file_paths["db_pickles"] / "nea.p",
        "rb",
    )
)
# nea_df.index.name = "ES"
# n = nea_df.head()
# # IDX rows = ENERGY SOURCE
# # IDX columns PROV, AGGREGATE, USAGE CAT, YEARS
s = nea_df.loc[
    IDX["Binnenschiffahrt"],
    IDX["Bgl", "Steinkohle", "Dampferzeugung", 2000],
]
print('s: ', s)
# s
# nea_df = nea_df.unstack(level="ET")  # .stack("BL")
# nea_df = nea_df.unstack(level=["BL", "ET", "USAGE", "YEAR"])  # .stack("BL")
# nea_df = nea_df.unstack(level="USAGE")  # .stack("BL")
# nea_df = nea_df.unstack(level="USAGE")  # .stack("BL")
# nea_df = nea_df.stack("BL")  # .stack("BL")

# nea_df.unstack("SECTOR")#.stack("SECTOR")

# %%

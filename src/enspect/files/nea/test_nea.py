#%%

import pandas as pd
from pathlib import Path
from typing import Union, List

import numpy as np
import pickle

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice

# sheets = pickle.load(
#     open("D:/_WORK/AEA/Projekte/bilanzen_monitor/src/sheets_ktn.p", "rb")
# )
#%%
nea_df = pickle.load(
    open(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/conversion/nea/pickles/nea.p",
        "rb",
    )
)
nea_df.index.name = "ET"
nea_df.head()
# IDX rows = ENERGY SOURCE
# IDX columns PROV, AGGREGATE, USAGE CAT, YEARS
s = nea_df.loc[
    IDX["Binnenschiffahrt", "Papier und Druck"],
    IDX["Ktn", "Steinkohle", "Dampferzeugung", 2000],
]
s
#%%
nea_df = nea_df.unstack(level="ET")  # .stack("BL")
nea_df = nea_df.unstack(level=["BL", "ET", "USAGE", "YEAR"])  # .stack("BL")
# nea_df = nea_df.unstack(level="USAGE")  # .stack("BL")
# nea_df = nea_df.unstack(level="USAGE")  # .stack("BL")
# nea_df = nea_df.stack("BL")  # .stack("BL")

# nea_df.unstack("SECTOR")#.stack("SECTOR")
nea_df.head()

# %%

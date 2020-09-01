# %%
import pandas as pd
from pathlib import Path
from typing import Union, List

import numpy as np
import pickle

from settings import provinces
from IPython.display import display


pd.set_option("display.max_columns", 50)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice

# %%

path_thg_df = Path.cwd() / "database/pickles/thg.p"

thg_df = pickle.load(
    open(
        path_thg_df,
        "rb",
    )
)
# # nea_df.index.name = "ET"
# thg_df.head()
# IDX rows = ENERGY SOURCE
# IDX columns PROV, AGGREGATE, USAGE CAT, YEARS
sources = thg_df.index.get_level_values(0).unique()
print('sources: ', sources)

# for province in provinces[:-1]:
#     s = thg_df.loc[
#         IDX["Energie"],
#         IDX[province, :]
#     ]
#    display(s)

for source in sources:
    s = thg_df.loc[
        IDX[:, "TOTAL"],
        IDX[:, :]
    ]

s = thg_df.T.groupby(["YEAR"]).sum()
# s = s.T.groupby("BL")
print("\n")
# print("/" * 79)
# print("\n")
display(s)

# s


# %%

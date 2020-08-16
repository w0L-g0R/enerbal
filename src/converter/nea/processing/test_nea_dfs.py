# %%
import pandas as pd
from pathlib import Path
from typing import Union, List

import numpy as np
import pickle

# import numpy as np

from nea_sheets import (
    sectors,
    energy_usage_types,
    energy_sources_93_98,
    energy_sources_99_plus,
    energy_sources_nea_df,
)

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice

# %%
sheets = pickle.load(
    open("D:/_WORK/AEA/Projekte/bilanzen_monitor/src/sheets_ktn.p", "rb")
)
nea_df = pickle.load(
    open("D:/_WORK/AEA/Projekte/bilanzen_monitor/src/nea_df.p", "rb"))


# %%
# IDX rows = ENERGY SOURCE
# IDX columns PROV, AGGREGATE, USAGE CAT, YEARS
nea_df.loc[IDX[:], IDX["Ktn", "Gesamt (ohne E1 - E7)", "Dampferzeugung", 2000]]

# %%
# %%
years = list(range(1999, 2019))


# %%

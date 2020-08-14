# %%
import pickle
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype
import numpy as np

pd.set_option("display.max_columns", None)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000


IDX = pd.IndexSlice


# %%
eev_df = pickle.load(open("/pickles/eev_df.p", "rb"))

bundesland = "Ktn"
energy_source = "Gesamtenergiebilanz"

eev_df_slice = eev_df.loc[
    IDX[:, "Gesamt", "Gesamt", "Gesamt",
        "Gesamt"], IDX[bundesland, energy_source, :]
]
eev_df_slice'

# %%

sectors_df = pickle.load(open("sectors_df.p", "rb"))

bundesland = "Ktn"
energy_source = "Gesamtenergiebilanz"

sectors_df_slice = sectors_df.loc[IDX[:], IDX[bundesland, energy_source, :]]
sectors_df_slice


# %%
# //////////////////////////////////////////////////////// ASSIGN_EEV_TABLE
renewables_df = pickle.load(open("renewables_df.p", "rb"))

renewables_sheet = pickle.load(open("renewables_sheet.p", "rb"))
renewables_sheet = renewables_sheet.iloc[2:, :].reset_index(drop=True)
renewables_sheet.columns = renewables_sheet.iloc[0, :].values
renewables_sheet.drop(
    labels=0, axis=0, inplace=True, errors="raise",
)


renewables_sheet.drop(
    labels=54, axis=0, inplace=True, errors="raise",
)

renewables_sheet.drop(
    labels=56, axis=0, inplace=True, errors="raise",
)

renewables_sheet.drop(
    labels=58, axis=0, inplace=True, errors="raise",
)

renewables_sheet.drop(
    labels=list(range(66, 163)), axis=0, inplace=True, errors="raise",
)

renewables_sheet.drop(
    labels=list(range(170, 175)), axis=0, inplace=True, errors="raise",
)

renewables_sheet.reset_index(drop=True, inplace=True)

renewables_sheet = renewables_sheet.iloc[:70, 1:]
renewables_df.loc[IDX[:], IDX["Ktn", :]]
# renewables_sheet


# renewables_sheet = renewables_sheet.astype("float64").dtypes
# renewables_sheet.dropna(axis=0, how="all", thresh=None, subset=None, inplace=True)


# %%
ren_df = pickle.load(open("ren.p", "rb"))

# ren_df.apply(lambda x: 0 if isinstance(x, str) else x)


for i in ren_df.index:
    # print(i)
    for j in ren_df.columns:
        # print(j)
        ren_df.loc[i, j]

        if isinstance(ren_df.loc[i, j], str):
            # print("ren_df.loc[i, j]: ", isinstance(ren_df.loc[i, j], str))

            ren_df.loc[i, j] = np.nan
            # print("ren_df.loc[i, j]: ", isinstance(ren_df.loc[i, j], str))

p = pd.Series(index=list(range(len(ren_df))), data=20)
# len(p)
print("len(p): ", len(ren_df))
print("len(p): ", len(p))
ren_df.mul(p, axis=0)

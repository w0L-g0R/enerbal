# %%
from pathlib import Path
import pandas as pd
import pickle
import xlwings as xw
from IPython.display import display
IDX = pd.IndexSlice
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

file = Path.cwd() / "src/files/stats/data/df_statistiken.xlsx"
sheet_names = [
    "AT_FLÄCHEN",
    "AT_PRIVATE_HAUSHALTE",
    "AT_BEVÖLKERUNG",
    "AT_PRIVATE_PKW_KM",
    "AT_WOHNFLÄCHE_AVG",
    "AT_BRP_REAL",
    "AT_HGS",
]
data = {}
for sheet_name in sheet_names:
    df = pd.read_excel(str(file), sheet_name=sheet_name, index_col=0)
    data = {
        "name": sheet_name,
        "df": df,
        "source": df.index.name
    }
    display(df)

    pickle.dump(data, open(sheet_name + ".pkl", "wb"))
# %%

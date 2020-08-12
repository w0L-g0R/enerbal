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

file = Path.cwd().parents[1] / "thg/data/df_THG_Luftschadstoff_1990_2017.xlsx"
sheet_names = [
    "AT_THG_EH_INDUSTRIE",
    "AT_THG_EH_ENERGIE",
]
data = {}
for sheet_name in sheet_names:
    df = pd.read_excel(str(file), sheet_name=sheet_name, index_col=0)
    data = {
        "name": sheet_name,
        "df": df,
        "source": df.iloc[0, 0]
    }
    display(df)

    pickle.dump(data, open(sheet_name + ".pkl", "wb"))

df = pd.read_excel(str(file), sheet_name="AT_THG", header=None)
df.set_index(0, inplace=True)

unit_series = df.iloc[1:, -1]
df = df.iloc[:, :-1]

provinces = df.iloc[0, :-1].unique()
sectors = df.iloc[1, :-1].unique()

midx = pd.MultiIndex.from_product(
    [provinces, sectors], names=["BL", "SECTOR"]
)

df.index.name = "THG_Emissionshandel_Länder_Luftschadstoff_Inventur_1990_2017, S.237"
df.columns = midx
df = df.iloc[2:, :]
df["Einheit"] = unit_series

data = {
    "name": "AT_THG",
    "df": df,
    "source": df.index.name
}

pickle.dump(data, open("AT_THG" + ".pkl", "wb"))
# %%

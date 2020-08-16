# from ig_wind.process.biv import biv_gesamt_tj
import xlwings as xw
import pandas as pd
from IPython.display import display
from pathlib import Path
import pickle
IDX = pd.IndexSlice

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
]

wb = xw.Book()

eev_pickle = Path().cwd() / "src/files/energiebilanzen/pickles/eev_df.p"
print('eev_pickle: ', eev_pickle)
eev_df = pickle.load(open(eev_pickle, "rb"))
print('eev_df: ', eev_df.head())

field = "Exporte"
energy_sources = ["Elektrische Energie"]
years = list(range(2000, 2019, 1))
provinces = provinces

dfs = []

for province in provinces:

    eev_data = eev_df.loc[
        IDX[field, "Gesamt", "Gesamt", "Gesamt",
            "Gesamt"], IDX[province, energy_sources, years]
    ].round(0)

    # name = "-".join([x for x in eev_data.name if x != "Gesamt"])
    eev_data.name = province
    eev_data = eev_data.droplevel([0, 1], axis=0)
    dfs.append(eev_data)

# ///////////////////////////////////////////////////////////////////// OUTPUTS
df = pd.concat(dfs, axis=1)
print('df: ', df)

# try:
wb.sheets.add(field)
#     ws = wb.sheets[field]
# except:
ws = wb.sheets[field]

ws.clear_contents()

ws.range("A1").value = f"Titel: {field}"
ws.range('A1').api.Font.Bold = True
ws.range("A2").value = df

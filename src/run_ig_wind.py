# from ig_wind.process.biv import biv_gesamt_tj
import xlwings as xw
from settings import provinces
import pandas as pd
from IPython.display import display
from pathlib import Path
import pickle
from ig_wind.processing.biv import (
    get_biv_gesamt_data,
    biv_gesamt_2018_xlsx,
    biv_gesamt_2018_pro_einwohner_xlsx,
    biv_gesamt_entwicklung_xlsx,
)

# ///////////////////////////////////////////////////////////// SETTINGS
energy_units = ["TJ", "PJ", "GWh", "TWh"]
# years = list(range(2000, 2019))

unit_energy = "TWh"
chart_width = 500
chart_height = 300

# ///////////////////////////////////////////////////////////// FILES

results_file = "src/charts.xlsx"
print("results_file: ", results_file)
wb = xw.Book(results_file)

eev_pickle = Path().cwd() / "src/files/energiebilanzen/pickles/eev_df.p"
eev_df = pickle.load(open(eev_pickle, "rb"))

bevölkerung_pickle = Path().cwd() / "src/files/stats/pickles/AT_Bevölkerung.pkl"
bevölkerung_df = pickle.load(open(bevölkerung_pickle, "rb"))

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

# ///////////////////////////////////////////////////////////// BIV
# ________________________________________________________ BIV 2018


biv_gesamt = get_biv_gesamt_data(
    eev_df=eev_df,
    field="Bruttoinlandsverbrauch",
    energy_sources=["Gesamtenergiebilanz"],
    years=list(range(2000, 2019, 1)),
    provinces=provinces,
)

biv_gesamt_2018_xlsx(
    wb=wb,
    sheet_name="BIV_2018",
    title="Bruttoinlandsverbrauch 2018",
    biv_gesamt=biv_gesamt,
    unit=unit_energy,
    energy_units=energy_units,
    provinces=provinces,
    width=chart_width,
    height=chart_height,
)

# biv_gesamt_2018_pro_einwohner_xlsx(
#     wb=wb,
#     sheet_name="BIV_2018_Einwohner",
#     title="BIV gesamt 2018 pro Einwohner*in",
#     biv_gesamt=biv_gesamt,
#     bevölkerung=bevölkerung_df,
#     unit=unit_energy,
#     energy_units=energy_units,
#     provinces=provinces,
#     width=chart_width,
#     height=chart_height,
# )

# biv_gesamt_entwicklung_xlsx(
#     wb=wb,
#     sheet_name="BIV_Entwicklung",
#     title="Bruttoinlandsverbrauch Entwicklung",
#     biv_gesamt=biv_gesamt,
#     unit=unit_energy,
#     energy_units=energy_units,
#     provinces=provinces,
#     years=list(range(2000, 2019)),
#     width=chart_width,
#     height=chart_height,
# )

# biv_gesamt_2000_2018_to_xlsx(
#     wb=wb,
#     sheetname="Bruttoinlandsverbrauch Entwicklung",
#     title="BIV Gesamt Index 2000-2018",
#     biv_gesamt=biv_gesamt,
#     unit=unit_energy,
#     energy_units=energy_units,
#     provinces=provinces,
#     width=chart_width,
#     height=chart_height,
# )

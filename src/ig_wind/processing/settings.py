
import pickle
import pandas as pd
from pathlib import Path
# from files.energiebilanzen.processing.eb_sheets import eb_sheets

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# ////////////////////////////////////////////////////////////////// CONVERSION

conversion = {
    "mwh_2_gwh": 0.001,
    "gwh_2_tj": (1 / 0.27778),
    "tj_2_pj": 0.001,
    "gwh_2_mwh": 1000,
    "tj_2_gwh": 0.27778,
    "tj_2_twh": 0.27778 / 1000,
    "pj_2_tj": 1000,
}
# /////////////////////////////////////////////////////////////////// PROVINCES

provinces_names = [
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

provinces_names_new = [
    "AT",
    "BGL",
    "KTN",
    "NOE",
    "OOE",
    "SBG",
    "STK",
    "TIR",
    "VOR",
    "WIE",
]

provinces_rgb = {

    "AT": (0, 0, 0),
    "Bgd": (230, 25, 75),
    "Ktn": (210, 245, 60),
    "Noe": (70, 240, 240),
    "Ooe": (128, 128, 128),
    "Sbg": (240, 50, 230),
    "Stk": (128, 0, 0),
    "Tir": (145, 30, 180),
    "Vbg": (60, 180, 75),
    "Wie": (245, 130, 48),
}
# //////////////////////////////////////////////////////////////////////// EEV

eev_file = Path.cwd().parent / "files/energiebilanzen/pickles/eev_df.p"
print('eev_file: ', eev_file)
eev_df = pickle.load(
    open(eev_file, "rb"))

eev_source = "Energiebilanzen Österreich"

# # //////////////////////////////////////////////////////////////////////// RES
# res_file = Path.cwd().parent / "files/energiebilanzen/pickles/renewables_df.p"
# res_file = pickle.load(
#     open(res_file, "rb"))

# # //////////////////////////////////////////////////////////////////////// NEA
# res_file = Path.cwd().parent / "files/nea/pickles/nea.p"
# res_file = pickle.load(
#     open(res_file, "rb"))

# # ///////////////////////////////////////////////////////////////// OUTPUT FILE
# ouput_file = Path.cwd().parent / "files/energiebilanzen/pickles/nea.p"

# eev_file = Path(
#     "files/energiebilanzen/pickles/eev_df.p")
# res_file = Path(
#     "C:/Users/WGO/Desktop/statsview_ipynb/files/energiebilanzen/pickles/renewables_df.p")
# nea_file = Path(
#     "C:/Users/WGO/Desktop/statsview_ipynb/files/nea/pickles/nea_df.p")
output_file = Path("C:/Users/WGO/Desktop/statsview_ipynb/files/data.xlsx")

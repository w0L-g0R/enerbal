
import pickle
import pandas as pd
from pathlib import Path

from gui.utils import create_row_indices, create_eev_energy_source_options
from files.energiebilanzen.processing.eb_sheets import eb_sheets

eev_indices = create_row_indices(_type="EEV")
sectors_indices = create_row_indices(_type="Sektoren")
sector_energy_indices = create_row_indices(_type="Sektor Energie")
renewables_indices = create_row_indices(_type="ErnRL")

energy_sources_options = create_eev_energy_source_options(
    energy_sources=eb_sheets)


conversion_multiplicators = {
    "mwh_2_gwh": 0.001,
    "gwh_2_tj": (1 / 0.27778),
    "tj_2_pj": 0.001,
    "gwh_2_mwh": 1000,
    "tj_2_gwh": 0.27778,
    "pj_2_tj": 1000,
}

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

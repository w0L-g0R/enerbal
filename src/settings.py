
import pickle
import pandas as pd
from pathlib import Path

from gui.utils import create_eev_indices, get_eb_indices, create_eev_energy_source_options
from files.energiebilanzen.processing.eb_sheets import eb_sheets

eb_indices = get_eb_indices()

eev_indices = create_eev_indices(eb_indices=eb_indices)
sectors_indices = eb_indices["IDX_EEV_SECTORS"].iloc[3:]
sector_energy_indices = eb_indices["IDX_SECTOR_ENERGY"].iloc[3:]
renewables_indices = eb_indices["IDX_RENEWABLES"]

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

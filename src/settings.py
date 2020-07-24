
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

aggregates_eb = [
    {"label": "Hauptaggregate", "value": "Hauptaggregate"},
    {"label": "Elektrische Energie", "value": "Elektrische Energie"},
    {"label": "Erneuerbare", "value": "Erneuerbare"},
    {"label": "Fossil-fest", "value": "Fossil-fest"},
    {"label": "Fossil-flüssig", "value": "Fossil-flüssig"},
    {"label": "Fossil-gasförmig", "value": "Fossil-gasförmig"},
    {"label": "Biogen-fest", "value": "Biogen-fest"},
    {"label": "Biogen-flüssig", "value": "Biogen-flüssig"},
    {"label": "Biogen-gasförmig", "value": "Biogen-gasförmig"},
    {"label": "Umgebungswärme", "value": "Umgebungswärme"},
    {"label": "Wasserkraft", "value": "Wasserkraft"},
    {"label": "Abfall", "value": "Abfall"},
]

units = [
    {"label": "TJ", "value": "TJ"},
    {"label": "PJ", "value": "PJ"},
    {"label": "GWh", "value": "GWh"},
    {"label": "TWh", "value": "TWh"},
    {"label": "MW", "value": "MW", "disabled": True},
    {"label": "h", "value": "h", "disabled": True},
    {"label": "%", "value": "%", "disabled": True},
]

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

DEFAULT_CHART_CONFIG = {
    'modeBarButtons': [
        [
            'toImage',
            'sendDataToCloud',
            'zoom2d',
            'pan2d',
            'zoomIn2d',
            'zoomOut2d',
            'autoScale2d',
            'resetScale2d',
            'toggleSpikelines',
            'hoverClosestCartesian',
            'hoverCompareCartesian',
            'drawline',
            'drawopenpath',
            'drawclosedpath',
            'drawcircle',
            'drawrect',
            'eraseshape'
        ]
    ],
    'displaylogo': False,
    "showLink": True,
    'editable': True,
    "plotlyServerURL": "https://chart-studio.plotly.com",
    'toImageButtonOptions': {
        'format': 'png',  # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 500,
        'width': 700,
        'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
    }
}

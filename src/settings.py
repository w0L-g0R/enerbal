
import pickle
import pandas as pd
from pathlib import Path
from gui.assets.styles import range_slider_style, label_style

from gui.utils import create_row_indices, create_eev_energy_source_options
from files.energiebilanzen.processing.eb_sheets import eb_sheets

eev_indices = create_row_indices(_type="EEV")
sectors_indices = create_row_indices(_type="Sektoren")
sector_energy_indices = create_row_indices(_type="Sektor Energie")
renewables_indices = create_row_indices(_type="ErnRL")

energy_sources_options = create_eev_energy_source_options(
    energy_sources=eb_sheets)

chart_type_options = {
    "Bar": {"label": "Bar", "style": range_slider_style},
    "Bar+": {"label": "Bar+", "style": range_slider_style},
    "Line": {"label": "Line", "style": range_slider_style},
    "Area": {"label": "Map", "style": range_slider_style},
    "Pie": {"label": "Pie", "style": range_slider_style},
    "Sun": {"label": "Sun", "style": range_slider_style},
    "Map": {"label": "Map", "style": range_slider_style},
    "Sankey": {"label": "Sankey", "style": range_slider_style},
    "Ratio": {"label": "Sankey", "style": range_slider_style},
}

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

scale_options = {
    0: {"label": "Absolute", "style": range_slider_style},
    1: {"label": "Normalized", "style": range_slider_style},
    2: {"label": "Index", "style": range_slider_style},
}

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
    "edits": {
        "titleText": True,
    },
    'modeBarButtons': [
        [
            'toImage',
            'sendDataToCloud',
            'zoom2d',
            'pan2d',
            # 'lasso',
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
    'responsive': True,
    'displaylogo': False,
    "showLink": False,
    # 'editable': True,
    "plotlyServerURL": "https://chart-studio.plotly.com",
    'toImageButtonOptions': {
        'format': 'png',  # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 500,
        'width': 700,
        'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
    }
}

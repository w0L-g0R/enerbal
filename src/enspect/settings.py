# from enspect.conversion.energiebilanzen.convert.get_eb_data_structures import eb_sheets
import pickle
from pathlib import Path

import pandas as pd

from enspect.gui.assets.styles import label_style, range_slider_style
from enspect.paths import file_paths
from enspect.utils import create_row_indices


def set_pd_options():
    pd.set_option("display.max_columns", 10)  # or 1000
    pd.set_option("display.max_rows", None)  # or 1000
    pd.set_option("display.width", None)  # or 1000
    pd.set_option("max_colwidth", 20)  # or 1000
    # pd.set_option("display.multi_sparse", True)  # or 1000
    # pd.set_option("display.column_space", 5)  # or 1000
    # pd.set_option("display.colheader_justify", "left")  # or 1000
    # pd.set_option("display.precision", 2)  # or 1000
    return


provinces_hex = {
    "AT": "161716",
    "Bgl": "64BDF5",  # hellblau
    "Ktn": "DCE374",  # dunkelrot
    "Noe": "AB5554",  # rot
    "Ooe": "D19F5A",  # orange
    "Sbg": "435694",  # limette
    "Stk": "32A852",  # grün
    "Tir": "9A5FBA",  # dunkelgrün
    "Vor": "59C7CF",  # braun
    "Wie": "2A6E3B",  # deeppink
}


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

unit_converter = {
    "MWh_2_GWh": 0.001,
    "GWh_2_TJ": (1 / 0.27778),
    "GWh_2_MWh": 1000,
    "TJ_2_PJ": 0.001,
    "PJ_2_TJ": 1000,
    "TJ_2_GWh": 0.27778,
    "TJ_2_TWh": 0.27778 / 1000,
}


DEFAULT_CHART_CONFIG = {
    "edits": {
        "titleText": True,
    },
    "modeBarButtons": [
        [
            "toImage",
            "sendDataToCloud",
            "zoom2d",
            "pan2d",
            # 'lasso',
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
            "toggleSpikelines",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape",
        ]
    ],
    "responsive": True,
    "displaylogo": False,
    "showLink": False,
    # 'editable': True,
    "plotlyServerURL": "https://chart-studio.plotly.com",
    "toImageButtonOptions": {
        "format": "png",  # one of png, svg, jpeg, webp
        "filename": "custom_image",
        "height": 500,
        "width": 700,
        "scale": 1,  # Multiply title/legend/axis/canvas sizes by this factor
    },
}


# //////////////////////////////////////////////////////////////////// GUI STUFF
# aggregates_eb = [
#     {"label": "Hauptaggregate", "value": "Hauptaggregate"},
#     {"label": "Elektrische Energie", "value": "Elektrische Energie"},
#     {"label": "Erneuerbare", "value": "Erneuerbare"},
#     {"label": "Fossil-fest", "value": "Fossil-fest"},
#     {"label": "Fossil-flüssig", "value": "Fossil-flüssig"},
#     {"label": "Fossil-gasförmig", "value": "Fossil-gasförmig"},
#     {"label": "Biogen-fest", "value": "Biogen-fest"},
#     {"label": "Biogen-flüssig", "value": "Biogen-flüssig"},
#     {"label": "Biogen-gasförmig", "value": "Biogen-gasförmig"},
#     {"label": "Umgebungswärme", "value": "Umgebungswärme"},
#     {"label": "Wasserkraft", "value": "Wasserkraft"},
#     {"label": "Abfall", "value": "Abfall"},
# ]

# chart_type_options = {
#     "Bar": {"label": "Bar", "style": range_slider_style},
#     "Bar+": {"label": "Bar+", "style": range_slider_style},
#     "Line": {"label": "Line", "style": range_slider_style},
#     "Area": {"label": "Map", "style": range_slider_style},
#     "Pie": {"label": "Pie", "style": range_slider_style},
#     "Sun": {"label": "Sun", "style": range_slider_style},
#     "Map": {"label": "Map", "style": range_slider_style},
#     "Sankey": {"label": "Sankey", "style": range_slider_style},
#     "Ratio": {"label": "Sankey", "style": range_slider_style},
# }

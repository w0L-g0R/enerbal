import inspect
import json
import os
import pickle
from pathlib import Path
from time import time
from typing import Dict, List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from gui.app import app
from gui.assets.AEA_colors import provinces_color_table
from gui.layouts import get_graph_layout
from gui.utils import show_callback_context
from pandas.core.common import flatten
from settings import DEFAULT_CHART_CONFIG
from utils import multiplicator

IDX = pd.IndexSlice


def change_unit(scale: str, setup: Dict, energy_source: str = None, year: int = None):

    if setup["xaxis_type"] == "Jahre":

        if setup["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:
            data_slice = (
                setup["data"]
                .loc[
                    IDX[setup["row_index"]],
                    IDX[
                        setup["provinces"],
                        energy_source,
                        setup["years"],
                    ],
                ]
                .fillna(0)
            )

        if "ErnRL" in setup["data_section"]:
            data_slice = (
                setup["data"]
                .loc[
                    IDX[setup["row_index"]],
                    IDX[
                        setup["provinces"],
                        setup["years"],
                    ],
                ]
                .fillna(0)
            )

        # if setup["scale"] == "Normalized":

        #     sum_per_year = data_slice.T.groupby(
        #         'YEAR').sum()

        #     data_slice = data_slice.T.groupby("YEAR").apply(
        #         lambda x: x / sum_per_year
        #     ).T * multiplicator(
        #         unit=setup["unit"], normalized=True
        #     )

        #     unit = "%"

        else:

            data_slice = data_slice.apply(pd.to_numeric) * multiplicator(
                unit=setup["unit"]
            )

            unit = setup["unit"]

    if setup["xaxis_type"] == "Bundesländer":

        if setup["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:
            data_slice = (
                setup["data"]
                .loc[
                    IDX[setup["row_index"]],
                    IDX[
                        setup["provinces"],
                        setup["energy_sources"],
                        year,
                    ],
                ]
                .fillna(0)
            )

        if "ErnRL" in setup["data_section"]:
            data_slice = (
                setup["data"]
                .loc[
                    IDX[setup["row_index"]],
                    IDX[
                        setup["provinces"],
                        year,
                    ],
                ]
                .fillna(0)
            )

        # if setup["scale"] == "Normalized":

        #     sum_per_year = data_slice.T.groupby(
        #         'BL').sum()

        #     data_slice = data_slice.T.groupby("PROV").apply(
        #         lambda x: x / sum_per_year
        #     ).T * multiplicator(
        #         unit=setup["unit"], normalized=True
        #     )

        #     unit = "%"

        else:

            data_slice = data_slice.apply(pd.to_numeric) * multiplicator(
                unit=setup["unit"]
            )

            unit = setup["unit"]

    return data_slice, unit

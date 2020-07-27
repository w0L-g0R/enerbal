from settings import DEFAULT_CHART_CONFIG
import pickle
from gui.assets.AEA_colors import provinces_color_table
from gui.layouts import get_graph_layout
import dash_html_components as html
from pandas.core.common import flatten
import inspect
import os
from typing import List, Dict
from pathlib import Path
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from gui.utils import multiplicator
import json
from gui.app import app
from gui.utils import show_callback_context
from dash import no_update
import numpy as np
from time import time
IDX = pd.IndexSlice


def on_bar_plus(setup: dict):

    graphs = []
    updated_figures = {}

    for title, figure in setup["figures"].items():

        # data = figure["data"]
        # layout = figure["layout"]
        # graphs.append(
        #     html.Hr(style={"background-color": "lightblue"}),
        # )
        if figure["data"][0]["orientation"] == "v":
            orientation = "h"
        else:
            orientation = "v"

        for trace in figure["data"]:
            trace["x"], trace["y"] = trace["y"], trace["x"]

            trace["orientation"] = orientation
            trace["hovertemplate"] = '%{x: .0f}'

        dict_of_fig = dict({
            "data": figure["data"],
            "layout": figure["layout"]
        })

        fig = go.Figure(dict_of_fig)

        fig.update_layout(
            xaxis=dict(
                title=figure["layout"]["yaxis"]["title"]["text"],
                tickangle=0,

            ),
            yaxis=dict(
                title=figure["layout"]["xaxis"]["title"]["text"],
                # categoryorder="array",
                # categoryarray=[x for _, x in sorted(
                #     zip(trace["y"], trace["x"]))]

            ),
            legend=dict(x=0, y=-0.24),

        )

        setup["figures"][title] = fig

        graphs.append(
            dcc.Graph(
                # id=f"{setup['graph_id']}-figure",
                responsive=True,
                # responsive=False,
                config=DEFAULT_CHART_CONFIG,
                style={
                    "height": "100%",
                    "width": "100%"},
                figure=fig,
            )
            #     ]
            # )
        )
        graphs.append(
            html.Hr(style={"background-color": "lightblue"}),
        )

    return graphs, setup

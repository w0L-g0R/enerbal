import numpy as np
from settings import DEFAULT_CHART_CONFIG, scale_options
import inspect
import os
from typing import List
import dash_html_components as html
from gui.layouts import get_graph_layout

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from gui.app import app
from gui.utils import show_callback_context
from dash import no_update
import pickle
from pprint import pprint
from typing import List, Dict
from dash_table.Format import Format
IDX = pd.IndexSlice


def create_on_update(graph_id: str):
    @app.callback(
        [
            Output(f"{graph_id}-update", "data"),
            Output(f"{graph_id}-container", "children"),
        ],
        [
            Input(f"{graph_id}-setup", "data"),
            Input(f"{graph_id}-options-1", "value"),
            Input(f"{graph_id}-options-2", "value"),
            Input(f"{graph_id}-scale", "value"),
            Input(f"{graph_id}-btn-bar", "n_clicks"),
            Input(f"{graph_id}-btn-line", "n_clicks"),
            Input(f"{graph_id}-btn-pie", "n_clicks"),
            Input(f"{graph_id}-btn-map", "n_clicks"),
            Input(f"{graph_id}-btn-barplus", "n_clicks"),
            Input(f"{graph_id}-btn-area", "n_clicks"),
            Input(f"{graph_id}-btn-sunburst", "n_clicks"),
            Input(f"{graph_id}-btn-sankey", "n_clicks"),
            Input(f"{graph_id}-btn-save", "n_clicks"),
            Input(f"{graph_id}-btn-xlsx", "n_clicks"),
            Input(f"{graph_id}-btn-image", "n_clicks"),
            Input(f"{graph_id}-btn-ratio", "n_clicks"),

        ],
        # [
        # State(f"{graph_id}-unit", "value"),
        # ]

    )
    def on_update(
        setup: Dict,
        options_1: List,
        options_2: List,
        scale: str,
        bar,
        line,
        pie,
        map,
        barplus,
        area,
        sunburst,
        sankey,
        save,
        xlsx,
        image,
        ratio
    ):

        # Log callback information
        show_callback_context(
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
            verbose=True,
        )

        # Get callback information to define the triggered input
        ctx = callback_context
        triggered = ctx.triggered

        if triggered:

            update = {}
            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            if "setup" in triggered_prop_id:
                # update["setup"] = setup
                update["type"] = "setup"

            if "options-1" in triggered_prop_id:
                update["type"] = "rotate_axes"

            if "scale" in triggered_prop_id:
                update["type"] = "scale"
                update["scale"] = scale_options[scale[0]]["label"]
                print('update["scale"]: ', update["scale"])

            return update, html.Div(
                dbc.Container(
                    style={"margin-top": 12},
                    id=f"{graph_id}-box",
                )
            )

        else:
            raise PreventUpdate
            # if "graph-A" in triggered_prop_id:
            #     graph_id = "graph-A"

            # if "graph-B" in triggered_prop_id:
            #     graph_id = "graph-B"

            # setup = pickle.load(
            #     open(graph_id + ".p", "rb"))

            # graphs = []
            # print('setup: ', setup)
            # print('figures: ', figures)

            # pprint(data)

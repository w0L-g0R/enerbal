import inspect
import os
from typing import List
import dash_html_components as html

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
import dash_table
import pickle
import dash_table.FormatTemplate as FormatTemplate
from gui.assets.AEA_colors import provinces_color_table, provinces_color_table_rgba

from dash_table.Format import Format
IDX = pd.IndexSlice


def create_on_update_graph(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-figure", "figure"),
        [
            Input(f"{graph_id}-updates-scale", "data"),
        ],
    )
    def on_update_graph(
        figure_after_scale_update,
    ):

        # Log callback information
        # show_callback_context(
        #     func_name=inspect.stack()[0][3],
        #     file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
        #     verbose=False,
        # )

        # Get callback information to define the triggered input
        ctx = callback_context
        triggered = ctx.triggered

        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            return triggered_value
        else:
            raise PreventUpdate

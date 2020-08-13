import inspect
import os
from typing import List
import dash_html_components as html
import json
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

from files.energiebilanzen.processing.get_energy_source_aggregates import energy_source_aggregates

from dash_table.Format import Format
IDX = pd.IndexSlice


def callback_return_on_select_aggregate(
    updates_scale: str = no_update,
    absolute_values: List = no_update,
):
    return [
        updates_scale,
        absolute_values
    ]
# _________________________________________________________________________
# ///////////////////////////////////////////////////////////////// DISPATCH EL


def create_on_select_aggregate(graph_id: str):
    @ app.callback(
        Output(f"{graph_id}-energy-sources", "value"),
        [
            Input(f"{graph_id}-aggregate-eb", "value"),
        ],
        [
            State(f"tabs-{graph_id}", "active_tab"),
        ]
    )
    def on_select_aggregate(
        aggregate_eb,
        active_tab
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

        if "eb" in active_tab:
            return energy_source_aggregates[aggregate_eb]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

import inspect
import os
from typing import List

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

from gui.components.views.setup import eev_idx_rows  # ,  # sectors_idx_rows
IDX = pd.IndexSlice


def create_on_switch_eb_data_section(graph_id: str):
    @app.callback(
        Output(f"idx-section-{graph_id}", "children"),
        [
            Input(f"data-section-{graph_id}", "value"),
        ],
    )
    def on_switch_eb_data_section(data_section):

        show_callback_context(
            verbose=True,
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
        )
        # Get callback information to define the triggered input
        ctx = callback_context
        triggered = ctx.triggered
        states = ctx.states
        inputs = ctx.inputs

        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            if "EEV" in data_section:
                if "graph-A" in triggered_prop_id:
                    return eev_idx_rows(graph_id="graph-A")

                elif "graph-B" in triggered_prop_id:
                    return eev_idx_rows(graph_id="graph-B")

            if "Sektoren" in data_section:
                if "graph-A" in triggered_prop_id:
                    return sectors_idx_rows(graph_id="graph-A")

                elif "graph-B" in triggered_prop_id:
                    return sectors_idx_rows(graph_id="graph-B")

        else:
            if "graph-A" in triggered_prop_id:
                return eev_idx_rows(graph_id="graph-A")

            elif "graph-B" in triggered_prop_id:
                return eev_idx_rows(graph_id="graph-B")

from settings import eev_indices
import inspect
import os
from typing import List, Dict

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

IDX = pd.IndexSlice


# def callback_on_select_graph_dropdowns(
#     graph: object
# ):

#     return [
#         idx_0,
#         idx_1,
#         idx_2,
#         idx_3,
#         idx_4,
#         idx_0_disabled,
#         idx_1_disabled,
#         idx_2_disabled,
#         idx_3_disabled,
#         idx_4_disabled,
#     ]


def create_on_select_graph_dropdowns(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-box", "children"),

        [Input(f"{graph_id}-plots", "value")],
        [State(f"{graph_id}-figures", "data")],
    )
    def on_select_graph_dropdowns(
        plots_dropdown_value: str,
        graph_figures: Dict,
    ):

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
            if triggered_value is not None:

                print('plots_dropdown_value: ', plots_dropdown_value)
                print('graph_figures: ', graph_figures.keys())

                graph = graph_figures[plots_dropdown_value]
                return graph
            else:
                raise PreventUpdate

        else:
            raise PreventUpdate

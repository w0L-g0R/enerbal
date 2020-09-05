import inspect
import os

import pandas as pd
from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from gui.app import app
from gui.utils import show_callback_context

from pandas import IndexSlice as IDX

# _________________________________________________________________________
# ///////////////////////////////////////////////////////////////// DISPATCH EL


def callback_return_on_click_update(_type: object = no_update):

    return [_type]


def create_on_click_update(graph_id: str):
    @app.callback(
        [
            # Output(f"{graph_id}-box", "children"),
            Output(f"{graph_id}-setup", "data"),
            # Output(f"{graph_id}-clicked-sectors-update", "data"),
            # Output(f"{graph_id}-clicked-sector-energy-update", "data"),
            # Output(f"{graph_id}-clicked-renewables-update", "data"),
            # Output(f"{graph_id}-clicked-nea-update", "data"),
            # Output(f"{graph_id}-clicked-thg-update", "data"),
            # Output(f"{graph_id}-clicked-stats-update", "data"),
        ],
        [Input(f"btn-plot-{graph_id}", "n_clicks"),],
        [
            State(f"tabs-{graph_id}", "active_tab"),
            State(f"data-section-{graph_id}", "value"),
        ],
    )
    def on_click_update(n_clicks_update, active_tab, eb_data_type):

        # Log callback information
        show_callback_context(
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
            verbose=True,
        )

        # Get callback information to define the triggered input
        ctx = callback_context
        triggered = ctx.triggered
        print("eb_data_type: ", eb_data_type)
        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_prop_id = triggered[0]["value"]

            if "eb" in active_tab:

                if eb_data_type == "EEV":
                    # print('eb_data_type: ', eb_data_type)
                    return callback_return_on_click_update(_type="EEV")

                if eb_data_type == "Sektoren":

                    return callback_return_on_click_update(_type="Sektoren")

                if eb_data_type == "ErnRL":

                    return callback_return_on_click_update(_type="ErnRL")
        else:
            # callback_on_click_update(eev="True")
            raise PreventUpdate
            # eev_slice = pickle.load(

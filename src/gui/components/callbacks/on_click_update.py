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
import dash_table

from gui.app import app
from gui.assets.AEA_colors import provinces_color_table
from gui.utils import get_graph_layout, show_callback_context
from settings import provinces_names, eev_indices, energy_sources_options
from dash import no_update
import pickle
from pathlib import Path
from files.energiebilanzen.processing.eb_sheets import eb_sheets

IDX = pd.IndexSlice
# _________________________________________________________________________
# ///////////////////////////////////////////////////////////////// DISPATCH EL


def callback_on_click_update(eev: object = no_update, sectors: object = no_update, sector_energy: object = no_update, renewables: object = no_update, nea: object = no_update, thg: object = no_update, stats: object = no_update):

    return [
        eev,
        sectors,
        sector_energy,
        renewables,
        nea,
        thg,
        stats
    ]


def create_on_click_update(graph_id: str):
    @app.callback(
        [
            # Output(f"box-{graph_id}", "children"),
            Output(f"{graph_id}-clicked-eev-update", "data"),
            Output(f"{graph_id}-clicked-sectors-update", "data"),
            Output(f"{graph_id}-clicked-sector-energy-update", "data"),
            Output(f"{graph_id}-clicked-renewables-update", "data"),
            Output(f"{graph_id}-clicked-nea-update", "data"),
            Output(f"{graph_id}-clicked-thg-update", "data"),
            Output(f"{graph_id}-clicked-stats-update", "data"),
        ],
        [Input(f"update-{graph_id}", "n_clicks"), ],
        [State(f"tabs-{graph_id}", "active_tab"),
         State(f"data-section-{graph_id}", "value"),
         ],
    )
    def on_click_update(
        n_clicks_update,
        active_tab,
        eb_data_type
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

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_prop_id = triggered[0]["value"]

            if "eb" in active_tab:

                if eb_data_type == "EEV":
                    # print('eb_data_type: ', eb_data_type)
                    return callback_on_click_update(eev="True")

                if eb_data_type == "Sektoren":

                    return callback_on_click_update(sectors="True")
        else:
            # callback_on_click_update(eev="True")
            raise PreventUpdate
            # eev_slice = pickle.load(

import inspect
import os

import pandas as pd
from dash import callback_context
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from gui.app import app
from gui.utils import show_callback_context

from pandas import IndexSlice as IDX


def callback_return_on_switch_eb_data_section(
    display_eev_idx: str = {"display": "none"},
    display_sectors_idx: str = {"display": "none"},
    display_sector_energy_idx: str = {"display": "none"},
    display_res_idx: str = {"display": "none"},
):

    return [
        display_eev_idx,
        display_sectors_idx,
        display_sector_energy_idx,
        display_res_idx,
    ]


def create_on_switch_eb_data_section(graph_id: str):
    @app.callback(
        [
            Output(f"idx-eev-{graph_id}", "style"),
            Output(f"idx-sectors-{graph_id}", "style"),
            Output(f"idx-sector-energy-{graph_id}", "style"),
            Output(f"idx-renewables-{graph_id}", "style"),
        ],
        [Input(f"{graph_id}-data-section", "value"),],
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
        inputs = list(inputs.keys())[0]
        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            if "EEV" in data_section:
                # if "graph-A" in triggered_prop_id:
                return callback_return_on_switch_eb_data_section(
                    display_eev_idx={"display": "inline"},
                )

                # elif "graph-B" in triggered_prop_id:
                # return eev_idx_rows(graph_id="graph-B")

            if "Sektoren" in data_section:

                return callback_return_on_switch_eb_data_section(
                    display_sectors_idx={"display": "inline"},
                )

                # if "graph-A" in triggered_prop_id:
                #     return sectors_idx_rows(graph_id="graph-A")

                # elif "graph-B" in triggered_prop_id:
                #     return sectors_idx_rows(graph_id="graph-B")

            if "Sektor Energie" in data_section:

                return callback_return_on_switch_eb_data_section(
                    display_sector_energy_idx={"display": "inline"},
                )
            if "ErnRL" in data_section:

                return callback_return_on_switch_eb_data_section(
                    display_res_idx={"display": "inline"},
                )
        # else:
        #     if "graph-A" in inputs:
        #         return eev_idx_rows(graph_id="graph-A")

        #     elif "graph-B" in inputs:
        #         return eev_idx_rows(graph_id="graph-B")

        #     if "EEV" in data_section:
        #         if "graph-A" in triggered_prop_id:
        #             return eev_idx_rows(graph_id="graph-A")

        #         elif "graph-B" in triggered_prop_id:
        #             return eev_idx_rows(graph_id="graph-B")

        #     if "Sektoren" in data_section:
        #         if "graph-A" in triggered_prop_id:
        #             return sectors_idx_rows(graph_id="graph-A")

        #         elif "graph-B" in triggered_prop_id:
        #             return sectors_idx_rows(graph_id="graph-B")

        #     if "Sektor Energie" in data_section:
        #         if "graph-A" in triggered_prop_id:
        #             return sector_energy_idx_rows(graph_id="graph-A")

        #         elif "graph-B" in triggered_prop_id:
        #             return sector_energy_idx_rows(graph_id="graph-B")

        #     if "ErnRL" in data_section:
        #         if "graph-A" in triggered_prop_id:
        #             return renewables_idx_rows(graph_id="graph-A")

        #         elif "graph-B" in triggered_prop_id:
        #             return renewables_idx_rows(graph_id="graph-B")

        else:
            raise PreventUpdate
            # if "graph-A" in inputs:
            #     return eev_idx_rows(graph_id="graph-A")

            # elif "graph-B" in inputs:
            #     return eev_idx_rows(graph_id="graph-B")

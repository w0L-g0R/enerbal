import pickle
from gui.assets.AEA_colors import provinces_color_table
from gui.layouts import get_graph_layout
import dash_html_components as html

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
IDX = pd.IndexSlice

# def callback_on_plot(
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


def create_on_plot(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-box", "children"),

        [
            Input(f"{graph_id}-plots", "value"),
            Input(f"{graph_id}-setup", "data"),

        ],
        # [State(f"{graph_id}-setup", "data"),
        #  State(f"idx-eev-0-{graph_id}", "disabled"),
        #  State(f"idx-eev-1-{graph_id}", "disabled"),
        #  State(f"idx-eev-2-{graph_id}", "disabled"),
        #  State(f"idx-eev-3-{graph_id}", "disabled"),
        #  State(f"idx-eev-4-{graph_id}", "disabled"),

        #  ],
    )
    def on_plot(
        plots_dropdown_value: str,
        setup_data: Dict,
        # state_idx_eev_0: bool,
        # state_idx_eev_1: bool,
        # state_idx_eev_2: bool,
        # state_idx_eev_3: bool,
        # state_idx_eev_4: bool,
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

            setup_data = json.loads(setup_data)
            # print('setup_data: ', setup_data.keys())
            print('setup_data: ', type(setup_data))

            # data_path = Path(setup_data["data_path"])
            # setup_data = json.loads(setup_data)[0]
            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            # Load data from pickle
            data = pickle.load(
                open(setup_data["data_path"], "rb"))

            print('data: ', data.head())
            # Output arrays
            # graphs = {}
            # dataframes = {}

            # for energy_source in setup_data["energy_sources"]:
            #     print('energy_source: ', energy_source)

            # Use energy source as title

            # else:

            # ////////////////////////////////////////////////////// ERN-RL

            if "ErnRL" in setup_data["data_section"]:

                # Create plot figure
                fig = go.Figure()
                opacity = 0.8

                title = "Erneuerbaren-Richtlinie"

                # Add more info to title
                for idx in setup_data["row_index"]:
                    if idx != "Gesamt":
                        title = " <br> ".join([title, idx])

                for province in setup_data["provinces"]:

                    data_slice = data.loc[
                        IDX[tuple(setup_data["row_index"])],
                        IDX[province,
                            setup_data["years"],
                            ],
                    ].T

                    data_slice.reset_index(inplace=True, drop=True)

                    data_slice = pd.Series(
                        index=setup_data["years"],
                        data=np.array(data_slice.values).flatten()
                    )

                    data_slice = data_slice.fillna(0)

                    fig.add_trace(
                        go.Bar(
                            x=data_slice.index,
                            y=data_slice *
                            multiplicator(unit=setup_data["unit"]),
                            name=province,
                            # legendgroup=province,
                            marker_color=provinces_color_table[province],
                            opacity=opacity,
                        )
                    )

                    fig.layout = get_graph_layout(
                        title=title, unit=setup_data["unit"])

                return html.Div(
                    children=[
                        dcc.Graph(figure=fig),
                        html.Hr()
                    ]
                )

            if setup_data["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:
                # ////////////////////////////////////////////////////// NOT ERN-RL
                energy_soure_graphs = []

                for energy_source in setup_data["energy_sources"]:

                    # Create plot figure
                    fig = go.Figure()
                    opacity = 0.8

                    # Use energy source as title
                    title = energy_source

                    # Add more info to title
                    for idx in setup_data["row_index"]:
                        if idx != "Gesamt":
                            title = " <br> ".join([title, idx])

                    for province in setup_data["provinces"]:

                        print('province: ', province)
                        data_slice = data.loc[
                            IDX[tuple(setup_data["row_index"])],
                            IDX[province,
                                energy_source,
                                setup_data["years"],
                                ],
                        ].T

                        data_slice.reset_index(inplace=True, drop=True)

                        data_slice = pd.Series(
                            index=setup_data["years"],
                            data=np.array(data_slice.values).flatten()
                        )

                        data_slice = data_slice.fillna(0)

                        fig.add_trace(
                            go.Bar(
                                x=data_slice.index,
                                y=data_slice *
                                multiplicator(unit=setup_data["unit"]),
                                name=province,
                                # legendgroup=province,
                                marker_color=provinces_color_table[province],
                                opacity=opacity,
                            )
                        )

                    fig.layout = get_graph_layout(
                        title=title, unit=setup_data["unit"])

                    energy_soure_graphs.append(
                        html.Div(
                            children=[
                                dcc.Graph(figure=fig),
                                html.Hr()
                            ]
                        )
                    )

                return energy_soure_graphs
                # graphs[energy_source] = dcc.Graph(figure=fig)
                # dataframes[energy_source] = data_slice

        else:
            raise PreventUpdate

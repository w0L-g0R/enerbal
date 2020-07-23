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
            Input(f"{graph_id}-scale", "value"),
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
        scale: str,
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

            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            if not setup_data:
                raise PreventUpdate

            # Convert json argument
            setup_data = json.loads(setup_data)

            # Load data from pickle
            data = pickle.load(
                open(setup_data["data_path"], "rb"))

            print('data: ', data.head())
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

                data_slice = rescale(
                    scale=scale, setup_data=setup_data, data=data)

                print('data_slice: ', data_slice)

                for province in setup_data["provinces"]:

                    fig.add_trace(
                        go.Bar(
                            x=setup_data["years"],
                            y=np.array(data_slice.loc[
                                IDX[setup_data["row_index"]],
                                IDX[province,
                                    setup_data["years"],
                                    ],
                            ].fillna(0).values).flatten() *
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

                    data_slice = rescale(
                        scale=scale, setup_data=setup_data, data=data, energy_source=energy_source)

                    print('data_slice: ', data_slice)
                    for province in setup_data["provinces"]:
                        print('province: ', province)

                        fig.add_trace(
                            go.Bar(
                                x=setup_data["years"],
                                # Values unpacked comes as a list of lists -> flatten
                                y=np.array(data_slice.loc[
                                    IDX[setup_data["row_index"]],
                                    IDX[province,
                                        energy_source,
                                        setup_data["years"],
                                        ],
                                ].fillna(0).values).flatten() *
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
                                dcc.Graph(
                                    id=f"{graph_id}-figure",
                                    figure=fig
                                ),
                            ]
                        )
                    )

                    if len(setup_data["energy_sources"]) > 1:
                        energy_soure_graphs.append(html.Hr())

                return energy_soure_graphs
                # graphs[energy_source] = dcc.Graph(figure=fig)
                # dataframes[energy_source] = data_slice

        else:
            raise PreventUpdate


def rescale(scale: str, setup_data: Dict, data: pd.DataFrame, energy_source: str = None):

    if setup_data["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:
        data_slice = data.loc[
            IDX[setup_data["row_index"]],
            IDX[setup_data["provinces"],
                energy_source,
                setup_data["years"],
                ],
        ].T.fillna(0)

    if "ErnRL" in setup_data["data_section"]:
        data_slice = data.loc[
            IDX[setup_data["row_index"]],
            IDX[setup_data["provinces"],
                setup_data["years"],
                ],
        ].T.fillna(0)

    data_slice = data_slice.apply(pd.to_numeric)

    if scale == "Normalisiert":

        sum_per_year = data_slice.groupby(
            'YEAR').sum()

        data_slice = data_slice.groupby("YEAR").apply(
            lambda x: x / sum_per_year)

    return data_slice.T


# def rescale_res(scale: str, setup_data: Dict, data: pd.DataFrame):

#     if scale == "Normalisiert":

#         data_slice = data.loc[
#             IDX[setup_data["row_index"]],
#             IDX[setup_data["provinces"],
#                 setup_data["years"],
#                 ],
#         ].T.fillna(0)

#         data_slice = data_slice.apply(pd.to_numeric)

#         sum_per_year = data_slice.groupby(
#             'YEAR').sum()

#         data_slice = data_slice.groupby("YEAR").apply(
#             lambda x: x / sum_per_year).T

#     else:
#         data_slice = data.loc[
#             IDX[tuple(setup_data["row_index"])],
#             IDX[province,
#                 setup_data["years"],
#                 ],
#         ].T.fillna(0)

#         data_slice = data_slice.apply(pd.to_numeric)
#         data_slice.reset_index(inplace=True, drop=True)

#         data_slice = pd.Series(
#             index=setup_data["years"],
#             data=np.array(data_slice.values).flatten()
#         )

#     return data_slice

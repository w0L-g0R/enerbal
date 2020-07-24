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
from time import time
from settings import DEFAULT_CHART_CONFIG
IDX = pd.IndexSlice


def create_on_plot(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-box", "children"),

        [
            Input(f"{graph_id}-plots", "value"),
            Input(f"{graph_id}-scale", "value"),
            Input(f"{graph_id}-setup", "data"),
        ],
        # [
        # State(f"{graph_id}-setup", "data"),
        #  State(f"idx-eev-0-{graph_id}", "disabled"),
        #  State(f"idx-eev-1-{graph_id}", "disabled"),
        #  State(f"idx-eev-2-{graph_id}", "disabled"),
        #  State(f"idx-eev-3-{graph_id}", "disabled"),
        #  State(f"idx-eev-4-{graph_id}", "disabled"),

        # ],
    )
    def on_plot(
        plots_dropdown_value: str,
        scale: str,
        # trigger: Dict,
        setup: str,
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

            if not setup:
                raise PreventUpdate

            # Convert json argument
            setup = json.loads(setup)

            # Load data from pickle
            start_time = time()

            setup["data"] = pickle.load(
                open(setup["data_path"], "rb"))
            end_time = time()

            print(
                f"Pickle execution time {Path(setup['data_path']).stem}", end_time-start_time)

            if setup["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:

                graphs = create_eb_figures(
                    setup=setup, scale=scale)

            if "ErnRL" in setup["data_section"]:

                # Create plot figure
                fig = go.Figure()
                opacity = 0.8

                title = "Erneuerbaren-Richtlinie"

                # Add more info to title
                for idx in setup["row_index"]:
                    if idx != "Gesamt":
                        title = " <br> ".join([title, idx])

                setup["data"], unit = rescale(
                    scale=scale, setup=setup, data=data,)

                for province in setup["provinces"]:

                    fig.add_trace(
                        go.Bar(
                            x=setup["years"],
                            y=np.array(setup["data"].loc[
                                IDX[tuple(setup["row_index"])],
                                IDX[province,
                                    setup["years"],
                                    ],
                            ].fillna(0).values).flatten() *
                            multiplicator(unit=setup["unit"]),
                            name=province,
                            # legendgroup=province,
                            marker_color=provinces_color_table[province],
                            opacity=opacity,
                        )
                    )

                    fig.layout = get_graph_layout(
                        title=title, unit=unit)

                return html.Div(
                    children=[
                        dcc.Graph(figure=fig, config=DEFAULT_CHART_CONFIG),
                    ]
                )

            return graphs
        else:
            raise PreventUpdate


def create_eb_figures(setup: Dict, scale: str):

    graphs = []

    if "Jahre" in setup["xaxis_type"]:
        print('"Jahre": ', "Jahre")

        # /////////////////////////////////////////////////// XAXIS TYPE
        setup["xaxis"] = setup["years"]

        # /////////////////////////////////////////////////// FIGURE
        for energy_source in setup["energy_sources"]:
            print('energy_source: ', energy_source)

            # Create plot figure
            fig = go.Figure()
            opacity = 0.8

            # Use energy source as title
            title = energy_source

            # Add more info to title
            for idx in setup["row_index"]:
                if idx != "Gesamt":
                    title = " <br> ".join([title, idx])

            data_slice, unit = rescale(
                scale=scale, setup=setup, energy_source=energy_source,)

            # /////////////////////////////////////////////////// TRACES
            for province in setup["provinces"]:
                print('province: ', province)

                y_data = np.array(data_slice.loc[
                    IDX[tuple(
                        setup["row_index"])],
                    IDX[
                        province,
                        energy_source,
                        setup["years"],
                    ]
                ].T.fillna(0).values).flatten()

                # /////////////////////////////////////////////////// CHART TYPE
                fig = create_trace(fig=fig,
                                   setup=setup,
                                   y_data=y_data,
                                   province=province,
                                   opacity=opacity
                                   )

                fig.layout = get_graph_layout(
                    title=title, unit=unit)

        graphs.append(
            html.Div(
                children=[
                    dcc.Graph(
                        id=f"{setup['graph_id']}-figure",
                        figure=fig,
                        config=DEFAULT_CHART_CONFIG
                    ),
                ]
            )
        )

        if len(setup["energy_sources"]) > 1:
            graphs.append(html.Hr())

        return graphs

    # //////////////////////////////////////////////////////////////////// CASE: XAXIS TYPE BUNDESLÄNDER
    if "Bundesländer" in setup["xaxis_type"]:

        for year in setup["years"]:

            # Create plot figure
            fig = go.Figure()
            opacity = 0.8

            # Use energy source as title
            title = str(year)

            # Add more info to title
            for idx in setup["row_index"]:
                if idx != "Gesamt":
                    title = " <br> ".join([title, idx])

            data_slice, unit = rescale(
                scale=scale, setup=setup, year=year,)

            # /////////////////////////////////////////////////// TRACES
            for province in setup["provinces"]:

                print('province: ', province)
                setup["xaxis"] = [province]

                y_data = np.array(data_slice.loc[
                    IDX[tuple(
                        setup["row_index"])],
                    IDX[
                        province,
                        setup["energy_sources"],
                        year,
                    ]
                ].T.fillna(0).values).flatten()

                # /////////////////////////////////////////////////// CHART TYPE
                fig = create_trace(fig=fig,
                                   setup=setup,
                                   y_data=y_data,
                                   province=province,
                                   opacity=opacity
                                   )

            fig.layout = get_graph_layout(
                title=title, unit=unit, barmode="group")

            graphs.append(
                html.Div(
                    children=[
                        dcc.Graph(
                            id=f"{setup['graph_id']}-figure",
                            figure=fig,
                            config=DEFAULT_CHART_CONFIG
                        ),
                    ]
                )
            )

            if len(setup["energy_sources"]) > 1:
                graphs.append(html.Hr())

        return graphs


def rescale(scale: str, setup: Dict, energy_source: str = None, year: int = None):

    if setup["xaxis_type"] == "Jahre":

        if setup["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:
            data_slice = setup["data"].loc[
                IDX[setup["row_index"]],
                IDX[setup["provinces"],
                    energy_source,
                    setup["years"],
                    ],
            ].fillna(0)

        if "ErnRL" in setup["data_section"]:
            data_slice = setup["data"].loc[
                IDX[setup["row_index"]],
                IDX[setup["provinces"],
                    setup["years"],
                    ],
            ].fillna(0)

    if setup["xaxis_type"] == "Bundesländer":

        if setup["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:
            data_slice = setup["data"].loc[
                IDX[setup["row_index"]],
                IDX[setup["provinces"],
                    setup["energy_sources"],
                    year,
                    ],
            ].fillna(0)

        if "ErnRL" in setup["data_section"]:
            data_slice = setup["data"].loc[
                IDX[setup["row_index"]],
                IDX[setup["provinces"],
                    year,
                    ],
            ].fillna(0)

    if scale == "Normalisiert":

        sum_per_year = data_slice.T.groupby(
            'YEAR').sum()

        data_slice = data_slice.T.groupby("YEAR").apply(
            lambda x: x / sum_per_year
        ).T * multiplicator(
            unit=setup["unit"], normalized=True
        )

        unit = "%"

    else:

        data_slice = data_slice.apply(pd.to_numeric) * multiplicator(
            unit=setup["unit"])

        unit = setup["unit"]

    print('data_slice: ', data_slice)
    return data_slice, unit


def create_trace(fig: Dict, setup: Dict, y_data: np.array, province: str, opacity: float):

    if "Bar" in setup["chart_type"]:

        fig.add_trace(
            go.Bar(
                x=setup["xaxis"],
                # Values unpacked comes as a list of lists -> flatten
                y=y_data,
                name=province,
                # legendgroup=province,
                marker_color=provinces_color_table[province],
                opacity=opacity,
            )
        )

    if "Line" == setup["chart_type"]:

        fig.add_trace(
            go.Scatter(
                x=setup["xaxis"],
                y=y_data,
                name=province,
                # legendgroup=province,
                line_color=provinces_color_table[province],
                opacity=opacity,
            )
        )

    return fig
    # Values unpacked comes as a list of lists -> flatten
    # y=np.array(setup["data"].loc[
    #     IDX[tuple(
    #         setup["row_index"])],
    #     IDX[province,
    #         energy_source,
    #         setup["years"],
    #         ],
    # ].fillna(0).values).flatten() *
    # multiplicator(
    #     unit=setup["unit"]),

# def rescale_res(scale: str, setup: Dict, data: pd.DataFrame):

#     if scale == "Normalisiert":

#         setup["data"] = data.loc[
#             IDX[setup["row_index"]],
#             IDX[setup["provinces"],
#                 setup["years"],
#                 ],
#         ].T.fillna(0)

#         setup["data"] = setup["data"].apply(pd.to_numeric)

#         sum_per_year = setup["data"].groupby(
#             'YEAR').sum()

#         setup["data"] = setup["data"].groupby("YEAR").apply(
#             lambda x: x / sum_per_year).T

#     else:
#         setup["data"] = data.loc[
#             IDX[tuple(setup["row_index"])],
#             IDX[province,
#                 setup["years"],
#                 ],
#         ].T.fillna(0)

#         setup["data"] = setup["data"].apply(pd.to_numeric)
#         setup["data"].reset_index(inplace=True, drop=True)

#         setup["data"] = pd.Series(
#             index=setup["years"],
#             data=np.array(setup["data"].values).flatten()
#         )

#     return setup["data"]

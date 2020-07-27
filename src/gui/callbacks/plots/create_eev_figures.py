from gui.callbacks.plots.on_change_unit import change_unit

from gui.callbacks.plots.create_traces import create_traces

from settings import DEFAULT_CHART_CONFIG
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
IDX = pd.IndexSlice


def create_eev_figures(setup: Dict):

    graphs = []
    opacity = 1

    # /////////////////////////////////// CASE: XAXIS TYPE BUNDESLÄNDER
    if "Jahre" in setup["xaxis_type"]:
        print('"Jahre": ', "Jahre")

        # /////////////////////////////////////////////////// XAXIS TYPE
        setup["xaxis"] = setup["years"]

        # setup["data_absolute"]

        # /////////////////////////////////////////////////// FIGURE
        for energy_source in setup["energy_sources"]:
            print('energy_source: ', energy_source)

            # Create plot figure
            fig = go.Figure()

            # Use energy source as title
            title = energy_source

            # Add more info to title
            for idx in setup["row_index"]:
                if idx != "Gesamt":
                    title = " <br> ".join([title, idx])

            data_slice, unit = change_unit(
                scale=setup["scale"], setup=setup, energy_source=energy_source,)

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
                fig = create_traces(fig=fig,
                                    setup=setup,
                                    y_data=y_data,
                                    name=province,
                                    opacity=opacity,
                                    marker_color=provinces_color_table
                                    )

                fig.layout = get_graph_layout(
                    title=title, y_unit=unit, x_unit=setup["xaxis_type"])

            setup["figures"][title] = {}
            setup["figures"][title]["graph"] = fig
            setup["figures"][title]["data_absolute"] = fig["data"]

            graphs.append(
                html.Div(
                    children=[
                        dcc.Graph(
                            id=f"{setup['graph_id']}-figure",
                            figure=fig,
                            responsive=True,
                            config=DEFAULT_CHART_CONFIG,
                            style={
                                # "height": 320,
                                "width": "100%"},
                        ),
                    ]
                )
            )

            if len(setup["energy_sources"]) > 1:
                graphs.append(
                    html.Hr(style={"background-color": "whitesmoke"}))

            # with open(setup["graph_id"] + ".p", 'wb') as file:
            #     pickle.dump(setup, file)

            # /////////////////////////////////// CASE: XAXIS TYPE BUNDESLÄNDER
    if "Bundesländer" in setup["xaxis_type"]:
        print('"Bundesländer": ', "Bundesländer")

        for year in setup["years"]:

            # Create plot figure
            fig = go.Figure()

            # Use energy source as title
            title = str(year)

            # Add more info to title
            for idx in setup["row_index"]:
                if idx != "Gesamt":
                    title = " <br> ".join([title, idx])

            # title = ["-".join([title, energy_source]) for energy_source
            #          in setup["energy_sources"]][0]

            data_slice, unit = change_unit(
                scale=setup["scale"], setup=setup, year=year,)

            # /////////////////////////////////////////////////// TRACES
            for energy_source in setup["energy_sources"]:

                # print('province: ', province)

                setup["xaxis"] = setup["provinces"]

                y_data = np.nan_to_num(np.array(data_slice.loc[
                    IDX[tuple(
                        setup["row_index"])],
                    IDX[
                        setup["provinces"],
                        energy_source,
                        year,
                    ]
                ].T).flatten())

                # /////////////////////////////////////////////////// CHART TYPE
                fig = create_traces(fig=fig,
                                    setup=setup,
                                    y_data=y_data,
                                    name=energy_source,
                                    opacity=opacity
                                    )

                fig.layout = get_graph_layout(
                    title=title, y_unit=unit, x_unit=setup["xaxis_type"])

                setup["figures"][title] = fig

            graphs.append(
                html.Div(
                    children=[
                        dcc.Graph(
                            id=f"{setup['graph_id']}-figure",
                            figure=fig,
                            responsive=True,
                            config=DEFAULT_CHART_CONFIG,
                            style={
                                # "height": 320,
                                "width": "100%"},
                        ),
                    ]
                )
            )

            if len(setup["years"]) > 1:
                graphs.append(
                    html.Hr(style={"background-color": "whitesmoke"}))

                # with open(setup["graph_id"] + ".p", 'wb') as file:
                #     pickle.dump(setup, file)

    return graphs, setup

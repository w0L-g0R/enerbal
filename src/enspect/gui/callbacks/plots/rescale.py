import inspect
import json
import os
import pickle
from copy import deepcopy
from pathlib import Path
from time import time
from typing import Dict, List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from gui.app import app
from gui.assets.AEA_colors import provinces_color_table
from gui.layouts import get_graph_layout
from gui.utils import show_callback_context
from pandas.core.common import flatten
from settings import DEFAULT_CHART_CONFIG
from utils import multiplicator

IDX = pd.IndexSlice


def rescale(setup: Dict, new_scale: str):

    # Bucket for graphs
    graphs = []

    # Create a copy of figure dict for update
    figures = deepcopy(setup["figures"])
    # print('setup["figures"]: ', setup["figures"])

    if setup["xaxis_type"] == "Jahre":

        for title, figure in figures.items():
            print("figure: ", figure)
            # print('keys: ', figure.keys())

            if new_scale == "Normalized":
                print("NORMAL: ", figure)

                # # Assign currrent scale
                # setup["figures"]["scale"] = "Normalized"

                # If existing use it, else create
                try:
                    figure["data_normalized"].values()
                except:

                    # # Save absolute values on first transformation
                    # setup["figures"][title]["data_absolute"] = \
                    #     figure["graph"]["data_absolute"]

                    # Make a copy for transformation
                    # normalized = figure["graph"]["data"]
                    trace_data = pd.DataFrame(
                        index=setup["provinces"], columns=setup["years"]
                    )

                    # yearly_values = pd.DataFrame(
                    #     index=setup["provinces"], columns=setup["years"])

                    for trace in figure["graph"]["data"]:

                        # print('trace: ', trace)
                        # print('trace["name"]: ', trace["name"])
                        trace_data.loc[trace["name"], :] = trace["y"]  # .tolist()

                    print("trace_data: ", trace_data)
                    print("trace_data sum per year: ", trace_data.sum(axis=0))

                    for trace in figure["graph"]["data"]:

                        try:
                            trace["y"] = (
                                trace_data.loc[trace["name"], :]
                                / trace_data.sum(axis=0).T
                                * multiplicator(unit=setup["unit"], normalized=True)
                            )
                        except:
                            pass
                    # trace["y"]
                    # print('trace["y"]: ', trace["y"])

                    # # Rewrite to figure object
                    # figure["graph"]["data"] = normalized

                finally:

                    # Store as current ploting data
                    figure["data_normalized"] = deepcopy(figure["graph"]["data"])

                    # Change layout y title == unit
                    figure["graph"]["layout"]["yaxis"]["title"]["text"] = "%"

            elif new_scale == "Absolute":
                # print(type(figure))
                # print('ABS: ', figure["graph"]["data"])

                # print('figure["data_absolute"]: ', figure["data_absolute"])

                fig = go.Figure()

                for y in figure["data_absolute"]:
                    print(y)
                    if isinstance(y, str):
                        pass
                    else:
                        fig.add_traces(y)

                # dict_of_fig = dict({
                #     "data": figure["graph"]["data_absolute"],
                #     "layout": figure["graph"]["layout"]
                # })

                # fig = go.Figure(dict_of_fig)
                figure["graph"] = fig
                # print('figure["graph"]: ', figure["graph"])
                # print('figure["data_absolute"]: ', figure["data_absolute"])

                # figure["graph"]["data"] = figure["data_absolute"]

                # figure["graph"]["layout"]["yaxis"]["title"]["text"] = setup["unit"]

                # pass
                # print('figure["data_absolute"]: ', figure["data_absolute"])
                # print('figure["graph"]["data"] : ', figure["graph"]["data"])

                # print('figure["graph"]["data"]: ', figure["graph"]["data"])

                # Check if already assigned
                # try:

                #     figure["data_absolute"]
                # except:
                #     # Save absolute values on first transformation
                #     figure["data_absolute"] = figure["graph"]["data"]
                #     print('figure["data_absolute"]: ',
                #           figure["data_absolute"])
                #     print('figure["graph"]["data"]: ', figure["graph"]["data"])

                # finally:
                # If existing, write to current graph data

                # figures["scale"] = "Absolute"

                # TODO: INDEX TRANSFORMATION
                # elif new_scale == "Index":

                # # Check if already assigned
                # try:
                #     figure["data_absolute"].values()
                # except:
                #     # Save absolute values on first transformation
                #     figure["data_absolute"] = figure["graph"]
        graphs.append(
            dcc.Graph(
                # id=f"{setup['graph_id']}-figure",
                responsive=True,
                # responsive=False,
                config=DEFAULT_CHART_CONFIG,
                style={"height": "100%", "width": "100%"},
                figure=figure["graph"],
            )
        )

        if len(setup["energy_sources"]) > 1:
            graphs.append(html.Hr(style={"background-color": "whitesmoke"}))

        # Overwrite with changes
        setup["figures"] = figures

        # Save new_scale
        setup["figures"]["scale"] = new_scale

    # figure[["data_normalized"] = figure["data"]

    # else:
    #     figure["graph"]["data"] = figure["data_absolute"]
    #     figure["graph"]["layout"]["yaxis"]["title"]["text"] = setup["unit"]

    # figure.update_layout(
    #     #     xaxis=dict(
    #     #         title=figure["layout"]["axis"]["title"]["text"],
    #     #         # tickangle=0,
    #     #     ),
    #     yaxis=dict(
    #         title=figure["layout"]["yaxis"]["title"]["text"],
    #     ),

    # )

    # if setup["scale"] == "Normalized":

    #     figure["data"] = figure["data_absolute"]

    #     unit = setup["unit"]

    # if setup["xaxis_type"] == "Bundesländer":

    #     if setup["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:
    #         data_slice = setup["data"].loc[
    #             IDX[setup["row_index"]],
    #             IDX[setup["provinces"],
    #                 setup["energy_sources"],
    #                 year,
    #                 ],
    #         ].fillna(0)

    #     if "ErnRL" in setup["data_section"]:
    #         data_slice = setup["data"].loc[
    #             IDX[setup["row_index"]],
    #             IDX[setup["provinces"],
    #                 year,
    #                 ],
    #         ].fillna(0)

    #     if setup["scale"] == "Normalized":

    #         sum_per_year = data_slice.T.groupby(
    #             'BL').sum()

    #         data_slice = data_slice.T.groupby("PROV").apply(
    #             lambda x: x / sum_per_year
    #         ).T * multiplicator(
    #             unit=setup["unit"], normalized=True
    #         )

    #         unit = "%"

    #     else:

    #         data_slice = data_slice.apply(pd.to_numeric) * multiplicator(
    #             unit=setup["unit"])

    #         unit = setup["unit"]

    return graphs, setup

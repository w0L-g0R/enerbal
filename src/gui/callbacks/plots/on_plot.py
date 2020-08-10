from gui.callbacks.plots.rotate_axes import rotate_axes
from gui.callbacks.plots.rescale import rescale
from gui.callbacks.plots.create_eev_figures import create_eev_figures
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
from utils import multiplicator
import json
from gui.app import app
from gui.utils import show_callback_context
from dash import no_update
import numpy as np
from time import time

IDX = pd.IndexSlice


def create_on_plot(graph_id: str):
    @app.callback(
        # [
        Output(f"{graph_id}-box", "children"),
        # Output(f"{graph_id}-plots", "data"),
        # ],
        [Input(f"{graph_id}-update", "data"),],
        [
            # ]
            State(f"{graph_id}-setup", "data"),
            State(f"{graph_id}-scale", "value"),
            State(f"{graph_id}-unit", "value"),
            #  State(f"idx-eev-0-{graph_id}", "disabled"),
            #  State(f"idx-eev-1-{graph_id}", "disabled"),
            #  State(f"idx-eev-2-{graph_id}", "disabled"),
            #  State(f"idx-eev-3-{graph_id}", "disabled"),
            #  State(f"idx-eev-4-{graph_id}", "disabled"),
        ],
    )
    def on_plot(
        update: str,
        setup: str,
        scale: str,
        unit: str
        # trigger: Dict,
    ):

        show_callback_context(
            verbose=True,
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
        )
        # Get callback information to define the triggered input
        # ctx = callback_context
        # triggered = ctx.triggered
        # states = ctx.states
        # update_key = [*ctx.inputs.keys()]
        # print('update_key: ', update_key)
        print("update: ", update)
        # print('setup: ', setup)
        # print('setup: ', type(setup))
        print('update["type"] : ', update["type"])

        # Parse callback state to dict
        setup = json.loads(setup)

        if update["type"] == "rotate_axes":

            with open(setup["graph_id"] + ".p", "rb") as file:
                setup = pickle.load(file)

            graphs, setup = rotate_axes(setup=setup,)

        if update["type"] == "scale":

            with open(setup["graph_id"] + ".p", "rb") as file:
                setup = pickle.load(file)

            graphs, setup = rescale(setup=setup, new_scale=update["scale"])

        if update["type"] == "setup":

            # Store fetched data from data source pickle file
            setup["data"] = pickle.load(open(Path(setup["data_path"]), "rb"))

            if setup["data_section"] in ["EEV", "Sektoren", "Sektor Energie"]:

                # Load data from pickle
                start_time = time()

                graphs, setup = create_eev_figures(setup=setup)

                end_time = time()

                print(
                    f"Graph build up time {Path(setup['data_path']).stem}",
                    end_time - start_time,
                )

            del setup["data"]

        with open(setup["graph_id"] + ".p", "wb") as file:
            pickle.dump(setup, file)

        return graphs

    # else:
    #     raise PreventUpdate
    # if "ErnRL" in setup["data_section"]:

    #     # Create plot figure
    #     fig = go.Figure()
    #     opacity = 0.8

    #     title = "Erneuerbaren-Richtlinie"

    #     # Add more info to title
    #     for idx in setup["row_index"]:
    #         if idx != "Gesamt":
    #             title = " <br> ".join([title, idx])

    #     setup["data"], unit = change_unit(
    #         scale=setup["scale"], setup=setup, data=data,)

    #     for province in setup["provinces"]:

    #         fig.add_trace(
    #             go.Bar(
    #                 x=setup["years"],
    #                 y=np.array(setup["data"].loc[
    #                     IDX[tuple(setup["row_index"])],
    #                     IDX[province,
    #                         setup["years"],
    #                         ],
    #                 ].fillna(0).values).flatten() *
    #                 multiplicator(unit=setup["unit"]),
    #                 name=province,
    #                 # legendgroup=province,
    #                 marker_color=provinces_color_table[province],
    #                 opacity=opacity,
    #             )
    #         )

    #         fig.layout = get_graph_layout(
    #             title=title, unit=unit)

    #     return html.Div(
    #         children=[
    #             dcc.Graph(figure=fig, config=DEFAULT_CHART_CONFIG),
    #         ]
    #     )

    # return graphs  # , figures]

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

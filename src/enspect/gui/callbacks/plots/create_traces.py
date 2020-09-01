import inspect
import json
import os
import pickle
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


def create_traces(
    fig: Dict,
    setup: Dict,
    y_data: np.array,
    name: str,
    opacity: float,
    marker_color: Dict = None,
    orientation: str = "v",
):

    hovertemplate = "%{y:.0f}"

    try:
        marker_color = marker_color[name]
    except:
        marker_color = None

    if "Bar" in setup["chart_type"]:

        fig.add_trace(
            go.Bar(
                x=setup["xaxis"],
                # Values unpacked comes as a list of lists -> flatten
                y=y_data,
                name=name,
                orientation=orientation,
                marker_line_color="black",
                marker_line_width=0.25,
                hovertemplate=hovertemplate,
                legendgroup=name,
                marker_color=marker_color,
                opacity=opacity,
            )
        )

    if "Bar+" in setup["chart_type"]:

        fig.add_trace(
            go.Bar(
                x=setup["xaxis"],
                # Values unpacked comes as a list of lists -> flatten
                y=y_data,
                name=name,
                orientation=orientation,
                marker_line_color="black",
                marker_line_width=0.25,
                hovertemplate=hovertemplate,
                legendgroup=name,
                marker_color=marker_color,
                opacity=opacity,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=setup["xaxis"],
                # Values unpacked comes as a list of lists -> flatten
                y=y_data.sum(axis=1),
                name=name,
                orientation=orientation,
                marker_line_color="black",
                marker_line_width=0.25,
                hovertemplate=hovertemplate,
                legendgroup=name,
                marker_color=marker_color,
                opacity=opacity,
            )
        )

    if "Line" == setup["chart_type"]:

        fig.add_trace(
            go.Scatter(
                x=setup["xaxis"],
                y=y_data,
                name=name,
                hovertemplate=hovertemplate,
                # legendgroup=province,
                line_color=provinces_color_table[name],
                opacity=opacity,
            )
        )

    # fig.update
    # fig["data"]["y"]
    # print('fig["data"]["y"]: ', fig["data"]["y"])
    # try:
    #     fig.add_shape(
    #         # Line reference to the axes
    #         type="line",
    #         xref="x",
    #         yref="y",
    #         x0=0,
    #         y0=min(fig["data"]["y"]),
    #         x1=0,
    #         y1=min(fig["data"]["y"]),
    #         line=dict(
    #             color="white",
    #             width=3,
    #         ),
    #     )

    # fig.add_shape(
    #     # Line reference to the axes
    #     type="line",
    #     xref="x",
    #     yref="y",
    #     y0=0,
    #     x0=min(fig["data"]["x"]),
    #     y1=0,
    #     x1=max(fig["data"]["x"]),
    #     line=dict(
    #         color="white",
    #         width=3,
    #     ),
    # )

    return fig

import plotly.graph_objects as go
import json
import logging
import webbrowser
from pathlib import Path
from pprint import pformat
from typing import Type, TypeVar

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import callback_context
from dash.exceptions import PreventUpdate
from waitress import serve
from typing import List, Dict
from gui.app import app
import pickle
# from files.energiebilanzen.processing.eb_sheets import eb_sheets
# from settings import eb_indices
from pathlib import Path


def get_layout_horizontal_bar_graphs(unit: str, title: str, height: int = 240):

    return go.Layout(
        title=dict(
            text=title,
            y=0.96,
            x=0,
            # xanchor="left",
            # yanchor="top",
            font_size=0,
            font_family="Quicksand",
        ),
        barmode="stack",
        hoverlabel=dict(bgcolor="white", font_size=14,),
        legend=dict(
            # yanchor='top',
            # xanchor='right',
            y=-0.15,
            x=0,
            # x=-.1,
            # y=-0.1,
            font=dict(family="Oswald, sans-serif",
                      size=14, color="whitesmoke"),
            bordercolor="whitesmoke",
            borderwidth=1,
        ),
        font=dict(family="Oswald Light, sans-serif",
                  size=14, color="lightblue"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # autosize=True,
        height=height,
        margin=dict(l=12, r=12, t=12, b=12, pad=24),
        showlegend=True,
        legend_orientation="h",
        template="plotly_dark",
        xaxis=dict(
            dtick=1,
            tickangle=35,
            showticklabels=True,
            # type: 'category',
            ticks="outside",
            tickcolor="black",
            ticklen=10,
            ticksuffix=" " + unit,
            showticksuffix="all",
            # domain=[0, 0.7]
            zeroline=True,
        ),
    )


def multiplicator(unit: str):

    if unit == "GWh":
        multiplicator = 0.27778

    if unit == "PJ":
        multiplicator = 0.001

    if unit == "TJ":
        multiplicator = 1

    return multiplicator
# def get_layout_with_datetime(unit: str, title: str, height: int = 360):

#     return go.Layout(
#         # title=dict(text=title, y=0.98, x=0.5,
#         #            xanchor="center", yanchor="top"),
#         # title=title,
#         barmode="stack",
#         # hoverlabel=dict(bgcolor="white", font_size=14,
#         #                 font_family="Quicksand"),
#         # legend=dict(
#         #     # yanchor='bottom',
#         #     # xanchor="center",
#         #     y=-0.18,
#         #     x=0.5,
#         #     # x=-.1,
#         #     # y=-0.1,
#         #     font=dict(family="Arial, sans-serif",
#         #               size=12, color="black"),
#         #     # bordercolor="whitesmoke",
#         #     # borderwidth=1,
#         # ),
#         # font=dict(family="Arial, sans-serif",
#         #           size=12, color="black"),
#         # paper_bgcolor="black",
#         # plot_bgcolor="black",
#         width=432,
#         # autosize=True,
#         height=440,
#         # margin=dict(l=48, r=48, t=24, b=0, pad=0),
#         # margin=dict(autoexpan),
#         showlegend=True,
#         legend_orientation="h",
#         template="plotly_white",
#         yaxis=dict(
#             ticks="outside",
#             # tickcolor="black",
#             ticklen=10,
#             # ticksuffix=" " + unit,
#             showticksuffix="all",
#             # domain=[0, 0.7]
#             zeroline=True,
#         ),
#         xaxis=dict(
#             # ticks="outside",
#             # tickcolor="black",
#             # ticklen=10,
#             # ticksuffix=" " + unit,
#             # showticksuffix="all",
#             # domain=[0, 0.7]
#             zeroline=True,
#             # zeroline_color="black",
#         ),
#     )


def get_graph_layout(unit: str, title: str):

    return go.Layout(
        title=dict(
            text=title,
            y=0.92,
            x=0,
            xanchor="center",
            # yanchor="top",
            font_size=12,
            font_family="Quicksand",
        ),
        barmode="stack",
        showlegend=True,
        legend=dict(x=-0.1, y=-0.32),
        legend_orientation="h",
        template="plotly_white",
        margin=dict(l=12, r=24, t=24, b=0),
        width=496,
        height=400,
        yaxis_title=unit,

        xaxis=dict(
            dtick=1,
            tickangle=90,
            showticklabels=True,
            # type: 'category',
            # ticks="outside",
            # tickcolor="black",
            # ticklen=10,
            # ticksuffix=" " + unit,
            # showticksuffix="all",
            # domain=[0, 0.7]
            zeroline=True,
        ),
        yaxis=dict(
            ticks="outside",
            tickcolor="lightgrey",
            ticklen=5,
            # ticksuffix=" " + unit,
            # showticksuffix="all",
            # domain=[0, 0.7]
            zeroline=True,
        ),
    )

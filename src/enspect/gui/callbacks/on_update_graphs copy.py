import inspect
import os
import pickle
from pprint import pprint
from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_table.Format import Format
from gui.app import app
from gui.layouts import get_graph_layout
from gui.utils import show_callback_context
from settings import DEFAULT_CHART_CONFIG

IDX = pd.IndexSlice


def create_on_update(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-box", "children"),
        [
            Input(f"{graph_id}-plots", "data"),
            Input(f"{graph_id}-axes", "data"),
        ],
        # [
        # State(f"{graph_id}-unit", "value"),
        # ]
    )
    def on_update(
        is_plot_data,
        flip_axes,
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
            triggered_value = triggered[0]["value"]

            if "graph-A" in triggered_prop_id:
                graph_id = "graph-A"

            if "graph-B" in triggered_prop_id:
                graph_id = "graph-B"

            setup = pickle.load(open(graph_id + ".p", "rb"))

            graphs = []
            # print('setup: ', setup)
            # print('figures: ', figures)

            # pprint(data)
            if is_plot_data == "True":

                for title, figure in setup["figures"].items():

                    graphs.append(
                        dcc.Graph(
                            # id=f"{setup['graph_id']}-figure",
                            responsive=True,
                            # responsive=False,
                            config=DEFAULT_CHART_CONFIG,
                            style={"height": "100%", "width": "100%"},
                            figure=figure,
                        )
                    )

                    graphs.append(
                        html.Hr(style={"background-color": "lightblue"}),
                    )
            else:
                data = figure["data"]
                layout = figure["layout"]

                # graphs.append(
                #     html.Hr(style={"background-color": "lightblue"}),
                # )

                for trace in data:
                    trace["x"], trace["y"] = trace["y"], trace["x"]

                    trace["orientation"] = "h"
                    trace["hovertemplate"] = "%{x: .0f}"

                    # df = pd.DataFrame(index=trace["x"], data=trace["y"])

                    # fig.layout = figures_layout

                    dict_of_fig = dict({"data": data, "layout": layout})

                    fig = go.Figure(dict_of_fig)
                    # pprint(fig)

                    fig.update_layout(
                        xaxis=dict(
                            title=setup["unit"],
                            # dtick=1,
                            tickangle=0,
                            showticklabels=True,
                            # zeroline=True,
                            showgrid=True,
                            gridwidth=0.5,
                            gridcolor="#444444",
                            # zerolinewidth=3,
                            # zerolinecolor='red',
                            autorange=True,
                        ),
                        yaxis=dict(
                            title=setup["xaxis_type"],
                            showgrid=True,
                            gridwidth=0.5,
                            gridcolor="#444444",
                            autorange=True,
                            categoryorder="array",
                            categoryarray=[
                                x for _, x in sorted(zip(trace["y"], trace["x"]))
                            ]
                            # ticks="outside",
                            # tickcolor="#444444",
                            # ticklen=2,
                            # zeroline=True,
                            # zerolinewidth=3,
                            # zerolinecolor='red',
                            # titlefont=dict(
                            #     family='Oswald, sans-serif',
                            #     size=14,
                            #     color='lightgrey'
                            # ),
                        ),
                        legend=dict(x=0, y=-0.24),
                    )

                    fig.add_shape(
                        # Line reference to the axes
                        type="line",
                        xref="x",
                        yref="y",
                        x0=0,
                        y0=min(trace["y"]),
                        x1=0,
                        y1=max(trace["y"]),
                        line=dict(
                            color="white",
                            width=3,
                        ),
                    )

                    # fig.add_shape(
                    #     # Line reference to the axes
                    #     type="line",
                    #     xref="x",
                    #     yref="y",
                    #     y0=0,
                    #     x0=min(trace["x"]),
                    #     y1=0,
                    #     x1=max(trace["x"]),
                    #     line=dict(
                    #         color="white",
                    #         width=3,
                    #     ),
                    # )
                    # fig.update_layout(
                    #     yaxis=dict(
                    #         title=setup["xaxis_type"],
                    #         # autorange="reversed",
                    #     ),
                    #     xaxis=dict(
                    #         title=setup["unit"],
                    #         tickangle=0,
                    #         showticklabels=True,
                    #         # zeroline=True,
                    #     ),
                    #     legend=dict(x=0, y=-0.24),
                    # )

                    fig.update_xaxes(tickmode="auto")

                    graphs.append(
                        dcc.Graph(
                            # id=f"{setup['graph_id']}-figure",
                            responsive=True,
                            # responsive=False,
                            config=DEFAULT_CHART_CONFIG,
                            style={"height": "100%", "width": "100%"},
                            figure=fig,
                        )
                        #     ]
                        # )
                    )
                    graphs.append(
                        html.Hr(style={"background-color": "lightblue"}),
                    )

            return graphs
        else:
            raise PreventUpdate

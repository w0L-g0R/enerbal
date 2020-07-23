# import inspect
# import os
# from typing import List
# import dash_html_components as html

# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import pandas as pd
# import plotly.graph_objects as go
# from dash import callback_context
# from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate

# from gui.app import app
# from gui.utils import show_callback_context
# from dash import no_update
# import dash_table
# import pickle
# import dash_table.FormatTemplate as FormatTemplate
# from gui.assets.AEA_colors import provinces_color_table, provinces_color_table_rgba

# from dash_table.Format import Format
# IDX = pd.IndexSlice


# def callback_return_on_change_scale(
#     updates_scale: str = no_update,
#     absolute_values: List = no_update,
# ):
#     return [
#         updates_scale,
#         absolute_values
#     ]
# # _________________________________________________________________________
# # ///////////////////////////////////////////////////////////////// DISPATCH EL


# def create_on_change_scale(graph_id: str):
#     @ app.callback(
#         [
#             Output(f"{graph_id}-updates-scale", "data"),
#             Output(f"{graph_id}-absolute-values", "data"),

#         ],
#         [
#             Input(f"{graph_id}-scale", "value"),
#         ],
#         [
#             State(f"{graph_id}-figures", "data"),
#             State(f"{graph_id}-absolute-values", "data"),
#         ]
#     )
#     def on_change_scale(
#         scale,
#         figure,
#         absolute_values
#     ):

#         # Log callback information
#         show_callback_context(
#             func_name=inspect.stack()[0][3],
#             file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
#             verbose=False,
#         )

#         # Get callback information to define the triggered input
#         ctx = callback_context
#         triggered = ctx.triggered

#         if triggered:

#             print('figure["data"]: ', figure["data"])

#             figures

#             absolute_values = no_update

#             if not absolute_values:

#                 absolute_values = [trace["y"] for trace in figure["data"]]

#             if scale == "Normalisiert":

#                 traces = []
#                 index = figure["data"][0]["x"]

#                 # Fetch figure data
#                 for trace in figure["data"]:
#                     s = pd.Series(
#                         index=index, data=trace["y"], name=trace["name"])
#                     traces.append(s)
#                 df = pd.concat(traces, axis=1).T

#                 # Normalize
#                 df = df.apply(lambda x: x/x.sum()).T

#                 # Write back to figure data
#                 for trace in figure["data"]:
#                     trace["y"] = df[trace["name"]] * 100

#                 # Change yaxis title
#                 figure["layout"]["yaxis"]["title"] = {'text': '%'}

#                 return callback_return_on_change_scale(
#                     updates_scale=figure,
#                     absolute_values=absolute_values,
#                 )
#             else:
#                 return []
#         else:
#             raise PreventUpdate

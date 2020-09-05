# import inspect
# import os
# from typing import List

# import pandas as pd
# from dash import callback_context, no_update
# from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate

# from gui.app import app
# from gui.utils import show_callback_context
# from pandas import IndexSlice as IDX


# def create_on_switch_axes(graph_id: str):
#     @app.callback(
#         Output(f"{graph_id}-axes", "data"),
#         [
#             Input(f"{graph_id}-axes", "value"),
#         ],
#     )
#     def on_switch_axes(
#         switch: str,
#     ):

#         show_callback_context(
#             verbose=True,
#             func_name=inspect.stack()[0][3],
#             file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
#         )
#         # Get callback information to define the triggered input
#         ctx = callback_context
#         triggered = ctx.triggered
#         states = ctx.states
#         inputs = ctx.inputs

#         if triggered:

#             triggered_prop_id = triggered[0]["prop_id"]
#             triggered_value = triggered[0]["value"]

#             return "Switch axis"
#         else:
#             raise PreventUpdate

import inspect
import os
from typing import List

import pandas as pd
from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from gui.app import app
from gui.utils import show_callback_context

IDX = pd.IndexSlice


def create_on_select_index_year(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-scale", "marks"),
        [
            Input(f"{graph_id}-index-year", "value"),
        ],
        [State(f"active-years", "value"), ]
    )
    def on_select_index_year(
        index_year: str,
        active_years: List
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

            active_years = [1987 + int(x) for x in active_years]

            if int(index_year) >= min(active_years) and int(index_year) <= max(active_years):

                print('active_years: ', active_years)
                print('min(active_years): ', min(active_years))
                print('max(active_years):: ', max(active_years))
                print('int(index_year): ', int(index_year))

                return {
                    {
                        0: {"label": "Absolute", "style": range_slider_style},
                        1: {"label": "Normalized", "style": range_slider_style},
                        2: {"label": "Index", "style": range_slider_style},
                    }
                }

            else:

                return no_update
        else:
            raise PreventUpdate

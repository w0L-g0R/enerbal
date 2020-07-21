import inspect
import os
from pathlib import Path
from typing import List

from dash import no_update
from dash.dependencies import Input, Output, State

from gui.app import app
from gui.utils import show_callback_context
from gui.components.views.setup import eev


def create_on_graph_tab_change(graph_id: str):
    @app.callback(
        Output(f"content-{graph_id}", "children"),
        [Input(f"tabs-{graph_id}", "active_tab")],
    )
    def on_graph_tab_change(active_tab):

        show_callback_context(
            verbose=True,
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
        )

        if active_tab == f"tab-eb-{graph_id}":

            # return "Hi"

            if "graph-A" in active_tab:
                return eev["graph-A"]

            elif "graph-B" in active_tab:
                return eev["graph-B"]

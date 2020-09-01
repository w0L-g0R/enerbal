import inspect
import os

from dash.dependencies import Input, Output
from gui.app import app
from gui.utils import show_callback_context
from gui.views.setup.view import eb_setup_views


def create_on_graph_tab_change(graph_id: str):
    @app.callback(
        Output(f"{graph_id}-content", "children"),
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
                return eb_setup_views["graph-A"]

            elif "graph-B" in active_tab:
                return eb_setup_views["graph-B"]

            elif "graph-C" in active_tab:
                return eb_setup_views["graph-C"]

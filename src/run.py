import logging
from logger.setup import setup_logging


import inspect
import os
from pathlib import Path
from typing import List

from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from gui.utils import run_server
from gui.index import layout
from gui.components.controller import register_callbacks
from gui.components.views.setup import eev

from gui.app import app

# /////////////////////////////////////////////////////////// PRE-RUNTIME SETUP

# from components.setups.callbacks.on_graph_tab_change import create_on_graph_tab_change

from gui.components.controller import register_callbacks

# Assign layout created in index.py to app object
app.layout = layout

register_callbacks()


# def create_on_graph_tab_change(graph_id: str):
#     @app.callback(
#         Output(f"content-{graph_id}", "children"),
#         [Input(f"tabs-{graph_id}", "active_tab")],
#     )
#     def on_graph_tab_change(active_tab):

#         # show_callback_context(
#         #     verbose=True,
#         #     func_name=inspect.stack()[0][3],
#         #     file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
#         # )

#         if active_tab == f"tab-1-{graph_id}":

#             # return "Hi"

#             if "graph-A" in active_tab:
#                 return eev["graph-A"]

#             elif "graph-B" in active_tab:
#                 return eev["graph-B"]

#         elif "tab-2" in active_tab:
#             return


# Assign URL and port info
connection = dict(url="127.0.0.1", port="8050")

# _____________________________________________________________________________
# ////////////////////////////////////////////////////////////////// AT-RUNTIME

if __name__ == "__main__":

    print("\n________________________________________________")
    print("|                                               |")
    print("|                    RELOAD                     |")
    print("|_______________________________________________|\n")

    setup_logging(
        console_log_actived=True,
        console_log_filter=None,
        console_out_level=logging.DEBUG,
    )

    logging.getLogger().debug("Hi")
    # Turn off werkzeug logger (in order to surpess "task queue" log messages etc.)
    # waitress_queue_logger = logging.getLogger("waitress.queue")
    # waitress_queue_logger.disabled = True

    # _____________________________________________________________________________
    # ////////////////////////////////////////////////////// AUTOMATIC BROWSER OPEN

    # Opens a new tab or window on your local browser
    # open_webbrowser(connection=connection, new=0)

    # _____________________________________________________________________________
    # ////////////////////////////////////////////////////////////////// RUN SERVER

    # Run a server instance in devolpement mode
    # run_server(app=app, connection=connection, development=False)

    # Run a server instance in production mode
    run_server(app=app, connection=connection, development=True)

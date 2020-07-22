import logging
from logger.setup import setup_logging
import inspect
import os
from pathlib import Path
from typing import List

from gui.utils import run_server
from gui.index import layout
from gui.components.controller import register_callbacks

from gui.app import app

# /////////////////////////////////////////////////////////// PRE-RUNTIME SETUP

# from components.setups.callbacks.on_graph_tab_change import create_on_graph_tab_change

from gui.components.controller import register_callbacks

# Assign layout created in index.py to app object
app.layout = layout

register_callbacks()

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

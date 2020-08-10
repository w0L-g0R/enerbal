import logging
import pickle
import webbrowser

# from files.energiebilanzen.processing.eb_sheets import eb_sheets
from pathlib import Path
from pprint import pformat
from typing import List, Type, TypeVar

from dash import callback_context
from waitress import serve

from settings import file_paths

# _____________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// TYPES

dash_component = Type[TypeVar("component")]


def run_server(
    app: dash_component, connection: dict, development: bool = True, debug: bool = True
):

    if development:

        app.run_server(
            debug=True if debug else False,
            # dev_tools_props_check=False,
            # dev_tools_ui=False,
            dev_tools_hot_reload=True,
            port=connection["port"],
            host=connection["url"],
        )

    else:
        serve(app.server, host=connection["url"], port=connection["port"])

    return


# ___________________________________________________________________________
# /////////////////////////////////////////////////////////////////// BROWSER


def open_webbrowser(connection: dict, new: int):
    webbrowser.get().open(
        "".join(("http://", connection["url"], ":", connection["port"])),
        new=new,
        autoraise=True,
    )
    return


# _____________________________________________________________________________
# //////////////////////////////////////////////////////////// CALLBACK CONTEXT


def show_callback_context(func_name: str, file_name: str, verbose: bool = False):

    # Switch to debug in order to surpress console output
    logging.getLogger().debug(f"{func_name} @ {file_name}")
    logging.getLogger().warning(f"{func_name} @ {file_name}")

    ctx_msg = {
        "inputs": callback_context.inputs,
        "states": callback_context.states,
        "triggered": callback_context.triggered,
    }

    if verbose:
        logging.getLogger().debug("\n" + pformat(ctx_msg))

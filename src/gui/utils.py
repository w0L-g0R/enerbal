import logging
import pickle
import webbrowser
# from files.energiebilanzen.processing.eb_sheets import eb_sheets
# from settings import eb_indices
from pathlib import Path
from pprint import pformat
from typing import List, Type, TypeVar

from dash import callback_context
from waitress import serve

# _____________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// TYPES

dash_component = Type[TypeVar("component")]


def multiplicator(unit: str, normalized: bool = False):
    print('unit: ', unit)

    if unit == "GWh":
        multiplicator = 0.27778

        if normalized:
            multiplicator = 1/multiplicator * 100

    if unit == "TWh":
        multiplicator = 0.00027778

        if normalized:
            multiplicator = 1/multiplicator * 100

    if unit == "PJ":
        multiplicator = 0.001

        if normalized:
            multiplicator = multiplicator * 1e8

    if unit in ["TJ", "MW", "h", "%"]:
        multiplicator = 1

        if normalized:
            multiplicator = multiplicator * 100
    return multiplicator


def get_eb_indices():
    eb_indices_path = Path("src/files/energiebilanzen/pickles/indices.p")
    return pickle.load(open(eb_indices_path, "rb"))


def create_eev_energy_source_options(energy_sources: List):

    # energy_sources = list(reversed(energy_sources[69:])) + energy_sources[:69]
    energy_sources = energy_sources[::-1]

    return [{"label": x, "value": x} for enum, x in enumerate(energy_sources)]


def create_row_indices(_type: str):

    eb_indices = get_eb_indices()

    print('_type: ', _type)
    if _type == "EEV":
        indices = eb_indices["MIDX_EEV"]

    if _type == "Sektoren":
        indices = eb_indices["IDX_EEV_SECTORS"].iloc[2:]

    if _type == "Sektor Energie":
        indices = eb_indices["IDX_SECTOR_ENERGY"].iloc[2:]

    if _type == "ErnRL":
        indices = eb_indices["MIDX_RENEWABLES"].loc[:, :2]
        print('indices: ', indices)

    midx = []

    for enum, col in enumerate(indices.columns):
        _indices = list(indices[col].unique())
        _indices = [{"label": x, "value": x}
                    for enum, x in enumerate(_indices)]
        midx.append(_indices)

    return midx


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

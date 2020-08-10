import dash_html_components as html
import inspect
import os
from typing import List, Dict

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
import json

from gui.app import app
from gui.utils import show_callback_context
from settings import provinces
from dash import no_update
import pickle
from pathlib import Path
from files.energiebilanzen.processing.eb_sheets import eb_sheets
from settings import chart_type_options, scale_options

IDX = pd.IndexSlice
# _________________________________________________________________________
# ///////////////////////////////////////////////////////////////// DISPATCH EL


# def callback_return_on_setup(
#     # options: List,
#     setup: Dict,
# ):

#     return [
#         # options,
#         setup
#     ]


def create_on_setup(graph_id: str):
    @app.callback(
        [Output(f"{graph_id}-setup", "data"),],
        [Input(f"{graph_id}-btn-setup", "n_clicks"),],
        [  # TAB
            State(f"tabs-{graph_id}", "active_tab"),
            # DATA
            State(f"{graph_id}-data-section", "value"),
            # TIME
            State(f"active-years", "value"),
            # PROVINCE ACTIVE
            State(f"checklist-AT", "value",),
            State(f"checklist-Bgd", "value",),
            State(f"checklist-Ktn", "value",),
            State(f"checklist-Noe", "value",),
            State(f"checklist-Ooe", "value",),
            State(f"checklist-Sbg", "value",),
            State(f"checklist-Stk", "value",),
            State(f"checklist-Tir", "value",),
            State(f"checklist-Vbg", "value",),
            State(f"checklist-Wie", "value",),
            # PROVINCE PLOT NAME
            State(f"plot-name-AT", "value",),
            State(f"plot-name-Bgd", "value",),
            State(f"plot-name-Ktn", "value",),
            State(f"plot-name-Noe", "value",),
            State(f"plot-name-Ooe", "value",),
            State(f"plot-name-Sbg", "value",),
            State(f"plot-name-Stk", "value",),
            State(f"plot-name-Tir", "value",),
            State(f"plot-name-Vbg", "value",),
            State(f"plot-name-Wie", "value",),
            # TITLE
            # State(f"{graph_id}-title", "value",),
            # SCALE
            State(f"{graph_id}-scale", "value",),
            # INDEX YEAR
            State(f"{graph_id}-index-year", "value",),
            # AGGREGATE
            State(f"{graph_id}-aggregate-eb", "value",),
            # ENERGY SOURCE
            State(f"{graph_id}-energy-sources", "value"),
            # UNIT
            State(f"{graph_id}-unit", "value"),
            # State(f"{graph_id}-chart-type", "value"),
            State(f"{graph_id}-xaxis-type", "value"),
            # CHART OPTIONS
            State(f"{graph_id}-options-1", "value"),
            State(f"{graph_id}-options-2", "value"),
            # INDEX EEV
            State(f"idx-eev-0-{graph_id}", "value"),
            State(f"idx-eev-1-{graph_id}", "value"),
            State(f"idx-eev-2-{graph_id}", "value"),
            State(f"idx-eev-3-{graph_id}", "value"),
            State(f"idx-eev-4-{graph_id}", "value"),
            # INDEX SECTORS
            State(f"idx-sectors-0-{graph_id}", "value"),
            # INDEX SECTOR ENERGY
            State(f"idx-sector-energy-0-{graph_id}", "value"),
            # INDEX SECTOR ENERGY
            State(f"idx-res-0-{graph_id}", "value"),
            State(f"idx-res-1-{graph_id}", "value"),
            State(f"idx-res-2-{graph_id}", "value"),
        ],
    )
    def on_setup(
        # BUTTON
        n_clicks,
        # ACTIVE TAB
        active_tab,
        # DATA TYPE
        data_section,
        # TIME
        years,
        # PROVINCE ACTIVE
        checkbox_AT,
        checkbox_Bgd,
        checkbox_Ktn,
        checkbox_Noe,
        checkbox_Ooe,
        checkbox_Sbg,
        checkbox_Stk,
        checkbox_Tir,
        checkbox_Vbg,
        checkbox_Wie,
        # PROVINCE PLOT NAME
        plotname_AT,
        plotname_Bgd,
        plotname_Ktn,
        plotname_Noe,
        plotname_Ooe,
        plotname_Sbg,
        plotname_Stk,
        plotname_Tir,
        plotname_Vbg,
        plotname_Wie,
        # TITLE
        # title,
        # SCALE
        scale,
        # INDEX YEAR
        index_year,
        # AGGREGATE
        aggregate_eb,
        # ENERGY SOURCE
        energy_sources,
        # UNIT
        unit,
        # CHART OPTIONS
        # chart_type,
        xaxis_type,
        chart_options_1,
        chart_options_2,
        # INDEX EEV
        idx_0_EEV,
        idx_1_EEV,
        idx_2_EEV,
        idx_3_EEV,
        idx_4_EEV,
        # INDEX SECTORS
        idx_0_SECTORS,
        # INDEX SECTOR ENERGY
        idx_0_SECTOR_ENERGY,
        # INDEX RENEWABLES
        idx_0_RES,
        idx_1_RES,
        idx_2_RES,
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
        states = ctx.states
        inputs = ctx.inputs

        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            triggered_value = triggered[0]["value"]

            setup = {}
            setup["figures"] = {}

            # =========================================================== GENERAL

            if "graph-A" in triggered_prop_id:
                setup["graph_id"] = "graph-A"

            if "graph-B" in triggered_prop_id:
                setup["graph_id"] = "graph-B"

            if "graph-C" in triggered_prop_id:
                setup["graph_id"] = "graph-C"

            setup["data_section"] = data_section
            # setup["title"] = title
            setup["scale"] = scale_options[scale[0]]["label"]
            setup["index_year"] = index_year
            setup["aggregate_eb"] = aggregate_eb
            setup["energy_sources"] = energy_sources
            setup["rotate"] = chart_options_1 if chart_options_1 == "Rotate" else []
            setup["for_each"] = chart_options_1 if chart_options_1 == "Foreach" else []
            setup["unit"] = unit
            setup["chart_type"] = chart_type_options["Bar"]["label"]
            setup["xaxis_type"] = "Jahre" if xaxis_type == [0] else "Bundesländer"
            # setup["chart_options_2"] = chart_options_2

            # =========================================================== YEARS

            setup["years"] = sorted([1987 + x for x in years])

            # ======================================================= PROVINCES
            provinces_selection = {
                "AT": checkbox_AT,
                "Bgd": checkbox_Bgd,
                "Ktn": checkbox_Ktn,
                "Noe": checkbox_Noe,
                "Ooe": checkbox_Ooe,
                "Sbg": checkbox_Sbg,
                "Stk": checkbox_Stk,
                "Tir": checkbox_Tir,
                "Vbg": checkbox_Vbg,
                "Wie": checkbox_Wie,
            }

            provinces_abbreviations = {
                "AT": plotname_AT,
                "Bgd": plotname_Bgd,
                "Ktn": plotname_Ktn,
                "Noe": plotname_Noe,
                "Ooe": plotname_Ooe,
                "Sbg": plotname_Sbg,
                "Stk": plotname_Stk,
                "Tir": plotname_Tir,
                "Vbg": plotname_Vbg,
                "Wie": plotname_Wie,
            }

            provinces = provinces.copy()

            # Only take the marked provinces
            for province, check in provinces_selection.items():

                if check is None or check == [0] or check == []:
                    provinces.remove(province)

            setup["provinces"] = provinces

            if data_section == "EEV":

                row_index = [idx_0_EEV, idx_1_EEV, idx_2_EEV, idx_3_EEV, idx_4_EEV]

                if idx_0_EEV in ["Umwandlungseinsatz", "Umwandlungsausstoß"]:

                    for enum, idx in enumerate(row_index[1:]):

                        if idx == "Gesamt":
                            row_index = row_index[: enum + 2] + list(
                                map(lambda x: "Gesamt", row_index[enum + 2 :])
                            )

                else:

                    row_index = ["Gesamt" for x in row_index[1:]]
                    row_index.insert(0, idx_0_EEV)

                # Used to slice eev_data
                setup["row_index"] = row_index

                setup["data_path"] = Path(
                    "src/files/energiebilanzen/pickles/eev_df.p"
                ).__str__()

            if data_section == "Sektoren":

                setup["row_index"] = [idx_0_SECTORS]
                setup["data_path"] = Path(
                    "src/files/energiebilanzen/pickles/sectors_df.p"
                ).__str__()

            if data_section == "Sektor Energie":

                setup["row_index"] = [idx_0_SECTOR_ENERGY]
                setup["data_path"] = Path(
                    "src/files/energiebilanzen/pickles/sector_energy_df.p"
                ).__str__()

            if data_section == "ErnRL":

                row_index = [idx_0_RES, idx_1_RES, idx_2_RES]

                if idx_1_EEV not in [
                    "Energetischer Endverbrauch Erneuerbare (TJ)",
                    "Elektrische Energie Produktion erneuerbar (TJ)",
                ]:
                    row_index = list(map(lambda x: "Gesamt", row_index))

                for enum, idx in enumerate(row_index):
                    if idx == "Gesamt":
                        row_index = list(map(lambda x: "Gesamt", row_index[enum + 1 :]))

                setup["row_index"] = (idx_0_RES, idx_1_RES, idx_2_RES)
                setup["data_path"] = Path(
                    "src/files/energiebilanzen/pickles/renewables_df.p"
                ).__str__()

            # Add options
            # options = [{"label": x, "value": x}
            #            for x in energy_sources]

            # with open(setup["graph_id"] + ".p", 'wb') as file:
            #     pickle.dump(setup, file)

            return [json.dumps(setup)]

            # return callback_return_on_setup(
            #     # options=options,
            #     setup=json.dumps(setup)
            # )

        else:
            PreventUpdate

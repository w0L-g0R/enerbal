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
from gui.assets.AEA_colors import provinces_color_table
from gui.utils import show_callback_context, multiplicator
from gui.layouts import get_graph_layout
from settings import provinces_names, eev_indices, energy_sources_options
from dash import no_update
import pickle
from pathlib import Path
from files.energiebilanzen.processing.eb_sheets import eb_sheets

IDX = pd.IndexSlice
# _________________________________________________________________________
# ///////////////////////////////////////////////////////////////// DISPATCH EL


def callback_return_on_setup(
    options: List,
    graphs: object,
    data: Dict,
):

    return [options, graphs, data]  # data]
    # table
    # data.to_json(date_format='iso', orient='split')


def create_on_setup(graph_id: str):
    @app.callback(
        [
            Output(f"{graph_id}-plots", "options"),
            Output(f"{graph_id}-figures", "data"),
            Output(f"{graph_id}-data", "data"),
        ],
        [
            Input(f"{graph_id}-setup", "data"),
        ],
        [
            # DATA
            State(f"data-section-{graph_id}", "value"),
            # State("eev-data", "data"),
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
            State(f"title-{graph_id}", "value",),
            # SCALE
            State(f"scale-{graph_id}", "value",),
            # INDEX YEAR
            State(f"index-year-{graph_id}", "value",),
            # AGGREGATE
            State(f"aggregate-{graph_id}", "value",),
            # ENERGY SOURCE
            State(f"energy-sources-{graph_id}", "value"),
            # SOURCE INDEX
            State(f"source-index-{graph_id}", "value"),

            # UNIT
            State(f"unit-{graph_id}", "value"),

            # CHART OPTIONS
            State(f"chart-type-{graph_id}", "value"),
            State(f"bar-chart-options-1-{graph_id}", "value"),
            State(f"bar-chart-options-2-{graph_id}", "value"),

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
        title,
        # SCALE
        scale,
        # INDEX YEAR
        index_year,
        # AGGREGATE
        aggregate,
        # ENERGY SOURCE
        energy_sources,
        # SOURCE INDEX
        source_index,

        # UNIT
        unit,
        # CHART OPTIONS
        chart_type,
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

            # Check which graph has been fired
            # if "graph-A" in triggered_prop_id:
            # _graph = "graph-A"
            _title = title
            print('_title: ', _title)
            _scale = scale
            print('_scale: ', _scale)
            _index_year = index_year
            print('_index_year: ', _index_year)
            _aggregate = aggregate
            print('_aggregate: ', _aggregate)
            _energy_sources = energy_sources
            print('_energy_sources: ', _energy_sources)
            _source_index = source_index
            print('_source_index: ', _source_index)
            _data_section = data_section
            print('_data_section: ', _data_section)
            _unit = unit

            _chart_type = chart_type
            _chart_options_1 = chart_type
            _chart_options_2 = chart_type

            # =========================================================== YEARS
            _years = [1987 + x for x in years]
            print('_years: ', _years)

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

            _provinces = provinces_names.copy()

            # Only take the marked provinces
            for province, check in provinces_selection.items():

                if check is None or check == [0] or check == []:
                    _provinces.remove(province)
                    print('_provinces: ', _provinces)

            if _data_section == "EEV":

                # ================================================ GET EEV DATA

                # Used to slice eev_data
                _row_index = (idx_0_EEV, idx_1_EEV,
                              idx_2_EEV, idx_3_EEV, idx_4_EEV)
                print('_row_index: ', _row_index)

                data_path = Path("src/files/energiebilanzen/pickles/eev_df.p")
                # temp = Path(f"src/gui/eev_{graph_id}.p")

            if _data_section == "Sektoren":

                data_path = Path(
                    "src/files/energiebilanzen/pickles/sectors_df.p")

                _row_index = idx_0_SECTORS

            if _data_section == "Sektor Energie":

                data_path = Path(
                    "src/files/energiebilanzen/pickles/renewables_df.p")

                _row_index = idx_0_SECTOR_ENERGY

            if _data_section == "ErnRL":

                data_path = Path(
                    "src/files/energiebilanzen/pickles/renewables_df.p")

                _row_index = idx_0_RES, idx_1_RES, idx_2_RES

            # Store the currents plot index
            # midx = {
            #     "row_index": _row_index,
            #     "col_index": [_provinces, _energy_sources, sorted(_years)],
            # }

            # Load data from pickle
            data = pickle.load(
                open(data_path, "rb"))

            data = data.loc[
                IDX[_row_index[:]],
                # _row_index,
                IDX[_provinces,
                    _energy_sources,
                    sorted(_years)],
            ]
            # Output arrays
            graphs = {}
            dataframes = {}

            for energy_source in _energy_sources:
                print('energy_source: ', energy_source)

                # Create plot figure
                fig = go.Figure()
                opacity = 1

                # Use energy source as title
                _title = energy_source

                # Add more info to title
                for idx in _row_index:
                    if idx != "Gesamt":
                        _title = "\n".join([_title, idx])

                for province in _provinces:
                    print('province: ', province)

                    data_slice = data.loc[
                        IDX[:],
                        # IDX[_row_index],
                        IDX[province,
                            energy_source,
                            :],
                        # sorted(_years)],
                    ]

                    data_slice = data_slice.fillna(0)

                    fig.add_trace(
                        go.Bar(
                            x=_years,
                            y=data_slice * multiplicator(unit=_unit),
                            name=province,
                            legendgroup=province,
                            marker_color=provinces_color_table[province],
                            opacity=opacity,
                        )
                    )

                fig.layout = get_graph_layout(
                    title=_title, unit=_unit)

                graphs[energy_source] = dcc.Graph(figure=fig)
                dataframes[energy_source] = data_slice

            # Add options
            options = [{"label": x, "value": x}
                       for x in energy_sources]

            return callback_on_setup_graph(
                options=options,
                data=dataframes,
                graphs=graphs
            )

        else:
            PreventUpdate
            # {"label": "EEV", "value": "EEV", },
            # {"label": "Sektoren", "value": "Sektoren", },
            # {"label": "Sektor Energie", "value": "Sektor Energie", },
            # {"label": "ErnRL", "value": "ErnRL", },

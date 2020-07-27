import inspect
import os
from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

from gui.app import app
from gui.assets.AEA_colors import provinces_color_table
from gui.utils import get_graph_layout, show_callback_context
from settings import provinces_names, eev_indices, energy_sources_options
from dash import no_update
import pickle
from pathlib import Path
from files.energiebilanzen.processing.eb_sheets import eb_sheets

IDX = pd.IndexSlice
# _________________________________________________________________________
# ///////////////////////////////////////////////////////////////// DISPATCH EL


def callback_on_update_eev_graph(graph: object, table: object):

    return [
        graph,
        no_update
        # table
        # data.to_json(date_format='iso', orient='split')
    ]


def create_on_update_eev_graph(graph_id: str):
    @app.callback(
        [
            Output(f"box-{graph_id}", "children"),
            Output(f"{graph_id}-setup-table", "data"),
        ],
        [Input(f"{graph_id}-clicked-eev-update", "data"),
         ],
        [
            # DATA
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
            State(f"title-graph-A", "value",),
            State(f"title-graph-B", "value",),
            # SCALE
            State(f"scale-graph-A", "value",),
            State(f"scale-graph-B", "value",),
            # INDEX YEAR
            State(f"index-year-graph-A", "value",),
            State(f"index-year-graph-B", "value",),
            # AGGREGATE
            State(f"aggregate-graph-A", "value",),
            State(f"aggregate-graph-B", "value",),
            # ENERGY SOURCE
            State(f"energy-sources-graph-A", "value"),
            State(f"energy-sources-graph-B", "value"),
            # SOURCE INDEX
            State(f"source-index-graph-A", "value"),
            State(f"source-index-graph-B", "value"),

            # DATA TYPE
            State(f"data-section-graph-A", "value"),
            State(f"data-section-graph-B", "value"),

            # UNIT
            State(f"unit-graph-A", "value"),
            State(f"unit-graph-B", "value"),

            # INDEX
            State(f"idx-eev-0-graph-A", "value"),
            State(f"idx-eev-0-graph-B", "value"),
            State(f"idx-eev-1-graph-A", "value"),
            State(f"idx-eev-1-graph-B", "value"),
            State(f"idx-eev-2-graph-A", "value"),
            State(f"idx-eev-2-graph-B", "value"),
            State(f"idx-eev-3-graph-A", "value"),
            State(f"idx-eev-3-graph-B", "value"),
            State(f"idx-eev-4-graph-A", "value"),
            State(f"idx-eev-4-graph-B", "value"),

            # CHART OPTIONS
            State(f"chart-type-graph-A", "value"),
            State(f"chart-type-graph-B", "value"),
            State(f"bar-chart-options-1-graph-A", "value"),
            State(f"bar-chart-options-1-graph-B", "value"),
            State(f"bar-chart-options-2-graph-A", "value"),
            State(f"bar-chart-options-2-graph-B", "value"),
        ],
    )
    def on_update_eev(
        # BUTTON
        n_clicks,
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
        title_graph_A,
        title_graph_B,
        # SCALE
        scale_graph_A,
        scale_graph_B,
        # INDEX YEAR
        index_year_graph_A,
        index_year_graph_B,
        # AGGREGATE
        aggregate_graph_A,
        aggregate_graph_B,
        # ENERGY SOURCE
        energy_sources_graph_A,
        energy_sources_graph_B,
        # SOURCE INDEX
        source_index_graph_A,
        source_index_graph_B,
        # DATA TYPE
        data_type_graph_A,
        data_type_graph_B,
        # UNIT
        unit_graph_A,
        unit_graph_B,
        # INDEX
        idx_0_graph_A,
        idx_0_graph_B,
        idx_1_graph_A,
        idx_1_graph_B,
        idx_2_graph_A,
        idx_2_graph_B,
        idx_3_graph_A,
        idx_3_graph_B,
        idx_4_graph_A,
        idx_4_graph_B,
        # CHART OPTIONS
        chart_type_graph_A,
        chart_type_graph_B,
        chart_options_1_graph_A,
        chart_options_1_graph_B,
        chart_options_2_graph_A,
        chart_options_2_graph_B,
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

            if "graph-A" in triggered_prop_id:
                _graph = "graph-A"
                _title = title_graph_A
                _scale = scale_graph_A
                _index_year = index_year_graph_A
                _aggregate = aggregate_graph_A
                _energy_sources = energy_sources_graph_A
                _source_index = source_index_graph_A
                _data_type = data_type_graph_A
                _unit = unit_graph_A
                _idx_0 = idx_0_graph_A
                _idx_1 = idx_1_graph_A
                _idx_2 = idx_2_graph_A
                _idx_3 = idx_3_graph_A
                _idx_4 = idx_4_graph_A
                _chart_type = chart_type_graph_A
                _chart_options_1 = chart_type_graph_A
                _chart_options_2 = chart_type_graph_A

            elif "graph-B" in triggered_prop_id:
                _graph = "graph-B"
                _title = title_graph_B
                _scale = scale_graph_B
                _index_year = index_year_graph_B
                _aggregate = aggregate_graph_B
                _energy_sources = energy_sources_graph_B
                _source_index = source_index_graph_B
                _data_type = data_type_graph_B
                _unit = unit_graph_B
                _idx_0 = idx_0_graph_B
                _idx_1 = idx_1_graph_B
                _idx_2 = idx_2_graph_B
                _idx_3 = idx_3_graph_B
                _idx_4 = idx_4_graph_B
                _chart_type = chart_type_graph_B
                _chart_options_1 = chart_type_graph_B
                _chart_options_2 = chart_type_graph_B

            # =========================================================== YEARS
            _years = [1987 + x for x in years]

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

            for province, check in provinces_selection.items():

                if check is None or check == [0] or check == []:
                    _provinces.remove(province)

            # ======================================================= GET DATA

            # if eev_data is None:
            eev_data = pickle.load(
                open(Path("src/files/energiebilanzen/pickles/eev_df.p"), "rb"))

            _row_index = [_idx_0, _idx_1, _idx_2, _idx_3, _idx_4]

            _title = _energy_sources[0]

            for idx in _row_index:
                if idx != "Gesamt":
                    _title = "-".join([_title, idx])

            # _table_info =
            midx = {
                "row_index": IDX[_idx_0, _idx_1, _idx_2, _idx_3, _idx_4],
                "col_index": IDX[_provinces, _energy_sources, sorted(_years)],
            }
            eev_slice = eev_data.loc[
                midx["row_index"], midx["col_index"],
            ]

            # print('data.index: ', eev_slice.index)
            pickle.dump(eev_slice, open("eev_data.p", "wb")
                        )

            # Create area plot figure
            fig = go.Figure()
            opacity = 1

            multiplicator = 1

            if _unit == "GWh":
                multiplicator = 0.27778

            if _unit == "PJ":
                multiplicator = 0.001

            # print('_bundeslaender: ', _bundeslaender)
            # POSITIVE: Add columns for stack with positive values
            for province in _provinces:
                print('province: ', province)

                data = eev_data.loc[
                    IDX[_row_index], IDX[[province], _energy_sources, _years]
                ] * multiplicator
                # print('data: ', data.values)
                fig.add_trace(
                    go.Bar(
                        x=_years,
                        # y=[1 for x in _years],
                        y=data.values[0],
                        name=province,
                        legendgroup=province,
                        marker_color=provinces_color_table[province],
                        opacity=opacity,
                        offsetgroup=province,
                        # stackgroup="positive",
                        # line=dict(width=0),
                        # line_shape="vh",
                    )
                )

            fig.layout = get_graph_layout(
                title=_title, unit=_unit)

            graph = dcc.Graph(figure=fig)

            return[graph, midx]

        else:
            PreventUpdate

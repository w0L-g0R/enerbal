import dash_daq as daq
from typing import List
from settings import aggregates_eb
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from settings import (
    eev_indices,
    renewables_indices,
    sector_energy_indices,
    sectors_indices,
    units
)
from gui.assets.styles import range_slider_style, label_style
from settings import chart_type_options


from gui.views.setup.components import (
    get_index_select,
    get_chart_type,
    get_xaxis_type,
    get_chart_options,
    get_scale,
    get_index_year,
    get_aggregate_eb,
    get_energy_source,
    get_energy_source_index,
    get_data_section,
    get_energy_unit,
)


# def create_sectors_graph_view(graph_id: str):

#     return dbc.Container(
#         # fluid=True,
#         children=[
#             title_row(graph_id=graph_id)[0],
#             html.Br(),
#             # html.Hr(style={"width": "100%", "margin-bottom": 8}),
#             #
#             data_scale_row(graph_id=graph_id)[0],
#             html.Br(),
#             # html.Hr(style={"width": "100%", "margin-bottom": 8}),
#             #
#             chart_options_row(graph_id=graph_id)[0],
#             # seventh_row(graph_id=graph_id)[0],
#             html.Br(style={"margin-bottom": 12}),
#             # html.Hr(style={"width": "100%", "margin-bottom": 8}),
#             #
#             eb_aggregate_row(graph_id=graph_id)[0],
#             eb_data_type_row(graph_id=graph_id)[0],
#             sectors_idx_rows(graph_id=graph_id)[0],

#         ]
#     )

# ////////////////////////////////////////////////////////////////////// ROWS


# def title_row(graph_id: str):
#     return dbc.Row(
#         no_gutters=True,
#         children=[dbc.Col(width=12, children=[
#             get_title(graph_id=graph_id)],), ],
#     )


def data_scale_row(graph_id: str):
    return dbc.Row(
        justify="center",
        align="center",
        no_gutters=True,
        children=[
            # dbc.Col(width=2,
            #         # style={"margin": 4},
            #         children=[
            #             get_chart_options(graph_id=graph_id)],),
            dbc.Col(
                # style={"margin-left": , "margin-right": -32},
                width=8, children=[
                    get_scale(graph_id=graph_id)],),

            dbc.Col(
                width=2,
                # style={
                #     "margin-left": 32,
                #     # "margin-right": -64,
                # },
                children=[
                    get_index_year(graph_id=graph_id)],),
        ],
    )


def eb_aggregate_row(graph_id: str):
    return dbc.Row(
        style={"font-family": "Quicksand, sans-serif"},
        no_gutters=True,
        children=[
            dbc.Col(width=12, children=[get_aggregate_eb(graph_id=graph_id)],),
            dbc.Col(width=12, children=[
                get_energy_source(graph_id=graph_id)],),
            # dbc.Col(
            # width=2, children=[get_energy_source_index(graph_id=graph_id)],
            # ),
        ],
    )


def eb_data_section_row(graph_id: str):
    return dbc.Row(
        justify="center",
        # align="center",
        children=[
                dbc.Col(width=10, children=[
                        get_data_section(graph_id=graph_id)],),
                dbc.Col(width=2, children=[
                        get_energy_unit(graph_id=graph_id)],),
        ],
    )


def sectors_idx_rows(graph_id: str):
    return dbc.Row(
        no_gutters=True,
        # style={"margin-top": 24},
        children=[
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"sectors-0-{graph_id}", name="IDX 0", disabled=False, value="Eisen- und Stahlerzeugung", options=sectors_indices[0])],
            ),
        ],
    )


def sector_energy_idx_rows(graph_id: str):
    return dbc.Row(
        no_gutters=True,
        # style={"margin-top": 24},
        children=[
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"sector-energy-0-{graph_id}", name="IDX 0", disabled=False, value="Gewinnung von Erdöl und Erdgas", options=sector_energy_indices[0])],
            ),
        ],
    )


def renewables_idx_rows(graph_id: str):
    return dbc.Row(
        no_gutters=True,
        # style={"margin-top": 24},
        children=[
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"res-0-{graph_id}", name="IDX 0", options=renewables_indices[0], value="Anrechenbarer Erneuerbare (TJ)", disabled=False)],
            ),
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"res-1-{graph_id}", name="IDX 1", options=renewables_indices[1], value="Gesamt")],
            ),
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"res-2-{graph_id}", name="IDX 2", options=renewables_indices[2], value="Gesamt")],
            ),
        ],
    )


def eev_idx_rows(graph_id: str):
    return dbc.Row(
        no_gutters=True,
        # style={"margin-top": 24},
        children=[
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"eev-0-{graph_id}", name="IDX 0", options=eev_indices[0], value="Bruttoinlandsverbrauch", disabled=False)],
            ),
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"eev-1-{graph_id}", name="IDX 1", options=eev_indices[1], value="Gesamt")],
            ),
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"eev-2-{graph_id}", name="IDX 2", options=eev_indices[2], value="Gesamt")],
            ),
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"eev-3-{graph_id}", name="IDX 3", options=eev_indices[3], value="Gesamt")],
            ),
            dbc.Col(
                width=12,
                children=[get_index_select(
                    graph_id=f"eev-4-{graph_id}", name="IDX 4", options=eev_indices[4], value="Gesamt")],
            ),
        ],
    )


def chart_type_row(graph_id: str):
    return dbc.Row(
        # style={"margin-top": 24},
        no_gutters=True,
        children=[
            dbc.Col(
                width=12,
                children=[
                    dbc.Label("Chart type",
                              style=label_style),
                    get_chart_type(graph_id=graph_id)
                ],
            ),
        ],
    )


# def chart_options_row(graph_id: str):
#     return dbc.Row(
#         # style={"margin-top": 24},
#         no_gutters=True,
#         children=[
#             dbc.Col(
#                 width=12,
#                 children=[
#                     # dbc.Label("Chart type",
#                     #           style=label_style),
#                     get_chart_options(graph_id=graph_id)
#                 ],
#             ),
#         ],
#     )


def xaxis_type_row(graph_id: str):
    return dbc.Row(
        # style={"margin-top": 24},
        no_gutters=True,
        children=[
            dbc.Col(
                width=12,
                children=[
                    get_xaxis_type(graph_id=graph_id)
                ],
            ),
        ],
    )

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from typing import List
from files.energiebilanzen.processing.eb_sheets import eb_sheets

from settings import energy_sources_options, eev_indices, sectors_indices, sector_energy_indices, renewables_indices

range_slider_style = {"font-family": "Roboto, sans-serif",
                      "font-size": 12, "color": "black", }
label_style = {"font-family": "Roboto, sans-serif",
               "font-size": 14, "color": "cadetblue"}


def create_eb_graph_view(graph_id: str):

    return dbc.Container(
        # fluid=True,
        children=[
            title_row(graph_id=graph_id),
            html.Br(),
            # html.Hr(style={"width": "100%", "margin-bottom": 8}),
            #

            # html.Hr(style={"width": "100%", "margin-bottom": 8}),
            #
            chart_options_row(graph_id=graph_id),
            # seventh_row(graph_id=graph_id)[0],
            html.Br(style={"margin-bottom": 12}),
            # html.Hr(style={"width": "100%", "margin-bottom": 8}),
            #
            eb_aggregate_row(graph_id=graph_id),
            eb_data_section_row(graph_id=graph_id),

            html.Div(
                id=f"idx-eev-{graph_id}",
                # style={"display": "none"},
                children=eev_idx_rows(graph_id=graph_id),
            ),
            html.Div(
                id=f"idx-sectors-{graph_id}",
                style={"display": "none"},
                children=sectors_idx_rows(graph_id=graph_id),
            ),
            html.Div(
                id=f"idx-sector-energy-{graph_id}",
                style={"display": "none"},
                children=sector_energy_idx_rows(graph_id=graph_id),
            ),
            html.Div(
                id=f"idx-renewables-{graph_id}",
                style={"display": "none"},
                children=renewables_idx_rows(graph_id=graph_id),
            ),

        ]
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


def title_row(graph_id: str):
    return dbc.Row(
        no_gutters=True,
        children=[dbc.Col(width=12, children=[
            get_title(graph_id=graph_id)],), ],
    )


def data_scale_row(graph_id: str):
    return dbc.Row(
        no_gutters=True,
        children=[
            dbc.Col(width=10, children=[
                get_scale(graph_id=graph_id)],),
            dbc.Col(width=2, children=[
                get_index_year(graph_id=graph_id)],),
        ],
    )


def eb_aggregate_row(graph_id: str):
    return dbc.Row(
        no_gutters=True,
        children=[
            dbc.Col(width=2, children=[get_aggregate(graph_id=graph_id)],),
            dbc.Col(width=8, children=[
                get_energy_source(graph_id=graph_id)],),
            dbc.Col(
                width=2, children=[get_energy_source_index(graph_id=graph_id)],
            ),
        ],
    )


def eb_data_section_row(graph_id: str):
    return dbc.Row(
        justify="center",
        align="center",
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
                    graph_id=f"eev-0-{graph_id}", name="IDX 0", options=eev_indices[0], value="Energetischer Endverbrauch", disabled=False)],
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


def chart_options_row(graph_id: str):
    return dbc.Row(
        # style={"margin-top": 24},
        no_gutters=True,
        children=[
            dbc.Col(
                width=12,
                children=[
                    dbc.Label("Chart type options",
                              style=label_style),
                    get_chart_options(graph_id=graph_id)
                ],
            ),
        ],
    )


# def seventh_row(graph_id: str):
#     return (
#         dbc.Row(
#             style={"margin-top": 24},
#             no_gutters=True,
#             children=[
#                 dbc.Col(
#                     width=12,
#                     children=[
#                         get_bar_chart_options(graph_id=graph_id)
#                     ],
#                 ),
#             ],
#         ),
#     )


# ////////////////////////////////////////////////////////////////////// GETTER


def get_title(graph_id: str):
    return dbc.FormGroup(
        [
            dbc.Label(children="Titel", style=label_style),
            dbc.Input(
                placeholder="Title goes here...", type="text", id=f"title-{graph_id}", value=f"{graph_id}"
            ),
        ]
    )


def get_scale(graph_id: str):
    return dbc.FormGroup(
        children=[
            dbc.Label("Datenskalierung", style=label_style),
            dbc.RadioItems(
                style={"margin-top": 24, "margin-right": 4, "font-size": 14},
                options=[
                    {"label": "Absolut", "value": 1, },
                    {"label": "Normalisiert", "value": 2, },
                    {"label": "Index Jahr", "value": 3, "disabled": True},
                ],
                value=1,
                id=f"{graph_id}-scale",
                inline=True,
            ),
        ]
    )


def get_index_year(graph_id: str):
    return dbc.FormGroup(
        [
            dbc.Label("Index Jahr", style=label_style),
            dbc.Input(placeholder="", type="text",
                      id=f"{graph_id}-index-year",),
        ]
    )


def get_aggregate(graph_id: str):
    return dbc.FormGroup(
        style={"margin-right": 4},
        children=[
            dbc.Label("Aggregat", style=label_style),
            dbc.Select(
                id=f"aggregate-{graph_id}",
                options=[
                    {"label": "Option 1", "value": "1"},
                    {"label": "Option 2", "value": "2"},
                ],
            ),
        ],
    )


def get_energy_source(graph_id: str):

    return dbc.FormGroup(
        style={"margin-right": 4},
        children=[
            dbc.Label("Energieträger", style=label_style),
            # dbc.Select(
            #     id=f"energy-sources-{graph_id}",
            #     options=energy_sources_options,
            #     value=[0]
            # ),
            dcc.Dropdown(
                id=f"energy-sources-{graph_id}",
                options=energy_sources_options,
                value=["Gesamtenergiebilanz"],
                multi=True,
            ),
        ],
    )


def get_energy_source_index(graph_id: str):

    return dbc.FormGroup(
        [
            dbc.Label("Nummer", style=label_style),
            dbc.Input(placeholder="", type="number",
                      id=f"source-index-{graph_id}",),
        ]
    )


def get_data_section(graph_id: str):

    return dbc.FormGroup(
        children=[
            dbc.Label("Datenbereich", style=label_style),
            dbc.RadioItems(
                style={"padding-top": 6, "margin-right": 4},
                options=[
                    {"label": "EEV", "value": "EEV", },
                    {"label": "Sektoren", "value": "Sektoren", },
                    {"label": "Sektor Energie", "value": "Sektor Energie", },
                    {"label": "ErnRL", "value": "ErnRL", },
                ],
                value="EEV",
                id=f"data-section-{graph_id}",
                inline=True,
            ),
        ]
    )


def get_energy_unit(graph_id: str):

    return dbc.FormGroup(
        style={"margin-left": -24},
        children=[
            dbc.Label("Einheit", style=label_style),
            dbc.Select(
                id=f"unit-{graph_id}",
                options=[
                    {"label": "GWh", "value": "GWh"},
                    {"label": "TJ", "value": "TJ"},
                    {"label": "PJ", "value": "PJ"},
                ],
                value="TJ"
            ),
        ],
    )


def get_index_select(graph_id: str, name: str, value: str = None, options: List = None, disabled: bool = True):
    return dbc.InputGroup(
        [
            dbc.InputGroupAddon(name, addon_type="prepend", style=label_style),
            dbc.Select(
                id=f"idx-{graph_id}",
                options=options,
                value=value,
                disabled=disabled
            ),
        ],
        className="mb-3",
    )


def get_chart_options(graph_id: str):
    return dbc.Row(children=[

        dbc.Col(
            width=3,
            children=[
                dcc.RangeSlider(
                    id=f"chart-type-{graph_id}",
                    min=0,
                    max=1,
                    step=1,
                    marks={
                        0: {"label": "Line", "style": range_slider_style},
                        1: {"label": "Bar", "style": range_slider_style},
                    },
                    value=[1],
                    vertical=True,
                    verticalHeight=100,
                ),
            ]),


        dbc.Col(
            width=3,
            children=[
                dcc.RangeSlider(
                    id=f"xaxis-type-{graph_id}",
                    min=0,
                    max=1,
                    step=1,
                    marks={
                        0: {"label": "x=Länder", "style": range_slider_style},
                        1: {"label": "x=Jahre", "style": range_slider_style},
                    },
                    value=[1],
                    vertical=True,
                    verticalHeight=100,
                ),
            ]),
        dbc.Col(
            width=3,
            children=[
                dcc.RangeSlider(
                    id=f"bar-chart-options-1-{graph_id}",
                    min=0,
                    max=1,
                    step=1,
                    marks={
                        0: {"label": "Horizontal", "style": range_slider_style},
                        1: {"label": "Vertikal", "style": range_slider_style},
                    },
                    value=[1],
                    vertical=True,
                    verticalHeight=100,
                ),
            ]),
        dbc.Col(
            width=3,

            children=[
                dcc.RangeSlider(
                    id=f"bar-chart-options-2-{graph_id}",
                    min=0,
                    max=1,
                    step=1,
                    marks={
                        0: {"label": "Gruppiert", "style": range_slider_style},
                        1: {"label": "Gestapelt", "style": range_slider_style},
                    },
                    value=[1],
                    vertical=True,
                    verticalHeight=100,
                )
            ])

    ])


energy_balances_views = {}
energy_balances_views["graph-A"] = create_eb_graph_view(graph_id="graph-A")
energy_balances_views["graph-B"] = create_eb_graph_view(graph_id="graph-B")

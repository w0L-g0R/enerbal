import dash_daq as daq
from typing import List
from settings import aggregates_eb
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from gui.assets.styles import range_slider_style, label_style
from settings import chart_type_options, units
from utils import create_eev_energy_source_options
from files.energiebilanzen.processing.get_eb_sheets import eb_sheets

energy_sources_options = create_eev_energy_source_options(
    energy_sources=eb_sheets)

# ////////////////////////////////////////////////////////////////////// GETTER

# def get_title(graph_id: str):
#     return dbc.FormGroup(
#         [
#             dbc.Label(children="Titel", style=label_style),
#             dbc.Input(
#                 placeholder="Title goes here...", type="text", id=f"{graph_id}-title", value=f"{graph_id}"
#             ),
#         ]
#     )


def get_chart_options(graph_id: str):

    return html.Div(
        children=[
            dbc.Row(
                justify="center",
                align="center",
                no_gutters=True,
                children=[
                    dbc.Col(
                        width=6,
                        children=[
                            dbc.Label(
                                "Stack",
                                style={
                                    # "margin-top": 12,
                                    "margin-left": 12,
                                    "font-family": "Quicksand, sans-serif",
                                    "font-size": 16,
                                    "color": "cadetblue",
                                },
                            ),
                            daq.ToggleSwitch(
                                id=f"{graph_id}-switch-stack",
                                style={"margin-top": 12, "margin-left": 24},
                                theme="dark",
                                color="deepskyblue",
                                size=32,
                                vertical=True,
                            ),
                        ],
                    ),
                    dbc.Col(
                        width=6,
                        children=[
                            dbc.Label(
                                "Flip",
                                style={
                                    # "margin-top": 12,
                                    "margin-left": 22,
                                    "font-family": "Quicksand, sans-serif",
                                    "font-size": 16,
                                    "color": "cadetblue",
                                },
                            ),
                            daq.ToggleSwitch(
                                id=f"{graph_id}-switch-axes",
                                style={"margin-top": 12, "margin-left": 24},
                                theme="dark",
                                color="deepskyblue",
                                size=32,
                                vertical=True,
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )


def get_scale(graph_id: str):
    return dbc.FormGroup(
        children=[
            dbc.Label(
                "Scale",
                style={
                    "margin-left": -12,
                    "margin-bottom": 12,
                    "font-family": "Quicksand, sans-serif",
                    "font-size": 16,
                    "color": "lightblue",
                },
            ),
            dcc.RangeSlider(
                id=f"{graph_id}-scale",
                min=0,
                max=2,
                step=1,
                marks={
                    0: {"label": "Absolute", "style": range_slider_style},
                    1: {"label": "Normalized", "style": range_slider_style},
                    2: {"label": "Index", "style": range_slider_style},
                },
                value=[0],
                # vertical=True,
                # verticalHeight=100,
            ),
        ]
    )


def get_index_year(graph_id: str):
    return dbc.FormGroup(
        [
            dbc.Label(
                "Year",
                style={
                    "margin-left": 4,
                    "margin-bottom": 12,
                    "font-family": "Quicksand, sans-serif",
                    "font-size": 16,
                    "color": "lightblue",
                },
            ),
            dbc.Input(
                placeholder="",
                style={
                    "text-align": "center",
                    "font-family": "Quicksand, sans-serif",
                    "font-size": 14,
                },  # type="text"
                value=2000,
                id=f"{graph_id}-index-year",
            ),
        ]
    )


def get_aggregate_eb(graph_id: str):
    return dbc.FormGroup(
        # style={"margin-right": 4},
        children=[
            dbc.Label("Aggregat", style=label_style),
            dcc.Dropdown(
                style={"color": "black"},
                id=f"{graph_id}-aggregate-eb",
                options=aggregates_eb,
            ),
        ],
    )


# def get_aggregate_2(graph_id: str):
#     return dbc.FormGroup(
#         style={"margin-right": 4},
#         children=[
#             dbc.Label("Aggregat 2", style=label_style),
#             dcc.Dropdown(
#                 id=f"{graph_id}-aggregate-2",
#                 options=aggregates
#             ),
#         ],
#     )


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
                style={"color": "black"},
                id=f"{graph_id}-energy-sources",
                options=energy_sources_options,
                value=["Gesamtenergiebilanz"],
                multi=True,
            ),
        ],
    )


def get_energy_source_index(graph_id: str):

    return dbc.FormGroup(
        children=[
            dbc.Label("Nummer", style=label_style),
            dbc.Input(placeholder="", type="number",
                      id=f"{graph_id}-source-index",),
        ]
    )


def get_data_section(graph_id: str):

    return dbc.FormGroup(
        children=[
            dbc.Label("Datenbereich", style=label_style),
            dbc.RadioItems(
                style={"font-size": 14},
                options=[
                    {"label": "EEV", "value": "EEV", },
                    {"label": "Sektoren", "value": "Sektoren", },
                    {"label": "Sektor Energie", "value": "Sektor Energie", },
                    {"label": "ErnRL", "value": "ErnRL", },
                ],
                value="EEV",
                id=f"{graph_id}-data-section",
                inline=True,
            ),
        ]
    )


def get_energy_unit(graph_id: str):

    return dbc.FormGroup(
        style={"margin-left": -24},
        children=[
            dbc.Label("Unit", style=label_style),
            dbc.Select(id=f"{graph_id}-unit", options=units, value="TJ"),
        ],
    )


def get_index_select(
    graph_id: str,
    name: str,
    value: str = None,
    options: List = None,
    disabled: bool = True,
):
    return dbc.InputGroup(
        [
            dbc.InputGroupAddon(name, addon_type="prepend", style=label_style),
            dbc.Select(
                id=f"idx-{graph_id}", options=options, value=value, disabled=disabled
            ),
        ],
        className="mb-3",
    )


def get_chart_type(graph_id: str):
    return dbc.Row(
        children=[
            dbc.Col(
                width=12,
                children=[
                    dcc.RangeSlider(
                        id=f"{graph_id}-chart-type",
                        min=0,
                        max=4,
                        step=1,
                        marks={
                            0: {"label": "Bar", "style": range_slider_style},
                            1: {"label": "Line", "style": range_slider_style},
                            2: {"label": "Scatter", "style": range_slider_style},
                            3: {"label": "Pie", "style": range_slider_style},
                            4: {"label": "Map", "style": range_slider_style},
                        },
                        value=[0],
                    ),
                ],
            ),
        ]
    )


def get_xaxis_type(graph_id: str):
    return html.Div(
        children=[
            dbc.Row(
                children=[dbc.Col(children=dbc.Label(
                    "X-Achse", style=label_style),), ]
            ),
            dbc.Row(
                style={
                    "border": "1px solid lightblue",
                    "border-radius": 4,
                    "height": 64,
                },
                justify="center",
                align="center",
                no_gutters=True,
                children=[
                    # dbc.Col(
                    #     children=dbc.Label("X-Achse", style=label_style),
                    # ),
                    dbc.Col(
                        width=8,
                        children=html.Div(
                            style={
                                # "background-color": "whitesmoke",
                                "margin-top": 12
                            },
                            children=[
                                dcc.RangeSlider(
                                    id=f"{graph_id}-xaxis-type",
                                    min=0,
                                    max=1,
                                    step=1,
                                    marks={
                                        0: {
                                            "label": "Jahre",
                                            "style": range_slider_style,
                                        },
                                        1: {
                                            "label": "Bundesländer",
                                            "style": range_slider_style,
                                        },
                                    },
                                    value=[0],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ]
    )

    # dbc.FormGroup(
    #     [
    #         dbc.Label("Stack"),

    #         dbc.Label("Flip"),
    #         daq.ToggleSwitch(
    #             vertical=True
    #         )
    #     ]
    # )


# def get_chart_options(graph_id: str):
#     return dbc.Row(children=[

#         dbc.Col(
#             width=3,
#             children=[
#                 dcc.RangeSlider(
#                     id=f"chart-type-{graph_id}",
#                     min=0,
#                     max=1,
#                     step=1,
#                     marks={
#                         0: {"label": "Line", "style": range_slider_style},
#                         1: {"label": "Bar", "style": range_slider_style},
#                     },
#                     value=[1],
#                     vertical=True,
#                     verticalHeight=100,
#                 ),
#             ]),


#         dbc.Col(
#             width=3,
#             children=[
#                 dcc.RangeSlider(
#                     id=f"xaxis-type-{graph_id}",
#                     min=0,
#                     max=1,
#                     step=1,
#                     marks={
#                         0: {"label": "x=Länder", "style": range_slider_style},
#                         1: {"label": "x=Jahre", "style": range_slider_style},
#                     },
#                     value=[1],
#                     vertical=True,
#                     verticalHeight=100,
#                 ),
#             ]),
#         dbc.Col(
#             width=3,
#             children=[
#                 dcc.RangeSlider(
#                     id=f"bar-chart-options-1-{graph_id}",
#                     min=0,
#                     max=1,
#                     step=1,
#                     marks={
#                         0: {"label": "Horizontal", "style": range_slider_style},
#                         1: {"label": "Vertikal", "style": range_slider_style},
#                     },
#                     value=[1],
#                     vertical=True,
#                     verticalHeight=100,
#                 ),
#             ]),
#         dbc.Col(
#             width=3,

#             children=[
#                 dcc.RangeSlider(
#                     id=f"bar-chart-options-2-{graph_id}",
#                     min=0,
#                     max=1,
#                     step=1,
#                     marks={
#                         0: {"label": "Gruppiert", "style": range_slider_style},
#                         1: {"label": "Gestapelt", "style": range_slider_style},
#                     },
#                     value=[1],
#                     vertical=True,
#                     verticalHeight=100,
#                 )
#             ])

#     ])

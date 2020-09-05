import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from gui.assets.styles import buttons_style_chart_types, label_style, range_slider_style
from gui.views.setup.components import get_index_year, get_scale
from gui.views.setup.rows import chart_type_row, data_scale_row
from settings import DEFAULT_CHART_CONFIG


def create_control_box_layout(graph_id: str):

    return dbc.Card(
        style={"width": "100%", "margin-top": -12, "border": "0px black solid"},
        children=[
            dbc.CardBody(
                style={"width": "100%"},
                id=f"{graph_id}-control",
                children=[
                    dbc.CardFooter(
                        style={
                            "margin-left": 4,
                            "margin-right": 4,
                            "margin-bottom": 1,
                            "border": "0px lightblue solid",
                            "border-radius": 0,
                        },
                        children=[
                            dbc.Button(
                                "SETUP",
                                color="info",
                                id=f"{graph_id}-btn-setup",
                                block=True,
                            ),
                        ],
                    ),
                    dbc.CardFooter(
                        style={
                            "border": "0px lightblue solid",
                            "border-radius": 0,
                            "margin-right": 4,
                            "margin-left": 4,
                            "margin-bottom": 1,
                        },
                        children=[
                            dbc.Row(
                                justify="center",
                                no_gutters=True,
                                children=[
                                    dbc.Col(
                                        style={
                                            "margin-left": 20,
                                            "margin-top": 12,
                                            "margin-right": 32,
                                        },
                                        width=8,
                                        children=[get_scale(graph_id=graph_id)],
                                    ),
                                    dbc.Col(
                                        width=2,
                                        style={"margin-right": 12, "margin-top": 12,},
                                        children=[get_index_year(graph_id=graph_id)],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dbc.CardFooter(
                        style={
                            "margin-left": 4,
                            "margin-right": 4,
                            "margin-bottom": 1,
                            "border": "0px lightblue solid",
                            "border-radius": 0,
                        },
                        children=[
                            dbc.Label(
                                "Chart type",
                                style={
                                    "margin-left": 12,
                                    "font-family": "Quicksand, sans-serif",
                                    "font-size": 16,
                                    "color": "lightblue",
                                },
                            ),
                            dbc.Row(
                                justify="center",
                                no_gutters=True,
                                children=[
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Bar",
                                                color="secondary",
                                                id=f"{graph_id}-btn-bar",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Line",
                                                color="secondary",
                                                id=f"{graph_id}-btn-line",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Pie",
                                                color="secondary",
                                                id=f"{graph_id}-btn-pie",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Map",
                                                color="secondary",
                                                id=f"{graph_id}-btn-map",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            dbc.Row(
                                justify="center",
                                no_gutters=True,
                                children=[
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Bar+",
                                                color="secondary",
                                                id=f"{graph_id}-btn-barplus",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Area",
                                                color="secondary",
                                                id=f"{graph_id}-btn-area",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Sun",
                                                color="secondary",
                                                id=f"{graph_id}-btn-sunburst",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        style=buttons_style_chart_types,
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Sankey",
                                                color="secondary",
                                                id=f"{graph_id}-btn-sankey",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        width=11,
                                        children=[
                                            dbc.Button(
                                                "Ratio",
                                                color="secondary",
                                                id=f"{graph_id}-btn-ratio",
                                                block=True,
                                                style={
                                                    "border": "1px lightblue solid",
                                                    "width": "100%",
                                                    # "margin-left": -8,
                                                    # "margin-right": 16
                                                },
                                            ),
                                        ],
                                    ),
                                    dbc.Row(
                                        align="center",
                                        justify="center",
                                        # no_gutters=True,
                                        children=[
                                            dbc.Col(
                                                width=5,
                                                style={
                                                    "margin-top": 12,
                                                    # "margin-bottom": 12,
                                                    "margin-right": 12,
                                                },
                                                children=[
                                                    dbc.Checklist(
                                                        labelStyle={
                                                            "font-family": "Quicksand, sans-serif",
                                                            "font-size": 17,
                                                            "color": "lightblue",
                                                            "margin-left": 24,
                                                            "margin-top": 12,
                                                            "margin-bottom": 12,
                                                        },
                                                        inputStyle={"size": 64},
                                                        options=[
                                                            {
                                                                "label": "Rotate",
                                                                "value": "Rotate",
                                                            },
                                                            {
                                                                "label": "Foreach",
                                                                "value": "Foreach",
                                                            },
                                                        ],
                                                        value=[],
                                                        id=f"{graph_id}-options-1",
                                                        switch=True,
                                                        # inline=True,
                                                    ),
                                                ],
                                            ),
                                            dbc.Col(
                                                width=5,
                                                style={
                                                    "margin-top": 12,
                                                    # "margin-bottom": 12,
                                                    # "margin-left": 124,
                                                },
                                                children=[
                                                    dbc.Checklist(
                                                        labelStyle={
                                                            "font-family": "Quicksand, sans-serif",
                                                            "font-size": 17,
                                                            "color": "lightblue",
                                                            "margin-left": 24,
                                                            "margin-top": 12,
                                                            "margin-bottom": 12,
                                                        },
                                                        # inputStyle={
                                                        #     "margin-bottom": 12, },
                                                        options=[
                                                            {
                                                                "label": "Stack",
                                                                "value": "Stack",
                                                            },
                                                            {
                                                                "label": "Group",
                                                                "value": "Group",
                                                            },
                                                        ],
                                                        value=[],
                                                        id=f"{graph_id}-options-2",
                                                        switch=True,
                                                        # inline=True,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # dbc.Row(
                            #     justify="center",
                            #     no_gutters=True,
                            #     children=[
                            #         dbc.Col(
                            #             width=12,
                            #             children=[
                            #                 dbc.Button(
                            #                     "Ratio",
                            #                     color="primary",
                            #                     id=f"{graph_id}-btn-ratio",
                            #                     block=True,
                            #                     # outline=True,
                            #                     style={
                            #                         # "width": "100%",
                            #                         # "margin-left": -12,
                            #                         "padding-left": -12,
                            #                         "padding-right": -12,
                            #                         "margin-top": 2,
                            #                     },
                            #                 ),
                            #             ],
                            #         ),
                            #     ]
                            # ),
                        ],
                    ),
                    dbc.CardFooter(
                        style={
                            "margin-left": 4,
                            "margin-right": 4,
                            "margin-bottom": 1,
                            "border": "0px lightblue solid",
                            "border-radius": 0,
                        },
                        children=[
                            dbc.Row(
                                justify="center",
                                no_gutters=True,
                                children=[
                                    dbc.Col(
                                        # style={"margin-left": 24},
                                        width=3,
                                        children=[
                                            dbc.DropdownMenu(
                                                [
                                                    dbc.DropdownMenuItem(
                                                        "Stats",
                                                        id=f"{graph_id}btn-table-stats",
                                                    ),
                                                    dbc.DropdownMenuItem(
                                                        "Summary",
                                                        id=f"{graph_id}-btn-table-sum",
                                                    ),
                                                ],
                                                label="Table",
                                                # className="m-1",
                                                color="warning",
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Save",
                                                color="info",
                                                id=f"{graph_id}-btn-save",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        width=3,
                                        # width={"offset": 3, "width": 9},
                                        children=[
                                            dbc.Button(
                                                "Image",
                                                color="info",
                                                id=f"{graph_id}-btn-image",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                    dbc.Col(
                                        width=3,
                                        children=[
                                            dbc.Button(
                                                "Excel",
                                                color="info",
                                                id=f"{graph_id}-btn-xlsx",
                                                block=True,
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            )
        ],
    )


def create_eb_graph_view(graph_id: str):

    return

    # dbc.InputGroup(
    #     [
    #         dbc.InputGroupAddon(
    #             dbc.RadioButton(), addon_type="prepend"),
    #         dbc.Input(
    #             id=f"{graph_id}-foreach"
    #             disabled=True, placeholder="Foreach"
    #         ),
    #     ],
    #     className="mb-3",
    # ),
    # dbc.InputGroup(
    #     [
    #         dbc.InputGroupAddon(
    #             dbc.RadioButton(), addon_type="prepend"),
    #         dbc.Input(
    #             id=f"{graph_id}-Stack"
    #             disabled=True, placeholder="Group"
    #         ),
    #     ],
    #     className="mb-3",
    # ),
    # dbc.InputGroup(
    #     [
    #         dbc.InputGroupAddon(
    #             dbc.RadioButton(), addon_type="prepend"),
    #         dbc.Input(
    #             id=f"{graph_id}-foreach"
    #             disabled=True, placeholder="Foreach"
    #         ),
    #     ],
    #     className="mb-3",
    # ),
    #     ]
    # ),
    # dbc.Col(
    #     # width={"offset": 7, "size": 5},
    #     width=12,
    #     children=[

    #         chart_type_row(
    #             graph_id=graph_id),
    #         html.Br(),
    #         data_scale_row(
    #             graph_id=graph_id),
    #         # html.Br(),
    #     ],
    # ),

    # dbc.Row(
    #     align="center",
    #     justify="end",
    #     no_gutters=True,
    #     children=[
    #         dbc.InputGroup(
    #             [
    #                 dbc.InputGroupAddon(
    #                     dbc.RadioButton(), addon_type="prepend"),
    #                 dbc.Input(
    #                     id=f"{graph_id}-foreach",
    #                     disabled=True, placeholder="Foreach"
    #                 ),
    #             ],
    #             className="mb-3",
    #         ),
    #     ]
    # ),
    # dbc.Row(
    #     align="center",
    #     justify="end",
    #     no_gutters=True,
    #     children=[
    #         dbc.InputGroup(
    #             [
    #                 dbc.InputGroupAddon(
    #                     dbc.RadioButton(), addon_type="prepend"),
    #                 dbc.Input(
    #                     id=f"{graph_id}-stack",
    #                     disabled=True, placeholder="Stack"
    #                 ),
    #             ],
    #             className="mb-3",
    #         ),
    #     ]
    # ),
    # dbc.Row(
    #     align="center",
    #     justify="end",
    #     no_gutters=True,
    #     children=[
    #         dbc.InputGroup(
    #             [
    #                 dbc.InputGroupAddon(
    #                     dbc.RadioButton(), addon_type="prepend"),
    #                 dbc.Input(
    #                     id=f"{graph_id}-group",
    #                     disabled=True, placeholder="Group"
    #                 ),
    #             ],
    #             className="mb-3",
    #         ),
    #     ]
    # ),
    #     ]
    # ),

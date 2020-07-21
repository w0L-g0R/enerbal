import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def create_eev_graph_view(graph_id: str):

    return dbc.Container(
        # fluid=True,
        children=[
            first_row(graph_id=graph_id)[0],
            second_row(graph_id=graph_id)[0],
            third_row(graph_id=graph_id)[0],
            fourth_row(graph_id=graph_id)[0],
            fifth_row(graph_id=graph_id)[0],
            sixth_row(graph_id=graph_id)[0],
        ]
    )


def first_row(graph_id: str):
    return (
        dbc.Row(
            no_gutters=True,
            children=[
                dbc.Col(
                    width=12,
                    children=[
                        dbc.FormGroup(
                            [
                                dbc.Label("Titel"),
                                dbc.Input(
                                    placeholder="Title goes here...",
                                    type="text",
                                    id=f"plot-title-{graph_id}",
                                ),
                            ]
                        )
                    ],
                ),
            ],
        ),
    )


def second_row(graph_id: str):
    return (
        dbc.Row(
            no_gutters=True,
            children=[
                dbc.Col(
                    width=10,
                    children=[
                        dbc.FormGroup(
                            children=[
                                dbc.Label("Datenskalierung"),
                                dbc.RadioItems(
                                    style={"padding-top": 6,
                                           "margin-right": 4},
                                    options=[
                                        {"label": "Absolute", "value": 1, },
                                        {"label": "Normalized", "value": 2, },
                                        {"label": "Index Year", "value": 3, },
                                    ],
                                    value=1,
                                    id=f"radio-scale-{graph_id}",
                                    inline=True,
                                ),
                            ]
                        )
                    ],
                ),
                dbc.Col(
                    width=2,
                    children=[
                        dbc.FormGroup(
                            [
                                dbc.Label("Index Jahr"),
                                dbc.Input(
                                    placeholder="",
                                    type="text",
                                    id=f"index-year-{graph_id}",
                                ),
                            ]
                        )
                    ],
                ),
            ],
        ),
    )


def third_row(graph_id: str):
    return (
        dbc.Row(
            no_gutters=True,
            children=[
                dbc.Col(
                    width=2,
                    children=[
                        dbc.FormGroup(
                            style={"margin-right": 4},
                            children=[
                                dbc.Label("Aggregat"),
                                dbc.Select(
                                    id=f"select-aggregat-{graph_id}",
                                    options=[
                                        {"label": "Option 1", "value": "1"},
                                        {"label": "Option 2", "value": "2"},
                                        {
                                            "label": "Disabled option",
                                            "value": "3",
                                            "disabled": True,
                                        },
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                dbc.Col(
                    width=8,
                    children=[
                        dbc.FormGroup(
                            style={"margin-right": 4},
                            children=[
                                dbc.Label("Energieträger"),
                                dbc.Select(
                                    id=f"select-energy-sources-{graph_id}",
                                    options=[
                                        {"label": "Option 1", "value": "1"},
                                        {"label": "Option 2", "value": "2"},
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                dbc.Col(
                    width=2,
                    children=[
                        dbc.FormGroup(
                            [
                                dbc.Label("Zeilenindex"),
                                dbc.Input(
                                    placeholder="",
                                    type="number",
                                    id=f"row-index-{graph_id}",
                                ),
                            ]
                        )
                    ],
                ),
            ],
        ),
    )


def fourth_row(graph_id: str):
    return (
        dbc.Row(
            justify="center",
            align="center",
            children=[
                dbc.Col(
                    width=10,
                    children=[
                        dbc.FormGroup(
                            children=[
                                dbc.Label("Datenbereich"),
                                dbc.RadioItems(
                                    style={"padding-top": 6,
                                           "margin-right": 4},
                                    options=[
                                        {"label": "EEV", "value": 1, },
                                        {"label": "Sektoren", "value": 2, },
                                        {"label": "Sektor Energie", "value": 3, },
                                        {"label": "ErnRL", "value": 3, },
                                    ],
                                    value=1,
                                    id=f"radio-scale-{graph_id}",
                                    inline=True,
                                ),
                            ]
                        )
                    ],
                ),
                dbc.Col(
                    width=2,
                    children=[
                        dbc.FormGroup(
                            style={"margin-left": -24},
                            children=[
                                dbc.Label("Einheit"),
                                dbc.Select(
                                    id=f"select-energy-unit-{graph_id}",
                                    options=[
                                        {"label": "GWh", "value": "1"},
                                        {"label": "TJ", "value": "2"},
                                        {"label": "PJ", "value": "3"},
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            ],
        ),
    )


range_slider_style = {"color": "#FBFCFF", "font-size": 14}


def fifth_row(graph_id: str):
    return (
        dbc.Row(
            no_gutters=True,
            # style={"margin-top": 24},
            children=[
                dbc.Col(
                    width=12,
                    children=[
                        dbc.InputGroup(
                            [
                                dbc.InputGroupAddon(
                                    "IDX 0", addon_type="prepend"),
                                dbc.Select(
                                    id=f"select-idx-0-{graph_id}",
                                    options=[
                                        {"label": "Option 1", "value": "1"},
                                        {"label": "Option 2", "value": "2"},
                                    ],
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                ),
                dbc.Col(
                    width=12,
                    children=[
                        dbc.InputGroup(
                            [
                                dbc.InputGroupAddon(
                                    "IDX 1", addon_type="prepend"),
                                dbc.Select(
                                    id=f"select-idx-1-{graph_id}",
                                    options=[
                                        {"label": "Option 1", "value": "1"},
                                        {"label": "Option 2", "value": "2"},
                                    ],
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                ),
                dbc.Col(
                    width=12,
                    children=[
                        dbc.InputGroup(
                            [
                                dbc.InputGroupAddon(
                                    "IDX 2", addon_type="prepend"),
                                dbc.Select(
                                    id=f"select-idx-2-{graph_id}",
                                    options=[
                                        {"label": "Option 1", "value": "1"},
                                        {"label": "Option 2", "value": "2"},
                                    ],
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                ),
                dbc.Col(
                    width=12,
                    children=[
                        dbc.InputGroup(
                            [
                                dbc.InputGroupAddon(
                                    "IDX 3", addon_type="prepend"),
                                dbc.Select(
                                    id=f"select-idx-3-{graph_id}",
                                    options=[
                                        {"label": "Option 1", "value": "1"},
                                        {"label": "Option 2", "value": "2"},
                                    ],
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                ),
                dbc.Col(
                    width=12,
                    children=[
                        dbc.InputGroup(
                            [
                                dbc.InputGroupAddon(
                                    "IDX 4", addon_type="prepend"),
                                dbc.Select(
                                    id=f"select-idx-4-{graph_id}",
                                    options=[
                                        {"label": "Option 1", "value": "1"},
                                        {"label": "Option 2", "value": "2"},
                                    ],
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                ),
            ],
        ),
    )


def sixth_row(graph_id: str):
    return (
        dbc.Row(
            style={"margin-top": 24},
            no_gutters=True,
            children=[
                dbc.Col(
                    width=12,
                    children=[
                        dcc.RangeSlider(
                            min=0,
                            max=2,
                            step=1,
                            marks={
                                0: {"label": "Line", "style": range_slider_style},
                                1: {"label": "Bar", "style": range_slider_style},
                                2: {"label": "Subplot", "style": range_slider_style, },
                            },
                            value=[0],
                        )
                    ],
                ),
            ],
        ),
    )


eev = {}
eev["graph-A"] = create_eev_graph_view(graph_id="graph-A")
eev["graph-B"] = create_eev_graph_view(graph_id="graph-B")

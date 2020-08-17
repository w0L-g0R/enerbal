import dash_bootstrap_components as dbc
import dash_html_components as html

from gui.assets.AEA_colors import provinces_color_table

# from settings import *


def create_province_input_group(
    province: str, placeholder: str, color: str, checked: bool = True
):
    return dbc.Row(
        no_gutters=True,
        children=[
            dbc.Col(
                style={"margin-right": 4, },
                children=[
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon(
                                children=province,
                                addon_type="prepend",
                                style={"width": 46},
                            ),
                            dbc.Input(
                                placeholder=placeholder, id=f"plot-name-{province}"
                            ),
                        ]
                    ),
                ],
            ),
            html.Div(
                style={
                    "background-color": color,
                    "border-radius": 4,
                    "border": "1px black solid",
                    "margin-right": 8,
                    "position": "relative",
                    "right": -8,
                    "top": 5,
                    "width": 24,
                    "height": 24,
                },
                children=dbc.Checklist(
                    labelStyle={
                        "margin-top": 6,
                        "margin-left": 12,
                        "margin-right": -24,
                        "width": 24,
                        "height": 24,
                        # "color": "green",
                        # "padding-right": 20,
                        # "text-align": "right",
                    },
                    options=[{"label": "", "value": 1, }, ],
                    value=[1 if checked else 0],
                    inline=True,
                    id="checklist-{}".format(province),
                ),
            ),
        ],
    )


layout = dbc.Card(
    style={"width": "100%", "border": "1px lightblue solid"},
    children=[
        dbc.CardBody(
            children=[
                dbc.Row(
                    no_gutters=True,
                    children=[
                        dbc.Col(
                            children=[
                                html.H5(
                                    "Provinces",
                                    # style={"margin": 7.5},
                                    className="card-title",
                                ),
                            ],
                        ),
                        dbc.Col(
                            width=2,
                            style={"margin-right": 16},
                            children=[
                                dbc.ButtonGroup(
                                    children=[
                                        dbc.Button("All", color="success"),
                                        dbc.Button("None", color="success"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                dbc.Row(
                    justify="center",
                    align="center",
                    no_gutters=True,
                    children=[
                        dbc.Row(
                            # xs=12,
                            # sm=12,
                            # md=12,
                            # lg=12,
                            # xl=12,
                            style={"margin-top": 12},
                            no_gutters=True,
                            justify="center",
                            children=[
                                dbc.Col(
                                    style={"margin-right": 16},
                                    children=[
                                        create_province_input_group(
                                            province="AT",
                                            placeholder="Österreich",
                                            color=provinces_color_table["AT"],
                                            checked=False,
                                        ),
                                        create_province_input_group(
                                            province="Wie",
                                            placeholder="Wien",
                                            color=provinces_color_table["Wie"],
                                        ),
                                        create_province_input_group(
                                            province="Bgd",
                                            placeholder="Burgenland",
                                            color=provinces_color_table["Bgd"],
                                        ),
                                        create_province_input_group(
                                            province="Noe",
                                            placeholder="Niederösterr.",
                                            color=provinces_color_table["Noe"],
                                        ),
                                        create_province_input_group(
                                            province="Ooe",
                                            placeholder="Oberösterr.",
                                            color=provinces_color_table["Ooe"],
                                        ),
                                    ],
                                ),
                                dbc.Col(
                                    # width=6,
                                    children=[
                                        create_province_input_group(
                                            province="Sbg",
                                            placeholder="Salzburg",
                                            color=provinces_color_table["Sbg"],
                                        ),
                                        create_province_input_group(
                                            province="Stk",
                                            placeholder="Steiermark",
                                            color=provinces_color_table["Stk"],
                                        ),
                                        create_province_input_group(
                                            province="Ktn",
                                            placeholder="Kärnten",
                                            color=provinces_color_table["Ktn"],
                                        ),
                                        create_province_input_group(
                                            province="Tir",
                                            placeholder="Tirol",
                                            color=provinces_color_table["Tir"],
                                        ),
                                        create_province_input_group(
                                            province="Vbg",
                                            placeholder="Vorarlberg",
                                            color=provinces_color_table["Vbg"],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        ),
    ],
)


# %%

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from gui.views.setup_components import chart_type_row, data_scale_row


def create_plots_dropdown(graph_id: str):

    return dbc.FormGroup(
        style={"margin-bottom": 0},
        children=[
            # dbc.Label("Einheit", style=label_style),
            dcc.Dropdown(
                id=f"{graph_id}-plots",
                placeholder="Select ... "

            ),
        ],
    )


def create_graph_box_layout(graph_id: str):
    return dbc.Card(
        style={"width": "100%", "border": "1px lightblue solid"},
        children=[
            dbc.CardHeader(

                style={"height": 82},
                children=[
                    dbc.Row(

                        # justify="end",
                        no_gutters=True,
                        children=[
                            dbc.Col(
                                # width=7,
                                children=[
                                    html.H5(graph_id, className="card-title"), ],
                            ),
                            dbc.Col(
                                # width={"offset": 7, "size": 5},
                                width=9,
                                children=[
                                    data_scale_row(graph_id=graph_id),
                                    html.Br(),
                                    html.Div(
                                        style={"display": "none"},
                                        children=create_plots_dropdown(
                                            graph_id=graph_id)
                                    )
                                ],
                            ),
                        ],
                    ),
                ]
            ),
            dbc.CardBody(
                id=f"{graph_id}-box",
                children=[
                    dcc.Graph(
                        id=f"{graph_id}-figure",
                        style={"width": 516},
                        figure=dict(
                            data=[
                                dict(
                                    x=[
                                        1995,
                                        1996,
                                        1997,
                                        1998,
                                        1999,
                                        2000,
                                        2001,
                                        2002,
                                        2003,
                                        2004,
                                        2005,
                                        2006,
                                        2007,
                                        2008,
                                        2009,
                                        2010,
                                        2011,
                                        2012,
                                    ],
                                    y=[
                                        219,
                                        146,
                                        112,
                                        127,
                                        124,
                                        180,
                                        236,
                                        207,
                                        236,
                                        263,
                                        350,
                                        430,
                                        474,
                                        526,
                                        488,
                                        537,
                                        500,
                                        439,
                                    ],
                                    name="Rest of world",
                                    marker=dict(color="rgb(55, 83, 109)"),
                                ),
                                dict(
                                    x=[
                                        1995,
                                        1996,
                                        1997,
                                        1998,
                                        1999,
                                        2000,
                                        2001,
                                        2002,
                                        2003,
                                        2004,
                                        2005,
                                        2006,
                                        2007,
                                        2008,
                                        2009,
                                        2010,
                                        2011,
                                        2012,
                                    ],
                                    y=[
                                        16,
                                        13,
                                        10,
                                        11,
                                        28,
                                        37,
                                        43,
                                        55,
                                        56,
                                        88,
                                        105,
                                        156,
                                        270,
                                        299,
                                        340,
                                        403,
                                        549,
                                        499,
                                    ],
                                    name="China",
                                    marker=dict(color="rgb(26, 118, 255)"),
                                ),
                            ],
                            layout=dict(
                                title="US Export of Plastic Scrap",
                                showlegend=True,
                                legend=dict(x=0, y=1.0),
                                margin=dict(l=0, r=0, t=30, b=30),
                                # width=1040,
                                height=320,
                            ),
                        ),
                    )
                ],
            ),
            dbc.CardFooter(

                style={"height": 80},
                children=[
                    dbc.Row(

                        # justify="end",
                        no_gutters=True,
                        children=[
                            # dbc.Col(
                            #     # width=7,
                            #     children=[
                            #         html.H5(graph_id, className="card-title"), ],
                            # ),
                            dbc.Col(

                                # width={"offset": 7, "size": 5},
                                width=12,
                                children=[
                                    chart_type_row(graph_id=graph_id),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )


# title_A = html.Img(
#     style={"margin-top": 0, "margin-bottom": -4},
#     src="https://fontmeme.com/permalink/200718/c53ecf1fd39235d3f8a16935633bbdfa.png",
#     # style=navbar_logo_style,
# )

# title_B = html.Img(
#     style={"margin-top": 0, "margin-bottom": -4},
#     src="https://fontmeme.com/permalink/200718/f155c17403325746f18dfe4eea451281.png",
#     # style=navbar_logo_style,
# )

graph_A = create_graph_box_layout(graph_id="graph-A")
graph_B = create_graph_box_layout(graph_id="graph-B")

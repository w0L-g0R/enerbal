import inspect
import logging
import os
from pathlib import Path
from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def create_graph_layout(graph_id: str):

    return dbc.Card(
        style={"width": "100%", "border": "1px lightblue solid"},
        children=[
            dbc.CardHeader(
                children=[
                    dbc.Row(
                        no_gutters=True,
                        children=[
                            dbc.Col(
                                width=7,
                                children=[
                                    html.H5("Plot B", className="card-title"), ],
                            ),
                            dbc.Col(
                                width=4,
                                children=[
                                    dbc.ButtonGroup(
                                        style={"margin": 0},
                                        children=[
                                            dbc.Button(
                                                "Update",
                                                color="success",
                                                id=f"update-{graph_id}",
                                            ),
                                            dbc.Button(
                                                "Excel", color="success"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
            dbc.CardBody(
                children=[
                    dcc.Graph(
                        id=f"{graph_id}",
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
                                width=520,
                                height=320,
                            ),
                        ),
                        style={"width": 560},
                    )
                ],
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


graph_A_layout = create_graph_layout(graph_id="graph-A")
graph_B_layout = create_graph_layout(graph_id="graph-B")
import dash_bootstrap_components as dbc
import dash_html_components as html

from gui.components.controller import views

layout = dbc.Container(
    style={"padding-top": 24},
    # fluid=True,
    children=[
        dbc.Row(
            # justify="center",
            # align="center",
            # style={"margin": 4, "margin-right": 0, "height": 44},
            no_gutters=True,
            children=[
                dbc.Col(
                    style={"margin-bottom": 12, },
                    width=12,
                    children=views["header_layout"],
                ),

                # html.Div(style={"border-top": "1px solid #2A2A57"}),
                # dbc.Col(width=12, children=[]),
                dbc.Row(
                    style={"height": "100%"},
                    children=[
                        dbc.Col(
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                            xl=6,
                            children=views["years_layout"],
                            style={"padding": 6},
                        ),
                        dbc.Col(
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                            xl=6,
                            children=views["provinces_layout"],
                            style={"padding": 6, },
                        ),
                    ],
                ),
                dbc.Row(
                    style={"height": "100%"},
                    children=[
                        dbc.Col(
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                            xl=6,
                            children=views["graph_setup_A_layout"],
                            style={"padding": 6},
                        ),
                        dbc.Col(
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                            xl=6,
                            children=views["graph_setup_B_layout"],
                            style={"padding": 6, },
                        ),
                    ],
                ),
                dbc.Row(
                    style={"height": "100%"},
                    children=[
                        dbc.Col(
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                            xl=6,
                            children=views["graph_A_layout"],
                            style={"padding": 6},
                        ),
                        dbc.Col(
                            xs=12,
                            sm=12,
                            md=12,
                            lg=6,
                            xl=6,
                            children=views["graph_B_layout"],
                            style={"padding": 6, },
                        ),
                    ],
                ),

                dbc.Row(
                    style={"width": 1164},
                    children=[
                        dbc.Col(
                            xs=12,
                            sm=12,
                            md=12,
                            lg=12,
                            xl=12,
                            children=views["graph_AB_layout"],
                            style={"padding": 6, "width": "100%"},
                        ),
                    ],
                ),
            ],
        )
    ],
)

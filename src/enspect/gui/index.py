import dash_bootstrap_components as dbc
from gui.storages import stores
from gui.view import layout

# //////////////////////////////////////////////////////////////////// LAYOUT

layout = dbc.Container(
    fluid=True,
    # className="body-content",
    # id="root-container",
    className="root-container",
    # style=container_style,
    children=[
        # ADDRESS BAR
        # dcc.Location(id="url", refresh=False),
        # NAVBAR
        dbc.Row(
            style={"margin": 0, "padding": 0},
            no_gutters=True,
            # NOTE: ==> GLOBAL STORES
            children=[
                stores
                # file_management_store,
                # parameter_store,
                # timeseries_store,
                # results_store,
            ],
        ),
        dbc.Row(
            style={"margin": 0, "padding": 0},
            no_gutters=True,
            children=[
                # html.Div(
                # ),
                dbc.Col(
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
                    xl=12,
                    style={"margin": 0, "padding": 0},
                    children=[
                        # navbar_layout,
                        layout
                        # html.Div(id="body-content",)
                    ],
                ),
            ],
        ),
    ],
)


# # ///////////////////////////////////////////////////////////////////// ROUTING


# @app.callback(Output("body-content", "children"), [Input("url", "pathname")])
# def display_page(pathname):

#     if pathname == "/home":
#         return

#     elif pathname == "/configuration-parameter":
#         return parameter_layout

#     elif pathname == "/configuration-timeseries":
#         return timeseries_layout

#     elif pathname == "/configuration-units":
#         return powerplants_layout

#     elif pathname == "/simulation-results":
#         return results_layout

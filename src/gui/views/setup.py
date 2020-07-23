import inspect
import logging
import os
from pathlib import Path
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html


def create_setup_layout(graph_id: str, title: str):

    return dbc.Card(
        style={"width": "100%", "border": "1px yellow solid"},
        children=[
            dbc.CardHeader(
                children=[
                    dbc.Row(
                        # justify="end",
                        no_gutters=True,
                        children=[
                            dbc.Col(
                                # width=2,
                                children=[
                                    title
                                ],
                            ),
                            dbc.Col(
                                # style={"margin-left": 64},
                                width={"offset": 3, "width": 9},
                                children=[
                                    dbc.Tabs(
                                        [
                                            dbc.Tab(
                                                label="EB", tab_id=f"tab-eb-{graph_id}",
                                            ),
                                            dbc.Tab(
                                                label="NEA", tab_id=f"tab-nea-{graph_id}",
                                            ),
                                            dbc.Tab(
                                                label="THG", tab_id=f"tab-thg-{graph_id}",
                                            ),
                                            dbc.Tab(
                                                label="STATS",
                                                tab_id=f"tab-stats-{graph_id}",
                                            ),
                                        ],
                                        id=f"tabs-{graph_id}",
                                        card=True,
                                        active_tab=f"tab-eb-{graph_id}",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
            dbc.CardBody(id=f"content-{graph_id}",),
            dbc.CardFooter(
                dbc.Button(
                    "Set up",
                    color="primary",
                    id=f"btn-setup-{graph_id}",
                    block=True
                ),

            )
        ],
    )


title_A = html.Img(
    style={"margin-top": 0, "margin-bottom": -4},
    src="https://fontmeme.com/permalink/200718/c53ecf1fd39235d3f8a16935633bbdfa.png",
    # style=navbar_logo_style,
)

title_B = html.Img(
    style={"margin-top": 0, "margin-bottom": -4},
    src="https://fontmeme.com/permalink/200718/f155c17403325746f18dfe4eea451281.png",
    # style=navbar_logo_style,
)


setup_A = create_setup_layout(
    graph_id="graph-A", title=title_A)
setup_B = create_setup_layout(
    graph_id="graph-B", title=title_B)


# @app.callback(
#     Output(component_id="text-graph-A", component_property="children"),
#     [Input(component_id="button-graph-A", component_property="n_clicks")],
# )
# def update_output_div(n_clicks):
#     return "Output: {}".format(n_clicks)


# @app.callback(
#     Output(f"content-graph-A", "children"),
#     [Input(f"button-graph-A", "n_clicks")],
#     # [State(f"tabs-graph-A", "active_tab")],
# )
# def on_graph_tab_change(active_tab):

#     show_callback_context(
#         verbose=True,
#         func_name=inspect.stack()[0][3],
#         file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
#     )

#     logging.getLogger().debug("Blue")

#     return "HIIII"
# if active_tab == f"tab-1-graph_A":

#     return "Hi"

#     # if "graph_A" in active_tab:
#     #     return "HULLI"  # views["eev_A"]

#     # elif "graph_B" in active_tab:
#     #     return views["eev_B"]

# elif "tab-2" in active_tab:
#     return


# create_on_graph_tab_change(graph_id="graph_A")
# create_on_graph_tab_change(graph_id="graph_B")


# @app.callback(Output("card-content", "children"), [Input("card-tabs", "active_tab")])
# def tab_content(active_tab):
#     if active_tab == "tab-1":
#         return tab1_content
#     elif active_tab == "tab-2":
#         return tab2_content
#     return "This is tab {}".format(active_tab)


# def create_graph_title_layout(graph_id: str):

#     return dbc.FormGroup(
#         [
#             dbc.Label("Plot title"),
#             dbc.Input(
#                 placeholder="Title name goes here...",
#                 type="text",
#                 id=f"title-{graph_id}",
#             ),
#         ]
#     )


# def create_graph_data_scale_type_layout(graph_id: str):

#     return dbc.FormGroup(
#         [
#             dbc.Label("Choose one"),
#             dbc.RadioItems(
#                 options=[
#                     {"label": "Absolute", "value": 1},
#                     {"label": "Normalized", "value": 2},
#                     {"label": "Index Year", "value": 3},
#                 ],
#                 inline=True,
#                 value=1,
#                 id=f"radioitems-data-scale-{graph_id}",
#             ),
#             dbc.Input(
#                 placeholder="Title name goes here...",
#                 type="text",
#                 id=f"title-{graph_id}",
#             ),
#         ]
#     )


# def create_graph_output_control_layout(graph_id: str):

#     return dbc.FormGroup(
#         [
#             dbc.Label("Choose one"),
#             dbc.RadioItems(
#                 options=[
#                     {"label": "Absolute", "value": 1},
#                     {"label": "Normalized", "value": 2},
#                     {"label": "Index Year", "value": 3},
#                 ],
#                 value=1,
#                 id=f"radioitems-data-scale-{graph_id}",
#             ),
#         ]
#     )

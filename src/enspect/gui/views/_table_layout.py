# %%

import dash_bootstrap_components as dbc
import dash_html_components as html


def create_table_layout(graph_id: str):

    return dbc.Card(
        style={"width": "100%", "border": "1px lightblue solid"},
        children=[
            dbc.CardHeader(
                children=[
                    dbc.Row(
                        # justify="end",
                        # no_gutters=True,
                        children=[
                            dbc.Col(
                                # width=7,
                                children=[html.H5(graph_id, className="card-title"),],
                            ),
                            dbc.Col(
                                # width={"offset": 7, "size": 5},
                                # width=2,
                                children=[
                                    dbc.ButtonGroup(
                                        # style={"margin-right": 32},
                                        children=[
                                            dbc.Button(
                                                "Table A",
                                                color="success",
                                                id=f"table-A-{graph_id}",
                                            ),
                                            dbc.Button(
                                                "Table B",
                                                color="success",
                                                id=f"table-B-{graph_id}",
                                            ),
                                            dbc.Button(
                                                "Graph A",
                                                color="success",
                                                id=f"show-A-{graph_id}",
                                            ),
                                            dbc.Button(
                                                "Graph B",
                                                color="success",
                                                id=f"show-B-{graph_id}",
                                            ),
                                            dbc.Button(
                                                "Graph A/B",
                                                color="success",
                                                id=f"show-{graph_id}",
                                            ),
                                            dbc.Button("Excel", color="success"),
                                        ],
                                    )
                                ],
                            ),
                        ],
                    ),
                ]
            ),
            dbc.CardBody(id=f"table-{graph_id}", children=[],),
        ],
    )


# def create_table_layout(graph_id: str):
#     # df =
#     return dbc.CardBody(
#                 id=f"box-{graph_id}",
#                 children=[
#                     # dash_table.DataTable(
#                     #     id='table',
#                     #     columns=[{"name": i, "id": i} for i in df.columns],
#                     #     data=df.to_dict('records'),
#                     # )
#                 ],
#             ),
#         ],
#     )


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


# graph_A_layout = create_graph_layout(graph_id="graph-A")
# graph_B_layout = create_graph_layout(graph_id="graph-B")
graph_AB_layout = create_table_layout(graph_id="graph-AB")
# graph_AB_layout[0] = 0

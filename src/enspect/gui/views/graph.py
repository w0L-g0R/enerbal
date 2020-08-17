import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from settings import DEFAULT_CHART_CONFIG
from gui.views.setup.rows import data_scale_row, chart_type_row


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

    return dbc.Row(

        children=[

            dbc.Container(
                fluid=True,
                id=f"{graph_id}-container",
                style={
                    "min-height": "100vh",
                    "width": "100%"},
                children=[

                    # dcc.Graph(

                    # )
                ],
            ),
        ]
    )


# dbc.CardFooter(

#     style={"height": 80},
#     children=[
#         dbc.Row(

#             # justify="end",
#             no_gutters=True,
#             children=[
#                 # dbc.Col(
#                 #     # width=7,
#                 #     children=[
#                 #         html.H5(graph_id, className="card-title"), ],
#                 # ),
#                 dbc.Col(

#                     # width={"offset": 7, "size": 5},
#                     width=12,
#                     children=[
#                         chart_type_row(graph_id=graph_id),
#                     ],
#                 ),
#             ],
#         ),
#     ]
# ),

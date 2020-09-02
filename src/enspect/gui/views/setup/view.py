import dash_bootstrap_components as dbc
import dash_html_components as html
from gui.views.control import create_control_box_layout
from gui.views.setup.rows import (
    chart_type_row,
    data_scale_row,
    eb_aggregate_row,
    eb_data_section_row,
    eev_idx_rows,
    renewables_idx_rows,
    sector_energy_idx_rows,
    sectors_idx_rows,
    xaxis_type_row,
)


def create_eb_graph_view(graph_id: str):

    return html.Div(
        style={
            "margin-left": 6,
            "margin-right": 6,
            # "margin-top": 12,
            # "margin-bottom": -12,
            "border": "0px lightblue solid",
            "border-radius": 4,
        },
        # fluid=True,
        children=[
            xaxis_type_row(graph_id=graph_id),
            html.Br(),
            dbc.CardFooter(
                children=[
                    eb_aggregate_row(graph_id=graph_id),
                ]
            ),
            dbc.CardFooter(
                children=[
                    eb_data_section_row(graph_id=graph_id),
                    # idx
                    html.Div(
                        style={
                            # "margin-left": 4,
                            "margin-top": 12,
                            # "margin-bottom": -12,
                            "border": "0px lightblue solid",
                            "border-radius": 4,
                        },
                        id=f"idx-eev-{graph_id}",
                        # style={"display": "none"},
                        children=eev_idx_rows(graph_id=graph_id),
                    ),
                    # idx
                    html.Div(
                        id=f"idx-sectors-{graph_id}",
                        style={"display": "none"},
                        children=sectors_idx_rows(graph_id=graph_id),
                    ),
                    # idx
                    html.Div(
                        id=f"idx-sector-energy-{graph_id}",
                        style={"display": "none"},
                        children=sector_energy_idx_rows(graph_id=graph_id),
                    ),
                    # idx
                    html.Div(
                        id=f"idx-renewables-{graph_id}",
                        style={"display": "none"},
                        children=renewables_idx_rows(graph_id=graph_id),
                    ),
                ]
            ),
        ],
    )


def create_setup_layout(graph_id: str, title: str):

    return dbc.Card(
        style={"width": "100%", "border": "1px lightblue solid"},
        children=[
            dbc.CardHeader(
                children=[
                    dbc.Row(
                        # justify="end",
                        no_gutters=True,
                        children=[
                            dbc.Col(
                                # width=2,
                                children=[title],
                            ),
                            dbc.Col(
                                # style={"margin-left": 64},
                                width={"offset": 3, "width": 9},
                                children=[
                                    dbc.Tabs(
                                        [
                                            dbc.Tab(
                                                label="EB",
                                                tab_id=f"tab-eb-{graph_id}",
                                            ),
                                            dbc.Tab(
                                                label="NEA",
                                                tab_id=f"tab-nea-{graph_id}",
                                            ),
                                            dbc.Tab(
                                                label="THG",
                                                tab_id=f"tab-thg-{graph_id}",
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
            dbc.CardBody(
                id=f"{graph_id}-content",
            ),
            create_control_box_layout(graph_id=graph_id),
        ],
    )


eb_setup_views = {}
eb_setup_views["graph-A"] = create_eb_graph_view(graph_id="graph-A")
eb_setup_views["graph-B"] = create_eb_graph_view(graph_id="graph-B")
# eb_setup_views["graph-C"] = create_eb_graph_view(graph_id="graph-C")
# eb_setup_views["graph-C"] = create_eb_graph_view(graph_id="graph-C")

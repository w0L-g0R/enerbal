import dash_bootstrap_components as dbc
import dash_html_components as html

checklist = dbc.FormGroup(
    [
        dbc.Checklist(
            labelStyle={"margin-right": 24, "padding": 0, "font-size": 17},
            style={"margin-left": 88, },
            options=[
                {"label": "1988", "value": 1},
                {"label": "1989", "value": 2},
                {"label": "1990", "value": 3},
                {"label": "1991", "value": 4},
                {"label": "1992", "value": 5},
                {"label": "1993", "value": 6},
                {"label": "1994", "value": 7},
                {"label": "1995", "value": 8},
                {"label": "1996", "value": 9},
                {"label": "1997", "value": 10},
                {"label": "1998", "value": 11},
                {"label": "1999", "value": 12},
                {"label": "2000", "value": 13},
                {"label": "2001", "value": 14},
                {"label": "2002", "value": 15},
                {"label": "2003", "value": 16},
                {"label": "2004", "value": 17},
                {"label": "2005", "value": 18},
                {"label": "2006", "value": 19},
                {"label": "2007", "value": 20},
                {"label": "2008", "value": 21},
                {"label": "2009", "value": 22},
                {"label": "2010", "value": 23},
                {"label": "2011", "value": 24},
                {"label": "2012", "value": 25},
                {"label": "2013", "value": 26},
                {"label": "2014", "value": 27},
                {"label": "2015", "value": 28},
                {"label": "2016", "value": 29},
                {"label": "2017", "value": 30},
                {"label": "2018", "value": 31},
            ],
            value=list(range(13, 32)),
            inline=True,
            id="active-years",
        ),
    ]
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
                            # width=9,
                            children=[
                                html.H5("Years", className="card-title"), ],
                        ),
                        dbc.Col(
                            width=10,
                            children=[
                                dbc.ButtonGroup(
                                    style={"margin": 0},
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
                    # align="center",
                    style={"margin-top": 16, "margin-bottom": -28},
                    no_gutters=True,
                    children=[
                        dbc.Col(
                            # style={"margin-left": 24, "padding-right": 36},
                            children=[checklist],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

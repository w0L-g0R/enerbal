import inspect
import os
import pickle

import dash_html_components as html
import dash_table
import pandas as pd
from dash import callback_context
from dash.dependencies import Input, Output
from dash_table.Format import Format
from gui.app import app
from gui.assets.AEA_colors import provinces_color_table
from gui.utils import show_callback_context

from pandas import IndexSlice as IDX


# _________________________________________________________________________
# ///////////////////////////////////////////////////////////////// DISPATCH EL


def data_bars(df, column, color):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min() for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append(
            {
                "if": {
                    "filter_query": (
                        "{{{column}}} >= {min_bound}"
                        + (
                            " && {{{column}}} < {max_bound}"
                            if (i < len(bounds) - 1)
                            else ""
                        )
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    "column_id": column,
                },
                "background": (
                    """ 
                    linear-gradient(90deg,
                    {color} 0%,
                    {color} {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(
                        max_bound_percentage=max_bound_percentage, color=color
                    )
                ),
                "paddingBottom": 2,
                "paddingTop": 2,
            }
        )

    return styles


def create_on_update_data_table(graph_id: str):
    @app.callback(
        Output("table-graph-AB", "children"),
        [
            Input(f"graph-A-updates-table", "data"),
            Input(f"graph-B-updates-table", "data"),
        ],
    )
    def on_update_data_table(
        eev_data_A, eev_data_B,
    ):

        # Log callback information
        show_callback_context(
            func_name=inspect.stack()[0][3],
            file_name=inspect.stack()[0][1].rsplit(os.sep, 1)[-1].upper(),
            verbose=True,
        )

        # Get callback information to define the triggered input
        ctx = callback_context
        triggered = ctx.triggered

        if triggered:

            # Store the selected dropdown item in a variable
            triggered_prop_id = triggered[0]["prop_id"]
            midx = triggered[0]["value"]
            BL_IDX = midx["col_index"][0]
            ET_IDX = midx["col_index"][1]
            YEARS_IDX = midx["col_index"][2]

            eev_slice = pickle.load(open("eev_data.p", "rb"))

            table_name = "-".join([x for x in eev_slice.name if x != "Gesamt"])
            tables = []

            for energy_source in ET_IDX:

                df = pd.DataFrame(index=YEARS_IDX, columns=BL_IDX)

                for province in BL_IDX:

                    df[province] = eev_slice.loc[
                        IDX[province, energy_source, YEARS_IDX]
                    ].values.round(0)

                row_sum = df.sum(axis=0)

                df_row_sum = pd.DataFrame(data=row_sum, index=BL_IDX)

                df = df.T
                df["SUM"] = row_sum
                df = df.T

                pd.concat([df, df_row_sum.T], ignore_index=True)

                df["SUM"] = df.sum(axis=1)

                df.index.name = "Jahre"
                df.reset_index(inplace=True)

                columns = [
                    {"name": i, "id": i, "type": "numeric", "format": Format(group=",")}
                    for i in df.columns
                ]
                columns.pop(0)
                columns.insert(0, {"name": "Jahre", "id": "Jahre"})

                databars = [
                    data_bars(df.iloc[:-1, :], BL, provinces_color_table[BL] + "4D")
                    for BL in BL_IDX
                ]
                dbars = []
                for db in databars:
                    dbars += db

                headers = [
                    {
                        "if": {"column_id": BL},
                        "backgroundColor": provinces_color_table[BL] + "4D",
                        "fontWeight": "bold",
                    }
                    for BL in BL_IDX
                ]

                tables.append(html.H5(" - ".join([energy_source, table_name])))
                tables.append(html.Label(f"in TJ"))
                tables.append(
                    dash_table.DataTable(
                        columns=columns,
                        data=df.to_dict("records"),
                        style_cell={
                            "border": "1px solid black",
                            "color": "black",
                            "textAlign": "center",
                            "font-family": "Oswald-Light, sans-serif",
                            "font-size": 14,
                            "width": 64,
                        },
                        style_header_conditional=headers,
                        style_cell_conditional=[
                            {
                                "if": {"column_id": "SUM"},
                                "width": "72px",
                                # "backgroundColor": "azure",
                            },
                            {
                                "if": {"column_id": "Jahre"},
                                "width": "64px",
                                # "backgroundColor": "azure",
                                "color": "black",
                            },
                        ],
                        style_data_conditional=(dbars),
                    )
                )
                tables.append(html.Hr())
                # "{:,}".format(_sum, ",").replace(",", " ")
            # print('e: ', e)
            # for province in provinces:
            #     df[province] =

            # print('df: ', df)
            # df = eev_slice  # = eev_slice.droplevel(level=1, axis=0)
            # eev_slice = eev_slice.droplevel([0, 1], axis=1)

            # table = dash_table.DataTable(
            #     id='table',
            #     columns=[{"name": i, "id": i} for i in df.columns],
            #     data=df.to_dict('records'),
            # )

            # print('table: ', table)
            return html.Div(tables)
            # data_bars(df.iloc[:-1, :], 'Bgd',
            #           provinces_color_table["Bgd"],) +
            # data_bars(df.iloc[:-1, :], 'Ktn',
            #           provinces_color_table["Ktn"],) +
            # data_bars(df.iloc[:-1, :], 'Noe',
            #           provinces_color_table["Noe"],) +
            # data_bars(df.iloc[:-1, :], 'Ooe',
            #           provinces_color_table["Ooe"],) +
            # data_bars(df.iloc[:-1, :], 'Sbg',
            #           provinces_color_table["Sbg"],) +
            # data_bars(df.iloc[:-1, :], 'Stk',
            #           provinces_color_table["Stk"],) +
            # data_bars(df.iloc[:-1, :], 'Tir',
            #           provinces_color_table["Tir"],) +
            # data_bars(df.iloc[:-1, :], 'Vbg',
            #           provinces_color_table["Vbg"],) +
            # data_bars(df.iloc[:-1, :], 'Wie',
            #           provinces_color_table["Wie"],) +
            # data_bars(df.iloc[:-1, :], 'AT',
            #           provinces_color_table["AT"],)
            # if "graph-A" in triggered[0]["prop_id"]:

            # if "graph-B" in triggered[0]["prop_id"]:
            #     return eev_data_B

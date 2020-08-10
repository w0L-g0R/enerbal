from settings import provinces
from pathlib import Path
import pandas as pd
import pickle
import xlwings as xw
from typing import List, Union, Dict
import pandas as pd
from settings import provinces


def rgb_to_int(rgb):
    """Given an rgb, return an int"""
    return rgb[0] + (rgb[1] * 256) + (rgb[2] * 256 * 256)


def create_xlsx_chart(
    df: pd.DataFrame,
    xaxis_values: List,
    xaxis_title: str,
    yaxis_title: str,
    title: str,
    chart_type: Union[str, int],
    ws: str,
    source_data: xw.Range,
    series_names: List,
    color_table: Dict,
    # : List = None,
    height: int = 300,
    width: int = 500,
):

    # Chart objects
    chart = ws.charts.add()

    # Width
    chart.width = 500

    # Height
    chart.height = 300

    # Data
    chart.set_source_data(source_data)

    # Type
    # "column_clustered"
    # "bar"
    # "line"
    # line_markers
    chart.chart_type = "line"

    # Title
    chart.api[1].SetElement(2)  # Place chart title at the top

    # XValues
    chart.api[1].FullSeriesCollection(1).XValues = xaxis_values

    # Bar Gapwidth
    chart.api[1].ChartGroups(1).GapWidth = 20

    # Adding new series
    cht.api[1].SeriesCollection().NewSeries()
    # Editing new series source:
    ws.charts["Chart 1"].api[1].SeriesCollection(1).XValues = sht.range("A1:A12").value

    # if chart_type == "column_clustered":
    for enum, name in enumerate(series_names):
        print("province: ", name)
        color = rgb_to_int(color_table[province])
        print("color: ", color)
        chart.api[1].SeriesCollection(1).Points(
            enum + 1
        ).Format.Fill.ForeColor.RGB = color

        # chart.api[1].SeriesCollection(enum+1).Format.Line.ForeColor.RGB = color
    #        chart.api[1].SeriesCollection(enum+1).HasDataLabels = True

    # Axis title
    # chart.api[1].Axes(1).HasTitle = True  # Change text of the chart title
    chart.api[1].Axes(2).HasTitle = True  # Change text of the chart title
    # chart.api[1].Axes(1).AxisTitle.Text = xaxis_title
    chart.api[1].Axes(2).AxisTitle.Text = yaxis_title
    # chart.api[1].Axes(1).AxisTitle.Font.Bold = False
    chart.api[1].Axes(2).AxisTitle.Font.Bold = False

    # Ticklabels
    chart.api[1].Axes(1).TickLabels.Orientation = 0

    # Chart title
    chart.api[1].SetElement(2)
    chart.api[1].ChartTitle.Text = title

    chart.api[1].HasLegend = 1
    # chart.api[1].Legend.LegendEntries = "2018"

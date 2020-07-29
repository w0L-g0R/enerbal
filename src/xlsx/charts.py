from settings import provinces_names
from pathlib import Path
import pandas as pd
import pickle
import xlwings as xw
from typing import List, Union
import pandas as pd
from settings import provinces_names
from gui.assets.AEA_colors import provinces_color_table_rgb


def rgb_to_int(rgb):
    """Given an rgb, return an int"""
    return rgb[0] + (rgb[1] * 256) + (rgb[2] * 256 * 256)


def xlsx_chart(
    df: pd.DataFrame,
    xaxis_values: List,
    xaxis_title: str,
    yaxis_title: str,
    title: str,
    chart_type: Union[str, int],
    ws: str,
    source_data: xw.Range,
    provinces: List,
    years: List = None,
    height: int = 300,
    width: int = 500,
):

    chart = ws.charts.add()
    chart.width = 500
    chart.height = 300

    chart.set_source_data(source_data)
    chart.chart_type = chart_type

    chart.api[1].SetElement(2)  # Place chart title at the top
    chart.api[1].FullSeriesCollection(1).XValues = xaxis_values
    chart.api[1].ChartGroups(1).GapWidth = 20

    # if chart_type == "column_clustered":
    for enum, province in enumerate(provinces):
        print('province: ', province)
        color = rgb_to_int(provinces_color_table_rgb[province])
        print('color: ', color)
        # chart.api[1].SeriesCollection(1).Points(
        #     enum+1).Format.Fill.ForeColor.RGB = color
        chart.api[1].SeriesCollection(enum+1).Format.Line.ForeColor.RGB = color
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

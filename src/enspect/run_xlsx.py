import io
import logging
import pickle
import sys
from pathlib import Path
from pprint import pprint

import pandas as pd
import xlwings as xw

from enspect.aggregates.common import provinces

# from enspect.xlsx.workbook import xlsx
from enspect.aggregates.eb import (
    eev_aggregates,
    eev_generation,
    energy_aggregate_lookup,
)
from enspect.logger.setup import setup_logging
from enspect.models.dataset import DataSet

# from enspect.models.workbook import xlsx
from enspect.models.utils import close_xlsx
from enspect.models.workbook import Workbook
from enspect.paths import file_paths

# ////////////////////////////////////////////////////////////////////// INPUTS

setup_logging(
    console_log_actived=True, console_log_filter=None, console_out_level=logging.DEBUG,
)

nea_energy_sources = [
    "Steinkohle",
    "Insgesamt",
    # "GAS",
]

nea_sectors = [
    "Gesamt (ohne E1 - E7)",
    "Produzierender Bereich Gesamt",
    "Transport Gesamt",
    "Offentliche und Private Dienstleistungen",
    "Private Haushalte",
    "Landwirtschaft",
]

nea_usage_categories = [
    "Raumheizung und Klimaanlagen",
    "Dampferzeugung",
    # "Industrieöfen",
    # "Standmotoren",
    # "Traktion",
    # "Beleuchtung und EDV",
    # "Elektrochemische Zwecke",
    # "Summe",
]


# years = list(range(2005, 2010, 1))
years = [2018]
print("years: ", years)

# /////////////////////////////////////////////////////////////// CREATE DATASET

ds = DataSet(name=f"Set_1", file_paths=file_paths)

# //////////////////////////////////////////////////////////////////////// STATS
# ds.add_stats_data_per_years(
#     name="Bevölkerungsstatisik",
#     file="pop", years=years, provinces=provinces,
# )

# ds.add_stats_data_per_years(
#     name="Fahrleistung_PKW",
#     file="km_pkw", years=years, provinces=provinces,
# )

# /////////////////////////////////////////////////////////////////////////// EB
# for aggregate in eb_aggregates:

logging.getLogger().error("/" * 80)

ds.add_nea_data(
    energy_sources=nea_energy_sources,
    balance_aggregates=nea_sectors,
    usage_categories=nea_usage_categories,
    years=years,
    provinces=provinces,
    # stacked_usage_categories=True,
    # stacked_balance_aggregates=True,
    stacked_energy_sources=True,
    stacked_usage_category=True,
    # stacked_balance_aggregate=True,
    # stacked_energy_source=True,
    # per_years=per_years,
)

filename = Path.cwd() / "wings.xlsx"
print("filename: ", filename)

# with open(filename, "rb") as f:
#     file = io.BytesIO(f.read())

wb = xw.Book(filename)

# close_xlsx()

# wb = Workbook(name="WB1", filename=filename)

# wb = xlsx(name="WB1", filename=filename)
# wb.add_sheets(sheets=["EEV", "BIV", "THG"])
# # try:
# #     wb.close()
# # except BaseException:


# wb = xw.Book(filename)
sht = wb.sheets["Sheet1"]
adress = "A1"
for data in ds.objects:

    print(id(data))
    print("data ID: ", data.key)
    sht.range(adress).value = data.frame
    adress = xw.Range("A2").end("down").offset(2, 0).address

#     # if data.order == "data.frane":

# wb.write_to_sheet(data=data, sheet="EEV")
# else:
#     wb.write(data=data, sheet=data.aggregate)


# wb.book.save(wb.path)
# wb.launch()

# for sheet in wb.book.sheetnames:
#     print("sheet: ", sheet)

#     dimension = wb.book[sheet].calculate_dimension()
#     wb.book[sheet].move_range(dimension, rows=0, cols=10)

#     wb.style(ws=wb.book[sheet])


# print('wb: ', wb.worksheets)

# for data in kpi_data:
# print(data.frame)
# for ds in graphs:
#     ds.write_to_sheet(
#         scaled="absolute", aggregates=["Bruttoinlandsverbrauch"],
#     )


# print("ds: ", ds)

# pprint(sorted(g_data))

# kpi_data = [v for v in ds.objects.filter(is_KPI=True)]


# for sector in sectors:
#     # ////////////////////////////////////////////////////////////////// EB IND
#     ds.add_indicator(

#         aggregate=aggregate,

#         numerator=[
#             data for data in ds.objects.filter(
#                 name__contains=aggregate + "_Gesamtenergiebilanz", order="per_years")
#         ],

#         denominator=[
#             data for data in ds.objects.filter(
#                 file="pop")
#         ],

#     )
# ////////////////////////////////////////////////////////////////////////// NEA

# ds.add_nea_data_per_years(
#     file="nea",
#     energy_sources=nea_energy_sources,
#     years=years,
#     provinces=provinces,
# )
# ////////////////////////////////////////////////////////////////////// OVERLAY

# ds.add_overlay(
#     to_data=[
#         data for data in ds.objects.filter(
#             name__startswith="Bruttoinlandsverbrauch",
#             order="per_years",
#             is_KPI=False
#         )
#     ],
#     overlays=[
#         data for data in ds.objects.filter(
#             file="km_pkw")
#     ],
#     scalings="absolute",
#     chart_type="line",
# )

# /////////////////////////////////////////////////////////////// FILTER DATASET

# g_data = [
#     v
#     for v in ds.objects.filter(
#         # order="per_sector",
#         # aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
#         # is_KPI=False
#     )
# ]

# /////////////////////////////////////////////////////////////// FILTER DATASET

# ov_data = [
#     v.unit
#     for v in ds.objects.filter(
#         # order="per_years",
#         balance_aggregates__in=["Energetischer Endverbrauch"],
#         # is_KPI=False
#         # has_overlay=True
#     )
# ]

# print("ov_data: ", ov_data)
# g_data_names = [x.name for x in g_data]
# g_size = [sys.getsizeof(x) for x in g_data]

# pprint(f'{g_data_names}')
# pprint(f'{g_size}')

# print(g_data)
# //////////////////////////////////////////////////////////////// WRITE TO XLSX

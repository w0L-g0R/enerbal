import sys
import logging
from pathlib import Path
from pprint import pprint

from settings import file_paths, provinces
from models.dataset import DataSet
from logger.setup import setup_logging
from xlsx.utils import get_workbook, write_to_sheet

from xlsx.workbook import xlsx
from conversion.energiebilanzen.data_structures import energy_sources_aggregates

# ////////////////////////////////////////////////////////////////////// INPUTS

setup_logging(
    console_log_actived=True, console_log_filter=None, console_out_level=logging.DEBUG,
)

eb_aggregates = [
    "Bruttoinlandsverbrauch",
]

# eb_sectors = [
#     "Energetischer Endverbrauch",
#     # "Produzierender Bereich",
#     # "Verkehr",
#     # "Öffentliche und Private Dienstleistungen",
#     # "Private Haushalte",
#     # "Landwirtschaft",
# ]
# aggregates = ["Bruttoinlandsverbrauch"]

eb_energy_sources = [
    "Elektrische Energie",
    # ]
    "Wasserkraft",
    "Wind",
    "Photovoltaik",
    "KOHLE",
    "ÖL",
    # "GAS",
    # "Sonst. Biogene fest",
    # "Hausmüll Bioanteil",
    # "Scheitholz",
    # "Pellets+Holzbriketts",
    # "Holzabfall",
    # "Holzkohle",
    # "Ablaugen",
    # "Bioethanol",
    # "Biodiesel",
    # "Sonst. Biogene flüssig",
    # "Deponiegas",
    # "Klärgas",
    # "Biogas"
]

# eb_energy_sources = (
#     energy_sources_aggregates["Fossil-fest"]
#     + energy_sources_aggregates["Fossil-flüssig"]
#     + energy_sources_aggregates["Fossil-gasförmig"]
#     + ["Elektrische Energie", "Fernwärme", "Umgebungswärme"]
#     + energy_sources_aggregates["Biogen-fest"]
#     + energy_sources_aggregates["Biogen-flüssig"]
#     + energy_sources_aggregates["Biogen-gasförmig"]
# )
nea_energy_sources = [
    "Steinkohle",
    "Insgesamt",
    # "GAS",
]

nea_sectors = [
    "Ö Gesamt (ohne E1 - E7)",
    "Produzierender Bereich Gesamt",
    "Transport Gesamt ",
    "Offentliche und Private Dienstleistungen",
    "Private Haushalte",
    "Landwirtschaft",
]

years = list(range(2005, 2019, 1))
years = [2018]

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

ds.add_eb_data(
    energy_sources=eb_energy_sources,
    balance_aggregates=eb_aggregates,
    years=years,
    provinces=provinces,
    conversion="TJ_2_TWh",
    per="sources_for_each_agg_and_year"
    # 1) sources_for_each_agg_and_year
    # 2) aggs_for_each_source_and_year
    # 3) agg_and_source_for_all_years
)

# ds.add_eb_data_per_sector(
#     file="sec",
#     energy_sources=eb_energy_sources,
#     aggregate=aggregate,
#     # years=[2016, 2017],
#     years=years,
#     provinces=provinces,
#     conversion="TJ_2_TWh",
#     sectors=eb_sectors
# )

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

g_data = [
    v
    for v in ds.objects.filter(
        # order="per_sector",
        # aggregate__in=["Bruttoinlandsverbrauch", "Importe"],
        # is_KPI=False
    )
]

# /////////////////////////////////////////////////////////////// FILTER DATASET

ov_data = [
    v.unit
    for v in ds.objects.filter(
        # order="per_years",
        aggregate__in=["Energetischer Endverbrauch"],
        # is_KPI=False
        # has_overlay=True
    )
]

print("ov_data: ", ov_data)
# g_data_names = [x.name for x in g_data]
# g_size = [sys.getsizeof(x) for x in g_data]

# pprint(f'{g_data_names}')
# pprint(f'{g_size}')

# print(g_data)
# //////////////////////////////////////////////////////////////// WRITE TO XLSX

wb = xlsx(name="WB1", path="test.xlsx", sheets=eb_aggregates)
try:
    wb.close()
except BaseException:
    pass

for data in g_data:

    # if data.order == "per_sector":

    wb.write(data=data, sheet=data.aggregate)
    # else:
    #     wb.write(data=data, sheet=data.aggregate)


for sheet in wb.book.sheetnames:
    print("sheet: ", sheet)

    dimension = wb.book[sheet].calculate_dimension()
    wb.book[sheet].move_range(dimension, rows=0, cols=10)

    wb.style(ws=wb.book[sheet])

wb.book.save(wb.path)
wb.launch()

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

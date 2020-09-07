import datetime
import logging
from pathlib import Path
from typing import Dict, List, Union
from collections import OrderedDict

import numpy as np
import pandas as pd
from enspect.logger.setup import setup_logging
from enspect.paths import file_paths
from enspect.utils import timeit
from enspect.aggregates.common import provinces

from pprint import pprint
import PyPDF2
from pandas import IndexSlice as IDX
from copy import copy


@timeit
def fetch_from_xlsx(file: str):

    return pd.read_excel(
        io=file, sheet_name=None, na_filter=False, index_col=0, header=0
    )


def create_thg_col_midx(
    last_year: int, sectors: List, energy_usage_types: List,
) -> pd.MultiIndex:
    years = [x for x in range(1993, last_year + 1, 1)]

    midx = pd.MultiIndex.from_product(
        [provinces, sectors, energy_usage_types, years], names=["PROV", "SRC", "YEAR"],
    )

    return midx


# def parse_pdf(provinces: List):

# Helper functions
# def chunks(lst, n):
#     """Yield successive n-sized chunks from lst."""
#     for i in range(0, len(lst), n):
#         yield lst[i : i + n]

# def is_float(value):
#     try:
#         float(value)
#         return True
#     except ValueError:
#         return False

# files = (
#     file_paths["folder_thg"] / "THG_1990_2006.xlsx",
#     file_paths["folder_thg"] / "THG_2000_2017.xlsx",
#     file_paths["folder_thg"] / "THG_ETS_2005_2017.xlsx",
# )

# dfs = []

# for file in files:
#     dfs.append(fetch_from_xlsx(file=file))

# headers = [
#     # THG_1990_2006.pdf:
#     iter(
#         [
#             "THG-Emissionen des Burgenlands in 1.000 t CO",
#             "THG-Emissionen Kärntens in 1.000 t CO",
#             "THG-Emissionen Niederösterreichs in 1.000 t CO",
#             "THG-Emissionen Oberösterreichs in 1.000 t CO",
#             "THG-Emissionen Salzburgs in 1.000 t CO",
#             "THG-Emissionen der Steiermark in 1.000 t CO",
#             "THG-Emissionen Tirols in 1.000 t CO",
#             "THG-Emissionen Vorarlbergs in 1.000 t CO",
#             "THG-Emissionen Wiens in 1.000 t CO",
#             # "THG-Emissionen AT",
#         ]
#     ),
#     # THG_2000_2017.pdf
#     iter(
#         [
#             "THG-Emissionen des Burgenlandes in 1.000 t CO",
#             "THG-Emissionen Kärntens in 1.000 t CO",
#             "THG-Emissionen Niederösterreichs in 1.000 t CO",
#             "THG-Emissionen Oberösterreichs in 1.000 t CO",
#             "THG-Emissionen Salzburgs in 1.000 t CO",
#             "THG-Emissionen der Steiermark in 1.000 t CO",
#             "THG-Emissionen Tirols in 1.000 t CO",
#             "THG-Emissionen Vorarlbergs in 1.000 t CO",
#             "THG-Emissionen Wiens in 1.000 t CO",
#             # "THG-Emissionen AT",
#         ]
#     ),
# ]
#     pprint(files)

#     emittents = [
#         # THG_1990_2006.pdf
#         [
#             "Energie",
#             "Kleinverbraucher",
#             "Industrie",
#             "Verkehr",
#             "Landwirtschaft",
#             "Sonstige",
#             "Gesamt",
#         ],
#         # THG_2000_2017.pdf
#         [
#             "Energie",
#             "Industrie",
#             "Verkehr",
#             "Gebäude",
#             "Landwirtschaft",
#             "Abfallwirtschaft",
#             "Fluorierte Gase",
#             "Gesamt",
#         ],
#     ]
#     # sources = iter(["Total", "ETS", "Non-ETS"])
#     y_1 = range(1990, 2006 + 1)
#     y_2 = [1990, 1995]
#     y_2.extend([x for x in range(2000, 2018 + 1)])
#     # y.insert(0, (1990, 1995))
#     print("y: ", y_2)

#     years_per_file = [
#         y_1,
#         y_2
#         # range(2005, 2017 + 1),
#     ]
#     dfs = []

#     for file, years, emmitent in zip(files, years_per_file, emittents):

#         provinces = iter(
#             [
#                 "Burgenland",
#                 "Kärnten",
#                 "Niederösterreich",
#                 "Oberösterreich",
#                 "Salzburg",
#                 "der Steiermar",
#                 "Tirol",
#                 "Vorarlberg",
#                 "Wien",
#             ]
#             # "THG-Emissionen AT",
#         )

#         # header = copy(header)
#         provinces = iter(provinces)

#         # print("\nfile: ", file)
#         # Open pdf
#         pdf = open(file, "rb")

#         # Create reader instance
#         reader = PyPDF2.PdfFileReader(pdf)

#         # Iter over pa
#         for page_nr in range(reader.numPages):

#             page = reader.getPage(page_nr)
#             data = page.extractText()
#             data = data.split("\n")  # output type: List

#             next_province_1 = next(provinces)
#             header_idx_1 = list(filter(lambda x: next_province_1 in x, data))
#             header_idx_1 = data.index(header_idx_1[0])
#             header_1 = data[header_idx_1]

#             try:

#                 next_province_2 = next(provinces)
#                 header_idx_2 = list(filter(lambda x: next_province_2 in x, data))
#                 header_idx_2 = data.index(header_idx_2[0])

#                 # header_idx_2 = data.index(next(header))
#                 header_2 = data[header_idx_2]

#             except StopIteration:
#                 header_2 = "AT"
#                 pass

#             table_1 = [
#                 int(x.replace(".", ""))  # .astype(int)
#                 for x in data[header_idx_1:header_idx_2]
#                 if is_float(x)
#             ]

#             table_2 = [
#                 int(x.replace(".", ""))  # .astype(int)
#                 for x in data[header_idx_2:]
#                 if is_float(x)
#             ]

#             for table, header, province in zip(
#                 [table_1, table_2],
#                 [header_1, header_2],
#                 [next_province_1, next_province_2],
#             ):

#                 if header == "AT":

#                     # print("df: ", df.head())

#                     break

#                 df = pd.DataFrame(data=list(chunks(table, len(list(years)))),)

#                 # Set first row as column YEAR index
#                 df.columns = df.iloc[0, :].astype(int)

#                 # Drop year row
#                 df.drop(labels=0, axis=0, inplace=True)

#                 # Set emittents as row BAGG_0
#                 df.index = emmitent

#                 df.index.name = "BAGG_0"

#                 df.columns = pd.MultiIndex.from_product(
#                     iterables=[[province], ["Total"], df.columns],
#                     names=["PROV", "ES", "YEAR",],
#                 )

#                 print("\ndf: ", df)
#                 dfs.append(df)

#     df = pd.concat(dfs, axis=1).sort_index()

#     df_AT = df.groupby(level="YEAR", axis=1).sum()
#     df_AT.columns = pd.MultiIndex.from_product(
#         iterables=[["AT"], ["Total"], years], names=["PROV", "ES", "YEAR",],
#     )
#     df = pd.concat([df_AT, df], axis=1)
#     print("\ndf_fineal: ", df.head())

#     return

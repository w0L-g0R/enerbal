from pathlib import Path
from pprint import pprint
import pickle
from enspect.settings import file_paths, provinces

# from enspect.models.dataset import DataSe

# from enspect.logger.setup import setup_logging
# from enspect.xlsx.utils import get_workbook, write_to_sheet

# from enspect.xlsx.workbook import xlsx
from enspect.conversion.energiebilanzen.data_structures import (
    energy_sources_aggregates,
    eev_aggregates,
)
from conversion.energiebilanzen.data_structures import (
    eb_sheet_names,
    eb_aggregate_names,
)
from enspect.models.utils import extend_balance_aggregates_index
from typing import Union
import pandas as pd

IDX = pd.IndexSlice

data = pickle.load(open(file_paths["db_pickles"] / "eb.p", "rb"))

# sources_for_each_agg_and_year
aggregates = eev_aggregates

energy_sources = (
    energy_sources_aggregates["Fossil-fest"]
    + energy_sources_aggregates["Fossil-flüssig"]
    + energy_sources_aggregates["Fossil-gasförmig"]
    + ["Elektrische Energie", "Fernwärme", "Umgebungswärme"]
    + energy_sources_aggregates["Biogen-fest"]
    + energy_sources_aggregates["Biogen-flüssig"]
    + energy_sources_aggregates["Biogen-gasförmig"]
)
print("energy_sources: ", energy_sources)

years = [2000, 2018]


sectors = [
    "Öffentliche und Private Dienstleistungen",
    "Private Haushalte",
    "Landwirtschaft",
    "Produzierender Bereich",
    "Verkehr",
    "Sonstige",
]

aggregates = sectors + ["Energetischer Endverbrauch "]


# data.columns = pd.MultiIndex.from_product([list(data.columns), eb_aggregate_names])

# data.columns = eb_col_midx

eb_df = data.loc[
    IDX[aggregates, :, :, :, :], IDX[provinces, energy_sources, years],
]

# eb_df
# print("eb_df: ", eb_df)

# aggregates = extend_balance_aggregates_index(
#     balance_aggregates=aggregates, add_all=True
# )

# eb_df = data.loc[
#     aggregates, IDX[provinces, energy_sources, years],
# ]

eb_df = eb_df.droplevel(level=[1, 2, 3, 4])

# et_group = eb_df.groupby(level=1, axis=1)[energy_sources_aggregates["Fossil-fest"]]
fossil_fest = energy_sources_aggregates["Fossil-fest"]

et_group = eb_df.groupby(level=1, axis=1)  # [tuple(fossil_fest)]

# filter e-aggs
l = et_group.filter(lambda x: x.columns.get_level_values(1).unique() in fossil_fest)
print("l: ", l)

year_group = l.groupby(level=2, axis=1)
year = year_group.get_group(2000).sum()
f = year.groupby(level=0, axis=0).sum()
print("f: ", f)

# print("year: ", year)
# for et, frame in et_group:
#     print(et)
#     print(frame.columns.get_level_values(1).unique())
#     print("frame: ", frame)
#     print()
# # g = et_group.get_group("Steinkohle")
# print("g : ", g)

# print(eb_df)

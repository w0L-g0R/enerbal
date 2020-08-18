#%%
import sys
import logging
from pathlib import Path
from pprint import pprint
import pickle
from enspect.settings import file_paths, provinces

# from enspect.models.dataset import DataSe

# from enspect.logger.setup import setup_logging
# from enspect.xlsx.utils import get_workbook, write_to_sheet

# from enspect.xlsx.workbook import xlsx
from enspect.conversion.energiebilanzen.data_structures import energy_sources_aggregates
from enspect.models.utils import extend_balance_aggregates_index
from typing import Union
import pandas as pd

IDX = pd.IndexSlice
# %%
data = pickle.load(open(file_paths["db_pickles"] / "eb.p", "rb"))

# sources_for_each_agg_and_year
#%%
aggregates = ["Energetischer Endverbrauch", "Importe", "Umwandlungsausstoß"]

energy_sources = [
    "Gesamtenergiebilanz",
    "Elektrische Energie",
    "Fernwärme",
    "Brennbare Abfälle",
    "ERNEUERBARE",
    "KOHLE",
    "ÖL",
    "GAS",
]

years = [2000, 2018]

# %%
aggregates = extend_balance_aggregates_index(
    balance_aggregates=aggregates, add_all=True
)
#%%
aggregates
#%%
eb_df = data.loc[
    IDX[aggregates], IDX[provinces, energy_sources, years],
]


# %%

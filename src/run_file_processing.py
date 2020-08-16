# from settings import file_paths
from pathlib import Path
from typing import Union, List, Dict
import pandas as pd

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

import pickle
import numpy as np
from time import time, ctime

import logging

from converter.energiebilanzen.to_dataframe import convert_energy_balances_to_dataframe
from converter.energiebilanzen.data_structures import eb_sheet_names
from converter.nea.processing.convert_nea_to_dataframe import convert_nea_to_df
from converter.nea.processing.get_nea_sheets import (
    sectors,
    energy_usage_types,
    energy_sources_93_98,
    energy_sources_99_plus,
    energy_sources_nea_df,
    energy_sources_nea_df_reindex,
)

from paths import file_paths

IDX = pd.IndexSlice
# ////////////////////////////////////////////////////////////////////// EB


convert_energy_balances_to_dataframe(
    # balances_directory_path=balances_directory_path,
    # row_indices_file_path=row_indices_file_path,
    last_year=2018,
)

eb_data = pickle.load(open(file_paths["pickles"] / Path("eb_df.pkl"), "rb"),)


energy_source = "Gesamtenergiebilanz"

eb_slice = eb_data.loc[
    IDX["Energetischer Endverbrauch", "Gesamt", "Gesamt", "Gesamt", "Gesamt"],
    IDX["AT", energy_source, :],
]
print("eb_slice: ", eb_slice)

res_data = pickle.load(open(file_paths["pickles"] / Path("res_df.pkl"), "rb"),)
res_df.loc[IDX[:], IDX["AT", :]]

# ////////////////////////////////////////////////////////////////////// NEA

# balances_directory_path = file_paths["nea_data_dir"]
# print("balances_directory_path: ", balances_directory_path)

# energy_sources = {
#     "nea_df": energy_sources_nea_df,
#     "<1999": energy_sources_93_98,
#     ">=1999": energy_sources_99_plus,
# }


# start = time.time()
# print("###########################################################################")
# print("start: ", start)
# convert_nea_to_df(
#     balances_directory_path=balances_directory_path,
#     sectors=sectors,
#     energy_usage_types=energy_usage_types,
#     energy_sources=energy_sources,
#     last_year=2018,
# )
# end = time.time()
# print("end: ", end)
# print(end - start)

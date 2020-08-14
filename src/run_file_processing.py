from settings import file_paths
from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np
import time


from files.energiebilanzen.convert.balances_to_dataframe import eb_to_df
from files.energiebilanzen.convert.get_eb_data_structures import eb_sheets

from files.nea.processing.convert_nea_to_dataframe import convert_nea_to_df

from files.nea.processing.get_nea_sheets import (
    sectors,
    energy_usage_types,
    energy_sources_93_98,
    energy_sources_99_plus,
    energy_sources_nea_df,
    energy_sources_nea_df_reindex,
)

# ////////////////////////////////////////////////////////////////////// EB

balances_directory_path = file_paths["eb_data_dir"]
print("balances_directory_path: ", balances_directory_path)

row_indices_file_path = file_paths["eb_row_indices"]
print("row_indices_file_path: ", row_indices_file_path)

start = time.time()
print("###########################################################################")
print("start: ", start)
convert_eb_to_df(
    balances_directory_path=balances_directory_path,
    row_indices_file_path=row_indices_file_path,
    last_year=2018,
)
end = time.time()
print("end: ", end)
print(end - start)
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

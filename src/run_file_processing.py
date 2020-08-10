from files.energiebilanzen.processing.convert_eb_to_dataframe import convert_eb_to_df
from files.energiebilanzen.processing.eb_sheets import eb_sheets
from settings import file_paths
from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np
import time

# ////////////////////////////////////////////////////////////////////// INPUTS

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

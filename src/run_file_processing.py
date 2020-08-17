# from settings import file_paths
from conversion.thg.to_dataframe import convert_thg_to_dataframe
from conversion.nea.to_dataframe import convert_nea_to_dataframe
from conversion.energiebilanzen.data_structures import eb_sheet_names
from conversion.energiebilanzen.to_dataframe import convert_energy_balances_to_dataframe
from paths import file_paths
import logging
from time import time, ctime
import numpy as np
import pickle
from pathlib import Path
from typing import Union, List, Dict
import pandas as pd

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000


IDX = pd.IndexSlice

# ////////////////////////////////////////////////////////////////////// EB


# convert_energy_balances_to_dataframe(last_year=2018,)
# ////////////////////////////////////////////////////////////////////// NEA


# convert_nea_to_dataframe(
#     last_year=2018,
# )

# ////////////////////////////////////////////////////////////////////// NEA


convert_thg_to_dataframe()

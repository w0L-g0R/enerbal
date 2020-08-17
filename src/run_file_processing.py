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

from paths import file_paths

IDX = pd.IndexSlice

# ////////////////////////////////////////////////////////////////////// EB

from conversion.energiebilanzen.to_dataframe import convert_energy_balances_to_dataframe
from conversion.energiebilanzen.data_structures import eb_sheet_names

convert_energy_balances_to_dataframe(last_year=2018,)
# ////////////////////////////////////////////////////////////////////// NEA

from conversion.nea.to_dataframe import convert_nea_to_dataframe


# convert_nea_to_dataframe(
#     last_year=2018,
# )

# ////////////////////////////////////////////////////////////////////// NEA

# from conversion.thg.to_dataframe import convert_thg_to_dataframe

# convert_thg_to_dataframe()

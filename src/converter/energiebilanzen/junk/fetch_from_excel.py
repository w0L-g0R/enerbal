from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np

# from converter.energiebilanzen.data_structures import eb_sheets_names

# # //////////////////////////////////////////////////////// FETCH_ENERGY_SOURCES


# def fetch_energy_sources(balances_file_path: str, years_range_data: pd.Series):

#     # Extract all sheets (=energieträger) from file at once
#     # NOTE: pd.read_excel with sheet_name=None creates a dictionary (=> energy_sources_sheets)

#     print("balances_file_path: ", balances_file_path)

#     # Exclude columns with years '70 until '88
#     if "AT" in balances_file_path:

#         energy_sources_sheets = pd.read_excel(
#             io=str(balances_file_path),
#             sheet_name=None,
#             na_filter=False,
#             usecols="A,T:AX",
#         )

#         energy_sources_sheets["Mischgas"] = pd.read_excel(
#             io=str(balances_file_path),
#             sheet_name="Mischgas",
#             na_filter=False,
#             usecols="A,P:X",
#         )

#         # NOTE: Only appears in "ET_AT_70_18"
#         del energy_sources_sheets["Generatorgas"]

#     else:
#         energy_sources_sheets = pd.read_excel(
#             io=str(balances_file_path), sheet_name=None, na_filter=False,
#         )

#     # NOTE: Helpers, to be removed
#     # pickle.dump(energy_sources_sheets, open("energy_sources_sheets.p", "wb"))
#     # energy_sources_sheets = pickle.load(open("energy_sources_sheets.p", "rb"))

#     # Delete non-data related sheets
#     del energy_sources_sheets["Deckblatt"]
#     del energy_sources_sheets["Grundbegriffe"]
#     del energy_sources_sheets["Klassifikation"]
#     del energy_sources_sheets["Wirkungsgrade"]

#     # Delete hidden sheets if existing
#     try:
#         del energy_sources_sheets["checkFormal"]
#     except:
#         pass

#     # NOTE: RES sheet names differ (=> "EU-Richtlinie" vs. "EU Richtlinie")
#     try:
#         # Extract "Erneuerbaren RL" to a seperate variable
#         res_sheet = energy_sources_sheets["Erneuerbare EU Richtlinie"].copy()

#         del energy_sources_sheets["Erneuerbare EU Richtlinie"]

#     except:

#         # Extract "Erneuerbaren RL" to a seperate variable
#         res_df = energy_sources_sheets["Erneuerbare EU-Richtlinie"].copy()

#         del energy_sources_sheets["Erneuerbare EU-Richtlinie"]

#     energy_sources_sheets = correct_file_errors(
#         energy_sources_sheets=energy_sources_sheets
#     )

#     return energy_sources_sheets, res_sheet


# def correct_file_errors(energy_sources_sheets: Dict):
#     # CHECK 2: Find unintended sheets in the excel file
#     fetched_sheets = list(energy_sources_sheets.keys())
#     unintended_sheets = set(eb_sheets).symmetric_difference(fetched_sheets)

#     mismatches = [
#         energy_source
#         for energy_source in fetched_sheets
#         if energy_source not in eb_sheets
#     ]

#     print("Mismatches: ", mismatches)
#     assert (
#         len(unintended_sheets) == 0
#     ), "There are some unintended sheets in the fetched xlsx file. Delete or rename those sheet_names with the corresponding names from 'eb_sheets.py'!"

#     # ////////////////////////////// KNOWN ERROR 1: Mischgas ends at year "1995"

#     # Replace missing years in column index
#     add_on = years[len(energy_sources_sheets["Mischgas"].columns) - 1 :]

#     df_dummy_columns = pd.DataFrame(
#         index=range(len(energy_sources_sheets["Mischgas"])), columns=add_on
#     )

#     energy_sources_sheets["Mischgas"] = pd.concat(
#         [energy_sources_sheets["Mischgas"], df_dummy_columns], axis="columns"
#     )

#     # /////////////////// KNOWN ERROR 2:  Misses name "Gesamt" at row 475
#     for source in ["Erdgas", "Elektrische Energie"]:

#         energy_sources_sheets[source].iloc[474, 0] = "Gesamt"

#     for source in ["GAS", "ERNEUERBARE", "ABFÄLLE", "Gesamtenergiebilanz"]:

#         energy_sources_sheets[source].iloc[237, 0] = "Gesamt"

#     return energy_sources_sheets

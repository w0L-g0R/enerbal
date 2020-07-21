from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np

# //////////////////////////////////////////////////////// FETCH_ENERGY_SOURCES


def fetch_energy_sources(
    balances_file_path: str, eb_sheets: List, years_range_data: pd.Series
):

    # Extract all sheets (=energieträger) from file at once and save them to a dictionary

    print("balances_file_path: ", balances_file_path)

    if "AT" in balances_file_path:
        dfs = pd.read_excel(
            io=str(balances_file_path),
            sheet_name=None,
            na_filter=False,
            usecols="A,T:AX",
        )

        dfs["Mischgas"] = pd.read_excel(
            io=str(balances_file_path),
            sheet_name="Mischgas",
            na_filter=False,
            usecols="A,P:X",
        )

    else:
        dfs = pd.read_excel(
            io=str(balances_file_path), sheet_name=None, na_filter=False,
        )

    # NOTE: Helpers to be removed
    # pickle.dump(dfs, open("dfs.p", "wb"))
    # dfs = pickle.load(open("dfs.p", "rb"))

    # Delete unnecessary sheets
    del dfs["Deckblatt"]
    del dfs["Grundbegriffe"]
    del dfs["Klassifikation"]
    del dfs["Wirkungsgrade"]

    # NOTE: Hidden sheets
    try:
        del dfs["checkFormal"]
    except:
        pass

    # NOTE: Sheet names differ
    try:
        # Extract "Erneuerbaren RL" to a seperate variable
        renewables_df = dfs["Erneuerbare EU Richtlinie"].copy()

        del dfs["Erneuerbare EU Richtlinie"]

    except:

        # Extract "Erneuerbaren RL" to a seperate variable
        renewables_df = dfs["Erneuerbare EU-Richtlinie"].copy()

        del dfs["Erneuerbare EU-Richtlinie"]

    # CHECK 2: Find unintended sheets in the excel file
    fetched_sheets = list(dfs.keys())
    unintended_sheets = set(eb_sheets).symmetric_difference(fetched_sheets)

    assert (
        len(unintended_sheets) == 0
    ), "There are some unintended sheets in the xlsx file"

    # ////////////////////////////// KNOWN ERROR 1: Mischgas ends at year "1995"

    # Replace missing years in column index
    add_on = years_range_data[len(dfs["Mischgas"].columns) - 1 :]

    df_dummy_columns = pd.DataFrame(index=range(len(dfs["Mischgas"])), columns=add_on)

    dfs["Mischgas"] = pd.concat([dfs["Mischgas"], df_dummy_columns], axis="columns")

    # /////////////////// KNOWN ERROR 2:  Misses name "Gesamt" at row 475
    for source in ["Erdgas", "Elektrische Energie"]:

        dfs[source].iloc[474, 0] = "Gesamt"

    for source in ["GAS", "ERNEUERBARE", "ABFÄLLE", "Gesamtenergiebilanz"]:

        dfs[source].iloc[237, 0] = "Gesamt"

    return dfs, renewables_df

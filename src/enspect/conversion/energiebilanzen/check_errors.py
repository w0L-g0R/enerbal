from pathlib import Path
from typing import List, Dict
import pandas as pd
import logging
from conversion.energiebilanzen.data_structures import eb_sheet_names
from utils import timeit


@timeit
def check_sheetname_errors(energy_sources_sheets: Dict, years: List):

    # CHECK 2: Find unintended sheets in the excel file
    fetched_sheets = list(energy_sources_sheets.keys())
    unintended_sheets = set(eb_sheet_names).symmetric_difference(fetched_sheets)

    mismatches = [
        energy_source
        for energy_source in fetched_sheets
        if energy_source not in eb_sheet_names
    ]

    if mismatches:
        # Track sheet name errors
        logging.getLogger().debug(
            "Found naming mismatch for sheet: {}".format(mismatches)
        )

    assert (
        len(unintended_sheets) == 0
    ), "There are some unintended sheets in the fetched xlsx file. Delete or rename those sheet_names with the corresponding names from 'data_structures.py -> eb_sheet_names'!"


@timeit
def check_column_errors(
    energy_sources_sheets: pd.DataFrame, years: int, extend: bool = False
):

    # ///////////////////////////// KNOWN ERROR 1: Mischgas ends at year "1995"

    for sheet in energy_sources_sheets:
        # Since res sheet does not appear, cut of
        df = energy_sources_sheets[sheet].iloc[:, : len(years) + 1]

        # Check if column index is complete, extend otherwise
        if int(df.iloc[2, -1]) != years[-1] or df.iloc[2, -1] == "":

            logging.getLogger().critical("ERRRRRRRRROOOR")
            #     extend = True

            # elif :
            #     extend = True

            # if extend:
            # Replace missing years in column index
            add_on_columns = pd.DataFrame(
                index=range(len(df.index)), columns=years[len(df.columns) - 1 :]
            )

            energy_sources_sheets[sheet] = pd.concat(
                [df, add_on_columns], axis="columns"
            )
        else:
            energy_sources_sheets[sheet] = df

    return energy_sources_sheets


def check_index_errors(
    data: pd.DataFrame, data_type: str = None, template_index: pd.DataFrame = None
):
    index_deviations = data.index.difference(template_index)

    if index_deviations.any():

        indices_template = template_index.difference(data.index)

        logging.getLogger().warning("\n\t{} WARNING {}".format("*" * 33, "*" * 33))

        devs_idx = [list(data.index.get_indexer_for([i]) + 5) for i in index_deviations]

        index_deviations = dict(zip(index_deviations, devs_idx))

        # if data_type == "res":
        #     template_index_names = dict.fromkeys(
        #         [list(template_index)[idx] for dev in devs_idx for idx in dev]
        #     )
        # else:
        template_index_names = dict.fromkeys(
            [list(template_index)[idx - 5] for dev in devs_idx for idx in dev]
        )

        logging.getLogger().warning(
            "\tDifferent index in data:\n\t{}\n\t{}".format(
                list(index_deviations.keys()), list(index_deviations.values())
            )
        )

        logging.getLogger().warning(
            "\tData index in template:\n\t{}\n\t{}".format(
                list(template_index_names.keys()), "*" * 75
            )
        )

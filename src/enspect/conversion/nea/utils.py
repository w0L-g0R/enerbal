import datetime
import logging
from pathlib import Path
from typing import List, Union

import pandas as pd

from enspect.aggregates.common import provinces
from enspect.logger.setup import setup_logging


def create_nea_col_midx(
    last_year: int, sectors: List, energy_usage_types: List,
) -> pd.MultiIndex:

    years = [x for x in range(1993, last_year + 1, 1)]

    midx = pd.MultiIndex.from_product(
        [provinces, sectors, energy_usage_types, years],
        names=["PROV", "BAGG_0", "UC", "YEAR"],
    )

    return midx


# //////////////////////////////////////////////////// FETCH_SHEETS
def fetch_from_xlsx(file: Path):
    # Extract all sheets (=energieträger) from file at once and save them
    # to a dictionary
    sheets = pd.read_excel(
        io=str(Path(file)), sheet_name=None, na_filter=False, usecols="A:I",
    )

    # Delete unnecessary sheets
    del sheets["Deckblatt"]

    try:
        del sheets["Check"]
    except BaseException:
        pass

    try:
        del sheets["check"]
    except BaseException:
        pass

    return sheets


def write_to_log_file(log_file: str, files: List):

    setup_logging(
        console_log_actived=False,
        console_log_filter=None,
        console_out_level=logging.DEBUG,
        log_file=log_file,
    )

    logging.getLogger().warning(
        "{}\n\n{}FILE CONVERSION NEA \n{}\n".format("_" * 79, "\t" * 7, "_" * 79)
    )

    logging.getLogger().debug(
        "Started converting:\n {}\n".format(
            datetime.datetime.now().strftime("%Y, %d.%b - %Hh:%Mmin")
        )
    )

    logging.getLogger().debug(
        "Following files found:\n {}\n".format([f.stem for f in files])
    )

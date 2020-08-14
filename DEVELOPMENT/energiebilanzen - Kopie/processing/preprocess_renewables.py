from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np


# //////////////////////////////////////////// PREPROCESS_RENEWABLES_SHEET


def preprocess_renewables_sheet(
    renewables_sheet: pd.DataFrame, conversion_multiplicator: pd.Series
):

    renewables_sheet.drop(
        index=[16, 27, 34, 56, 58, 60], axis=0, inplace=True, errors="raise",
    )

    renewables_sheet.drop(
        index=list(range(68, 165)), axis=0, inplace=True, errors="raise",
    )

    renewables_sheet.drop(
        index=list(range(172, 177)), axis=0, inplace=True, errors="raise",
    )

    renewables_sheet.columns = renewables_sheet.iloc[2, :].values
    renewables_sheet.reset_index(drop=True, inplace=True)
    renewables_sheet = renewables_sheet.iloc[3:70, :]
    renewables_sheet.reset_index(drop=True, inplace=True)

    renewables_sheet = renewables_sheet.iloc[:, 1:]

    renewables_sheet = renewables_sheet.apply(pd.to_numeric, errors="coerce").round(2)

    # TODO: Replace with appropriate function
    for i in renewables_sheet.index:
        for j in renewables_sheet.columns:
            if isinstance(renewables_sheet.loc[i, j], str):
                renewables_sheet.loc[i, j] = np.nan

    renewables_sheet = renewables_sheet.mul(conversion_multiplicator, axis=0,)

    renewables_sheet_index = renewables_sheet.iloc[:, 1]

    return renewables_sheet, renewables_sheet_index

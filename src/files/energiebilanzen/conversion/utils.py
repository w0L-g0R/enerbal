from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np

from files.energiebilanzen.conversion.eb_data_structures import eb_sheets

# /////////////////////////////////////////////////////// CREATE_EB_STORAGE_DFS


def create_eb_storage_dfs(
    renewables_col_midx: pd.MultiIndex, eev_col_midx: pd.MultiIndex, row_indices: Dict,
):

    # _______________________________________________________ EEV MULTIINDEX DF

    # Create a dataframe with multiindex in order to copy indices from xlsx
    # sheets
    eev_df = pd.DataFrame(index=eev_col_midx, columns=range(190)).T

    # _______________________________________________________ EEV MULTIINDEX DF

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    renewables_df = pd.DataFrame(
        index=renewables_col_midx,
        columns=range(67)).T

    # _______________________________________ SECTOR CONSUMPTIONS MULTIINDEX DF

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    sectors_df = pd.DataFrame(
        index=row_indices["IDX_EEV_SECTORS"][0].values, columns=eev_col_midx
    )

    # _________________________________ SECTOR ENERGY CONSUMPTION MULTIINDEX DF

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    sector_energy_df = pd.DataFrame(
        index=row_indices["IDX_SECTOR_ENERGY"][0].values, columns=eev_col_midx
    )

    return (eev_df, renewables_df, sectors_df,
            sector_energy_df)


# //////////////////////////////////////////////////// CREATE_IDX_CHECK_DFS


def create_idx_check_dfs(row_indices: Dict):
    # Log index mismatches
    eev_idx_check_df = pd.DataFrame(
        data=row_indices["IDX_EEV"].values, columns=["Template"]
    )

    # Log index mismatches
    renewables_idx_check_df = pd.DataFrame(
        data=row_indices["IDX_RENEWABLES"].values, columns=["Template"]
    )

    # Log index mismatches
    sector_idx_check_df = pd.DataFrame(
        data=row_indices["IDX_EEV_SECTORS"].values, columns=["Template"]
    )

    sector_energy_idx_check_df = pd.DataFrame(
        data=row_indices["IDX_SECTOR_ENERGY"].values, columns=["Template"]
    )

    return (
        eev_idx_check_df,
        renewables_idx_check_df,
        sector_idx_check_df,
        sector_energy_idx_check_df,
    )

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

    renewables_sheet = renewables_sheet.apply(
        pd.to_numeric, errors="coerce").round(2)

    # TODO: Replace with appropriate function
    for i in renewables_sheet.index:
        for j in renewables_sheet.columns:
            if isinstance(renewables_sheet.loc[i, j], str):
                renewables_sheet.loc[i, j] = np.nan

    renewables_sheet = renewables_sheet.mul(conversion_multiplicator, axis=0,)

    renewables_sheet_index = renewables_sheet.iloc[:, 1]

    return renewables_sheet, renewables_sheet_index


def create_indices(provinces: List, eb_sheets: List, last_year: int):

    # Create a row multiindex from xlsx "midx_rows_eb"
    eb_row_midx = pd.MultiIndex.from_tuples(
        tuples=[tuple(x) for x in pd.read_excel(
            io=file_paths["eb_midx_xlsx"], sheet_name=None, na_filter=False, header=None,
        ).values],
        names=["IDX_0", "IDX_1", "IDX_2", "IDX_3", "IDX_4"],
    )

    # Create a res row multiindex (don't use the unit conversion columns ->
    # loc[:, :3])
    res_row_midx = pd.MultiIndex.from_tuples(
        tuples=[tuple(x)
                for x in pd.read_excel(
            io=file_paths["res_midx_xlsx"], sheet_name=None, na_filter=False, header=None,
        ).loc[:, :3].values],
        names=["IDX_0", "IDX_1", "IDX_2", "IDX_3"],
    )

    # ______________________________________________________ COL MULTI INDEX
    # Create column midx with provinces, energy_sources, years
    eb_col_midx = pd.MultiIndex.from_product(
        [
            provinces,
            eb_sheets,  # energy sources
            [x for x in range(1988, last_year + 1, 1)]  # years

        ], names=["BL", "ET", "YEAR"]
    )

    # Create a column muliindex with levels [province, Jahre]
    res_col_midx = pd.MultiIndex.from_product(
        [
            provinces,
            [x for x in range(1970, last_year + 1, 1)]  # years
        ], names=["BL", "YEAR"])

    return eb_row_midx, res_row_midx, eb_col_midx, res_col_midx

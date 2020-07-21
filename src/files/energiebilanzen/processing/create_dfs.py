from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np

# /////////////////////////////////////////////////////// CREATE_EB_STORAGE_DFS


def create_eb_storage_dfs(
    renewables_col_midx: pd.MultiIndex, eev_col_midx: pd.MultiIndex, row_indices: Dict,
):

    # _______________________________________________________ EEV MULTIINDEX DF

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    eev_df = pd.DataFrame(index=eev_col_midx, columns=range(190)).T

    # _______________________________________________________ EEV MULTIINDEX DF

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    renewables_df = pd.DataFrame(index=renewables_col_midx, columns=range(67)).T

    # _______________________________________ SECTOR CONSUMPTIONS MULTIINDEX DF

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    sector_consumptions_df = pd.DataFrame(
        index=row_indices["IDX_EEV_SECTORS"][0].values, columns=eev_col_midx
    )

    # _________________________________ SECTOR ENERGY CONSUMPTION MULTIINDEX DF

    # Create a dataframe with multiindex to copy the xlsx sheet values to
    sector_energy_consumption_df = pd.DataFrame(
        index=row_indices["IDX_SECTOR_ENERGY"][0].values, columns=eev_col_midx
    )

    return (eev_df, renewables_df, sector_consumptions_df, sector_energy_consumption_df)


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
    sector_consumptions_idx_check_df = pd.DataFrame(
        data=row_indices["IDX_EEV_SECTORS"].values, columns=["Template"]
    )

    sector_energy_consumption_idx_check_df = pd.DataFrame(
        data=row_indices["IDX_SECTOR_ENERGY"].values, columns=["Template"]
    )

    return (
        eev_idx_check_df,
        renewables_idx_check_df,
        sector_consumptions_idx_check_df,
        sector_energy_consumption_idx_check_df,
    )

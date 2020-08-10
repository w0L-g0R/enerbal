from pathlib import Path
from typing import Union, List, Dict
import pandas as pd
import pickle
import numpy as np

from files.energiebilanzen.processing.preprocess_renewables import (
    preprocess_renewables_sheet,
)

IDX = pd.IndexSlice

# //////////////////////////////////////////////////////// ASSIGN_EEV_TABLE


def assign_eev_table(
    eev_df: pd.DataFrame,
    eev_idx_check_df: pd.DataFrame,
    row_indices: pd.DataFrame,
    dfs: Dict,
    energy_source: str,
    province: str,
    years_range_data: pd.Series,
):
    # Assign current energy source df
    df = dfs[energy_source].iloc[3:193, 1:32].reset_index(drop=True)

    # Convert to numeric and round
    df = df.apply(pd.to_numeric, errors="coerce").round(2)

    # Extract row and col index for testing purposes
    energy_source_index = dfs[energy_source].iloc[3:193, 0].reset_index(drop=True)

    eev_template_index = pd.Series(data=row_indices["IDX_EEV"][0], name=0)

    try:

        # Test whether the index names (=Bilanzaggregate) are equal
        pd.testing.assert_series_equal(
            left=energy_source_index, right=eev_template_index, check_names=False,
        )

    except:

        eev_idx_check_df[energy_source] = energy_source_index

        check_col_name = "_".join(["Is_equal", energy_source])

        # If index mismatch, then checkout which rows are not equal to template
        eev_idx_check_df[check_col_name] = (
            eev_idx_check_df["Template"] == eev_idx_check_df[energy_source]
        )

    # Assign column multindex to current df
    df.columns = eev_df.loc[IDX[:], IDX[province, energy_source, :]].columns

    # Copy values from current energy source df to eev_df
    eev_df.loc[IDX[:], IDX[province, energy_source, :]] = df

    # NOTE: Adjust to "..energy_source, 1988:]" for EB_OE_70_18.xlxs
    # Slice again for final testing
    eev_df_slice = eev_df.loc[IDX[:], IDX[province, energy_source, :]]

    # Test if copying has been done right
    pd.testing.assert_frame_equal(
        left=eev_df_slice, right=df,
    )


# //////////////////////////////////////////////////////// ASSIGN_EEV_TABLE


def assign_renewables_table(
    renewables_df: pd.DataFrame,
    renewables_idx_check_df: pd.DataFrame,
    row_indices: pd.DataFrame,
    renewables_sheet: pd.DataFrame,
    province: str,
    years_range_data: pd.Series,
):

    conversion_multiplicator = row_indices["MIDX_RENEWABLES"].iloc[:, -1]

    renewables_sheet, renewables_sheet_index = preprocess_renewables_sheet(
        renewables_sheet=renewables_sheet,
        conversion_multiplicator=conversion_multiplicator,
    )

    renewables_template_index = pd.Series(data=row_indices["IDX_RENEWABLES"][0], name=0)

    try:

        # Test whether the index names (=Bilanzaggregate) are equal
        pd.testing.assert_series_equal(
            left=renewables_sheet_index,
            right=renewables_template_index,
            check_names=False,
        )

    except:

        renewables_idx_check_df["Erneuerbare RL"] = renewables_sheet.index

        # If index mismatch, then checkout which rows are not equal to template
        renewables_idx_check_df["Is_equal"] = (
            renewables_idx_check_df["Template"]
            == renewables_idx_check_df["Erneuerbare RL"]
        )
        print("Index name mismatch")

    # Assign column multindex to current df
    renewables_sheet.columns = renewables_df.loc[IDX[:], IDX[province, :]].columns

    # Copy values from current energy source df to eev_df
    renewables_df.loc[IDX[:], IDX[province, :]] = renewables_sheet

    # NOTE: Adjust to "..energy_source, 1988:]" for EB_OE_70_18.xlxs
    # Slice again for final testing
    renewables_df_slice = renewables_df.loc[IDX[:], IDX[province, :]]

    # Test if copying has been done right
    pd.testing.assert_frame_equal(
        left=renewables_df_slice, right=renewables_sheet,
    )


# //////////////////////////////////////////// ASSIGN_SECTORS_CONSUMPTION_TABLE


def assign_sectors_consumption_table(
    sector_consumptions_df: pd.DataFrame,
    sector_consumptions_idx_check_df: pd.DataFrame,
    dfs: Dict,
    energy_source: str,
    province: str,
    years_range_data: pd.Series,
):

    df = dfs[energy_source].copy()
    df.set_index(df.iloc[:, 0], inplace=True)
    df.drop(df.columns[[0]], axis=1, inplace=True)

    start_index = df.index.get_indexer_for(["Sektoraler Energetischer Endverbrauch"])[0]

    print("SEC_Consump start_index: ", start_index)

    if start_index == [-1]:
        sector_consumptions_df.loc[:, IDX[province, energy_source, :]] = float("NaN")

        sector_consumptions_idx_check_df[energy_source] = False

        return

    df = df.iloc[start_index : start_index + 27, :31]

    if df.index[1] == "in Tonnen":
        return

    # assert len(df.columns) == len(years_range_data), "Years not equal"
    # assert "Terajoule" in df.index[1], "Row slicing mismatch"
    assert df.index[-1] == "Sonstige", "Row slicing mismatch"

    sector_columns = sector_consumptions_df.loc[
        :, IDX[province, energy_source, :]
    ].columns

    df.columns = sector_columns

    sector_consumptions_df.loc[:, IDX[province, energy_source, :]] = df


# ////////////////////////////////////// ASSIGN_SECTOR_ENERGY_CONSUMPTION_TABLE


def assign_sector_energy_consumption_table(
    sector_energy_consumption_df: pd.DataFrame,
    sector_energy_consumption_idx_check_df: pd.DataFrame,
    dfs: Dict,
    energy_source: str,
    province: str,
    years_range_data: pd.Series,
):

    df = dfs[energy_source].copy()
    df.set_index(df.iloc[:, 0], inplace=True)
    df.drop(df.columns[[0]], axis=1, inplace=True)

    start_index = df.index.get_indexer_for(["Verbrauch Sektor Energie"])[0]
    print("SEC_Energy start_index: ", start_index)

    if start_index == [-1]:

        sector_energy_consumption_df.loc[:, IDX[province, energy_source, :]] = float(
            "NaN"
        )

        sector_energy_consumption_idx_check_df[energy_source] = False
        return

    df = df.iloc[start_index : start_index + 10, :31]

    df = df.apply(pd.to_numeric, args=("coerce",))
    print("df: ", df.iloc[2:, :])

    if df.index[1] == "in Tonnen":
        return

    # assert len(df.columns) == len(years_range_data), "Years not equal"
    # assert "Terajoule" in df.index[1], "Row slicing mismatch: {}".format(df.index[1])
    assert (
        df.index[-2] == "Energieversorgung (Elektrizität, Erdgas, Fernwärme)"
    ), "Row slicing mismatch"

    if df.index[-1] != "Gesamt":
        new_index = list(df.index)[:-1]
        new_index.append("Gesamt")
        df.index = pd.Index(new_index)

    sector_energy_consumption_columns = sector_energy_consumption_df.loc[
        :, IDX[province, energy_source, :]
    ].columns

    df.columns = sector_energy_consumption_columns

    sector_energy_consumption_df.loc[:, IDX[province, energy_source, :]] = df

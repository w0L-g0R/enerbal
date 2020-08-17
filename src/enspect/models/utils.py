import pandas as pd
import numpy as np
from copy import deepcopy
from enspect.settings import conversion_multiplicators
from typing import List
from pprint import pprint


def add_sums(df: pd.DataFrame):

    # Create provinces sum column and years sum row
    # print("df sums: ", df)
    df["Sum"] = df.iloc[:, :-1].sum(axis=1)
    # print("df sums col: ", df)
    df = df.T
    # print("df sums T: ", df)
    df["Sum"] = df.sum(axis=1)

    return df.T


def add_means(df: pd.DataFrame):

    # Create provinces sum column and years sum row
    # print("df sums: ", df)
    df["Mean"] = df.iloc[:, :-1].mean(axis=1)
    # print("df sums col: ", df)
    df = df.T
    # print("df sums T: ", df)
    df["Mean"] = df.mean(axis=1)

    return df.T


def switch_sum_and_AT_col(df: pd.DataFrame):

    # get a list of the columns
    col_list = list(df)
    # use this handy way to swap the elements
    col_list[0], col_list[1] = col_list[1], col_list[0]
    # assign back, the order will now be swapped
    df.columns = col_list

    return df


def get_shares(df: pd.DataFrame,):

    print('"inside post": ')

    df_shares = {}

    # Each row divided the sum row
    df_rows = deepcopy(df)

    # _____________________________________________________________________ COL
    df_cols = deepcopy(df)

    # Set share for AT to 100%
    df_cols["AT"] = 1

    # Sum over provinces as share of AT
    df_cols["Sum"] = df.iloc[:, :-2].sum(axis="columns") / df["AT"]

    # Each col divided by sum col
    for col in df.columns:
        # Exclude sum col and AT col
        df_cols[col] = df[col] / df[col].iloc[-1]  # sum

    df_shares["cols"] = df_cols.round(2)

    # _____________________________________________________________________ ROW
    # AT row values as share of AT sum over rows
    df_rows["AT"] = df["AT"] / df["AT"].sum(axis="rows")

    # Sum over provinces as share of AT
    df_rows["Sum"] = df.iloc[:, :-2].sum(axis="columns") / df["AT"]

    for index, row_values in df.iterrows():
        # Exclude sum col and AT col
        df_rows.loc[index, :] = row_values / row_values[:-2].sum(axis="rows")

    df_shares["rows"] = df_rows.round(2)

    # pprint(df_shares)

    return df_shares

    # if provinces:
    #     df_shares = df_shares.T

    #     provinces_sums_per_year = df_shares.iloc[:-2, :].sum(axis=0).replace(0, np.nan)

    #     # print("provinces_sums_per_year: ", provinces_sums_per_year)
    #     AT_sums_per_year = df_shares.iloc[-2, :].replace(0, np.nan)

    #     # Province share over sum of provinces, per year
    #     df_shares.iloc[:-2, :].replace(0, np.nan).divide(provinces_sums_per_year)

    #     # try:
    #     # Percentage sum over provinces per year (== 1)
    #     df_shares.iloc[-1, :].replace(0, np.nan).divide(provinces_sums_per_year)
    #     # except BaseException:
    #     #     pass

    #     # Sum of selected province as a share of "AT", per year
    #     df_shares.loc["AT", :] = provinces_sums_per_year.divide(AT_sums_per_year)

    #     # print("df_shares: ", df_shares)
    #     # Check if row values sum up to 1
    #     if "Sum" in df_shares.columns:
    #         for col in df_shares.columns:
    #             assert round(df_shares[col].iloc[:-2].sum(axis=0), 3) == round(
    #                 df_shares[col].loc["Sum"], 3
    #             ), f"PROVINCES SHARES '{col}': Percentage value sum {df_shares[col].iloc[:-2].sum(axis=0)} does not match sum {df_shares[col].loc['Sum']}!"

    #     if "Mean" in df_shares.columns:
    #         for col in df_shares.columns:
    #             assert round(df_shares[col].iloc[:-2].mean(axis=0), 3) == round(
    #                 df_shares[col].loc["Mean"], 3
    #             ), f"PROVINCES SHARES '{col}': Percentage value sum {df_shares[col].iloc[:-2].mean(axis=0)} does not match sum {df_shares[col].loc['Mean']}!"

    #     return df_shares.T

    # elif years:

    #     df_shares = df_shares / df_shares.sum(axis=0)

    #     # Check if all necessary sum values are given
    #     if sum(df_shares.sum(axis=0)) == len(df_shares.columns):

    #         df_shares.loc["Sum", :] = df_shares.sum(axis=0).values

    #     if "Sum" in df_shares.columns:

    #         # Check if row values sum up to 1
    #         for col in df_shares.columns:

    #             assert round(df_shares[col].iloc[:-1].sum(axis=0), 3) == round(
    #                 df_shares[col].loc["Sum"], 3
    #             ), f"YEARS SHARES: {col}: Percentage value sum {df_shares[col].sum(axis=0)-1} does not match sum {df_shares[col].loc['Sum']}!"

    #     if "Mean" in df_shares.index:

    #         # Check if row values sum up to 1
    #         for col in df_shares.columns:

    #             assert round(df_shares[col].iloc[:-1].mean(axis=0), 3) == round(
    #                 df_shares[col].loc["Mean"], 3
    #             ), f"YEARS SHARES: {col}: Percentage value sum {df_shares[col].mean(axis=0)-1} does not match sum {df_shares[col].loc['Mean']}!"


def apply_single_index(df: pd.DataFrame):

    # Validate type of df
    if not isinstance(df, pd.DataFrame):
        df = df.to_frame()

    df = df.T.reset_index(drop=True).T

    # Only one year in YEARS index - drop it
    if len(df.index.get_level_values("YEAR").unique()) == 1:
        df = df.droplevel(("YEAR"), axis=0)
    else:
        df = df.droplevel((1), axis=0)

    df = df.T.stack().droplevel((0), axis=0)

    df.index.name = ""

    # Put "AT" at the end
    if "AT" in df.columns:
        df = df.reindex(columns=list(df.columns[1:]) + ["AT"])

    return df


def convert(df: pd.DataFrame, conversion: str):

    # Transform data values to new unit scale
    df *= conversion_multiplicators[conversion]

    # Assign new unit
    unit = conversion.split("_")[-1]

    return df, unit


def extend_eb_row_index(balance_aggregate: str):

    aggregate = [balance_aggregate]

    # Extend eev data index -> multi index
    row_midx_addon = 5 - len(aggregate)

    # Extend the  with "Gesamt" if not specified
    aggregate.extend(["Gesamt"] * row_midx_addon)

    return aggregate


def reduce_eb_row_index(balance_aggregates: List):
    # Remove all indices with "Gesamt"
    return "_".join([x for x in aggregate if x != "Gesamt"])


def post_process(df: pd.DataFrame, conversion: str):

    # Data tranformation
    df = apply_single_index(df=df)

    # Sum column and row
    df = add_sums(df=df)

    # Conversion
    if conversion is not None:
        df, unit = convert(df=df, conversion=conversion)
    else:
        unit = "TJ"

    # Share of each province over total provinces per year
    df_shares = get_shares(df=df)

    return df, df_shares, unit

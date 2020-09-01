import logging
import os
import pickle
from copy import deepcopy
from pprint import pprint
from typing import List, Union

import numpy as np
import pandas as pd
from pandas.core.common import flatten

from enspect.paths import file_paths
from enspect.settings import unit_converter


def close_xlsx():

    try:
        os.system("TASKKILL /F /IM excel.exe")

    except Exception:
        print("No open excel file.")


IDX = pd.IndexSlice


# def add_sums(df: pd.DataFrame):

#     # Create provinces sum column and years sum row
#     # print("df sums: ", df)
#     df["Sum"] = df.iloc[:, :-1].sum(axis=1)
#     # print("df sums col: ", df)
#     df = df.T
#     # print("df sums T: ", df)
#     df["Sum"] = df.sum(axis=1)

#     return df.T


# def add_means(df: pd.DataFrame):

#     # Create provinces sum column and years sum row
#     # print("df sums: ", df)
#     df["Mean"] = df.iloc[:, :-1].mean(axis=1)
#     # print("df sums col: ", df)
#     df = df.T
#     # print("df sums T: ", df)
#     df["Mean"] = df.mean(axis=1)

#     return df.T


def switch_sum_and_AT_col(df: pd.DataFrame):

    # get a list of the columns
    col_list = list(df)
    # use this handy way to swap the elements
    col_list[0], col_list[1] = col_list[1], col_list[0]
    # assign back, the order will now be swapped
    df.columns = col_list

    return df


def make_AT_last_midx_col(df: pd.DataFrame):

    col_list = list(df.columns.get_level_values(level="BL").unique())
    col_list.append(col_list[0])
    col_list.pop(0)

    df.columns = pd.MultiIndex.from_product(
        iterables=[
            df.columns.get_level_values(level="YEAR").unique(),
            df.columns.get_level_values(level="IDX_0").unique(),
            col_list,
        ],
        names=["YEAR", "IDX_0", "BL"],
    )

    return df


def reduce_eb_row_index(balance_aggregates: List):
    # Remove all indices with "Gesamt"
    return "_".join([x for x in aggregate if x != "Gesamt"])


# def drop_eb_row_levels(balance_aggregates: Union[List, str], df:
# pd.DataFrame):

#     return df


def add_row_total(df: pd.DataFrame):
    # Add colum_total row
    df.loc["SUM", :] = df.sum(numeric_only=True, axis=0)

    df.iloc[-1, 0] = "SUM"
    return df


def add_col_total(df: pd.DataFrame):
    # Add colum_total row
    df.loc[:, "SUM"] = df.sum(
        numeric_only=True, axis=1).subtract(df[df.columns[0]])

    col_list = list(df.columns)
    col_list.remove("AT")
    col_list.append("AT")
    df = df[col_list]

    return df


def slice_eb_inputs(df: pd.DataFrame, balance_aggregates: List, years=List):

    ua_indices = 0
    ue_indices = 0

    for aggregate in balance_aggregates:

        if "Umwandlungsausstoß" in aggregate:
            try:
                ua_indices = len(aggregate.split("_"))
            except BaseException:
                pass
        if "Umwandlungseinsatz" in aggregate:
            try:
                ue_indices = len(aggregate.split("_"))
            except BaseException:
                pass

    cutoff_indices = list(range(4, max(ua_indices, ue_indices), -1))

    df = df.droplevel(level=cutoff_indices[::-1], axis=0)

    df = df.loc[IDX[balance_aggregates], IDX[:, :, years]]

    return df

    # new_cols is a single item tuple
    # assign back, the order will now be swapped

    # cols = ['IWWGCW', 'IWWGDW', 'BASE']

    # new_cols = df.columns.reindex(cols, level = 0)

    # return df.columns.reindex(col_list, level="BL")


# def get_shares(df: pd.DataFrame,):

#     print('"inside post": ')

#     df_shares = {}

#     # Each row divided the sum row
#     df_rows = deepcopy(df)

#     # _____________________________________________________________________ COL
#     df_cols = deepcopy(df)

#     # Set share for AT to 100%
#     df_cols["AT"] = 1

#     # Sum over provinces as share of AT
#     df_cols["Sum"] = df.iloc[:, :-2].sum(axis="columns") / df["AT"]

#     # Each col divided by sum col
#     for col in df.columns:
#         # Exclude sum col and AT col
#         df_cols[col] = df[col] / df[col].iloc[-1]  # sum

#     df_shares["cols"] = df_cols.round(2)

#     # _____________________________________________________________________ ROW
#     # AT row values as share of AT sum over rows
#     df_rows["AT"] = df["AT"] / df["AT"].sum(axis="rows")

#     # Sum over provinces as share of AT
#     df_rows["Sum"] = df.iloc[:, :-2].sum(axis="columns") / df["AT"]

#     for index, row_values in df.iterrows():
#         # Exclude sum col and AT col
#         df_rows.loc[index, :] = row_values / row_values[:-2].sum(axis="rows")

#     df_shares["rows"] = df_rows.round(2)

#     # pprint(df_shares)

#     return df_shares


# def apply_single_index(df: pd.DataFrame):

#     # Validate type of df
#     if not isinstance(df, pd.DataFrame):
#         df = df.to_frame()

#     # Only one year in YEARS index - drop it
#     if len(df.columns.get_level_values("YEAR").unique()) == 1:
#         df = df.droplevel(("YEAR"), axis="columns")

#     df = df.T.reset_index(drop=True).T

#     df
#     print("df: ", df)

#     # else:
#     df = df.droplevel((1), axis=0)

#     df = df.T.stack().droplevel((0), axis=0)

#     df.index.name = ""

#     # Put "AT" at the end
#     if "AT" in df.columns:
#         df = df.reindex(columns=list(df.columns[1:]) + ["AT"])

#     return df

# def extend_eb_row_index(balance_aggregates: Union[List, str]):
#     """
#     Takes a list or a single aggregates and adds additional indices.
#     This way one don't have to specify all five levels of the row multiindex.

#     add_all:
# Adds ":" (without quotation marks!) for the missing
# indices[balance_aggregate, :, : , : , :]

#     add_total:
# Adds "Gesamt" (without quotation marks!) for the missing
# indices[balance_aggregate, "Gesamt", "Gesamt" , "Gesamt" , "Gesamt"]

#     """
#     # balance_aggregates_extended = []

#     # for aggregate in balance_aggregates:
#     #     print("aggregate: ", aggregate)

#     if not isinstance(balance_aggregates, list):
#         aggregate = list(balance_aggregates)

#     # if add_all:

#     #     # # Extend the  with : if not specified
#     #     # for x in range(0, row_midx_addon):

#     #     #     aggregate.append(IDX[:])
#     # per: str,
#     balance_aggregates = []
#     for aggregate in balance_aggregates:

#         # Check for missing level values (eb row idx == 5 Levels)
#         row_midx_addon = 5 - len(aggregate)

#         # Extend the  with "Gesamt" if not specified
#         aggregate.extend(["Gesamt"] * row_midx_addon)

#         balance_aggregates.append(aggregate)

#         # balance_aggregates.append(
#         #     IDX[aggregate, "Gesamt", "Gesamt", "Gesamt", "Gesamt"]
#         # )

#     balance_aggregates = IDX[aggregate, "Gesamt", "Gesamt", "Gesamt", "Gesamt"]
#     print("balance_aggregates: ", balance_aggregates)

#     # balance_aggregates_extended.append(aggregate)
#     # print("balance_aggregates_extended: ", balance_aggregates_extended)

#     return balance_aggregates


# def convert_round(func):
#     def wrapper(*args, **kwargs):

#         data, conversion = func(*args, **kwargs)
#         print("data: ", type(data))

#         if isinstance(data, pd.DataFrame):
#             data = [data]

#         data = [f.round(2) * unit[conversion] for f in data]

#         print("data: ", data)
#         # print("frame: ", frame)
#         # dataset.objects
#         return

#     return wrapper

#     data.append(
#         df.groupby(level=["IDX_0"], axis=0).get_group(aggregate)
#         # .swaplevel(2, 1, axis=1)
#         # .sort_index(axis=1, level=0)
#     )

# return data

# if sort_column_by == "province":
#     data = data.swaplevel(0, 1, axis=1).sort_index(axis=1, level=0)

# data.loc["Column_Total"] = data.sum(numeric_only=True, axis=0)

# if len(energy_sources) == 1:

# return data

# USE FOR SUM ROWS ONLY -> Chart
# d = data.groupby(level=["ET"], axis=0).get_group("SUM")
# print("d: ", d)
# # g =
# # g.index
# print("g.index: ", g.index)
# # g.drop(labels=aggregate, level=0, axis=0)
# # print("g.index: ", g.index)
# # print("g.columns: ", g.columns)
# #     data = data.swaplevel(0, 1, axis=1).sort_index(axis=1, level=0)

# print("g: ", g)

# .agg("sum")
# for aggregate in energy_aggregate_lookup[source]:
# def get_data_per_aggregate(energy_aggregates: List):
#     data

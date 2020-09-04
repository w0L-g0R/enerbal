import itertools
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
from enspect.aggregates.eb import energy_aggregate_lookup


def close_xlsx():

    try:
        os.system("TASKKILL /F /IM excel.exe")

    except Exception:
        print("No open excel file.")


IDX = pd.IndexSlice


def add_sums(df: pd.DataFrame, drop_cols: List):

    df = add_total_per_col(df=df)

    df.reset_index(inplace=True)

    df.drop(drop_cols, inplace=True, axis=1)

    df = add_total_per_row(df=df)

    return df.copy()


# def add_means(df: pd.DataFrame):

#     # Create provinces sum column and years sum row
#     # print("df sums: ", df)
#     df["Mean"] = df.iloc[:, :-1].mean(axis=1)
#     # print("df sums col: ", df)
#     df = df.T
#     # print("df sums T: ", df)
#     df["Mean"] = df.mean(axis=1)

#     return df.T


# def switch_sum_and_AT_col(df: pd.DataFrame):

#     # get a list of the columns
#     col_list = list(df)
#     # use this handy way to swap the elements
#     col_list[0], col_list[1] = col_list[1], col_list[0]
#     # assign back, the order will now be swapped
#     df.columns = col_list

#     return df


# def make_AT_last_midx_col(df: pd.DataFrame):

#     col_list = list(df.columns.get_level_values(level="PROV").unique())
#     col_list.append(col_list[0])
#     col_list.pop(0)

#     df.columns = pd.MultiIndex.from_product(
#         iterables=[
#             df.columns.get_level_values(level="YEAR").unique(),
#             df.columns.get_level_values(level="BAGG_0").unique(),
#             col_list,
#         ],
#         names=["YEAR", "BAGG_0", "PROV"],
#     )

#     return df


def reduce_eb_row_index(balance_aggregates: List):
    # Remove all indices with "Gesamt"
    return "_".join([x for x in aggregate if x != "Gesamt"])


# def drop_eb_row_levels(balance_aggregates: Union[List, str], df:
# pd.DataFrame):

#     return df


def add_total_per_row(df: pd.DataFrame):
    # Sum over column values per row
    df.loc["SUM", :] = df.sum(axis=0)

    df.iloc[-1, 0] = "SUM"
    return df


def add_total_per_col(df: pd.DataFrame):

    s = df.drop("AT", axis=1)
    df.loc[:, "SUM"] = s.sum(axis=1)

    col_list = list(df.columns)
    col_list.remove("AT")
    col_list.append("AT")
    df = df[col_list]

    return df


def check_balance_aggregates_type(func):
    def wrapper(*args, **kwargs):

        # Make sure balance_aggregates comes a list of list
        assert isinstance(
            kwargs["balance_aggregates"], list
        ), "Balance aggregate argument must be a list"

        for element in kwargs["balance_aggregates"]:
            assert isinstance(element, list), f"{element} is not a list!"
            assert element != [], f"{element} is an empty list!"

        func(*args, **kwargs)

        return

    return wrapper


# def slice_pickled_eb_df(
#     df: pd.DataFrame,
#     energy_sources: List,
#     energy_aggregates: List,
#     balance_aggregates: List,
#     years: List,
#     provinces: List,
# ):

#     # Filter energy sources for energy aggregates if necessary
#     if energy_sources is None:

#         energy_sources = list(
#             flatten(
#                 [energy_aggregate_lookup[aggregate] for aggregate in energy_aggregates]
#             )
#         )

#     # # In case all baggs elements only contain less than the max nr of levels..
#     # dummy = ["Gesamt", "Gesamt", "Gesamt", "Gesamt", "Gesamt"]

#     # # .. add this dummy, wich gets used as ref to fill missing index values ..
#     # balance_aggregates.insert(0, dummy)

#     # # .. in the course of combining aggregates for slicing
#     # balance_aggregates = tuple(
#     #     itertools.zip_longest(*balance_aggregates, fillvalue="Gesamt")
#     # )

#     balance_aggregates = [
#         "_".join(val).rstrip("_").split("_Gesamt")[0]
#         for val in balance_aggregates
#         if val != "Gesamt"
#     ]

#     print()
#     pprint(balance_aggregates)

#     # Flatten with underline separation, pass over "Gesamt" indices
#     index = [
#         "_".join(val).rstrip("_").split("_Gesamt")[0]
#         for val in df.index.values
#         if val != "Gesamt"
#     ]
#     df.index = index

#     # Slice -> dummy indices will not be considered since not in index
#     df = df.loc[IDX[balance_aggregates], IDX[provinces, energy_sources, years]]
#     # df = df.loc[IDX[i], IDX[:, years]]

#     df.index.name = "BAGG_0"

#     # columns: YEAR,PROV, ES
#     # df = df.swaplevel(0, 2, axis=1).sort_index(axis=1, level=0)
#     print("\ndf SLICE: ", df.head())

#     return df, balance_aggregates


# def slice_pickled_res_df(
#     df: pd.DataFrame, balance_aggregates: List, provinces: List, years: List
# ):

#     # # In case all baggs elements only contain one or two strings..
#     # dummy = ["Gesamt", "Gesamt", "Gesamt"]

#     # # .. add this dummy, wich then gets used to fill missing index values ..
#     # balance_aggregates.insert(0, dummy)

#     # # .. when combining aggregates for slicing
#     # i = tuple(itertools.zip_longest(*balance_aggregates, fillvalue="Gesamt"))

#     balance_aggregates = [
#         "_".join(val).rstrip("_").split("_Gesamt")[0]
#         for val in balance_aggregates
#         if val != "Gesamt"
#     ]

#     # Flatten with underline seperation, pass over "Gesamt"
#     index = [
#         "_".join(val).rstrip("_").split("_Gesamt")[0]
#         for val in df.index.values
#         if val != "Gesamt"
#     ]

#     df.index = index

#     # Slice
#     df = df.loc[IDX[balance_aggregates], IDX[provinces, years]]

#     # TODO: Add the level in the conversion process
#     # Add another row level
#     df = pd.concat({"RES": df}, names=["ES"])

#     # Turn row into column index
#     df = df.unstack("ES")

#     # Rename
#     df.index.name = "BAGG_0"

#     # # columns: YEAR, PROV, ES
#     df = df.swaplevel(1, 2, axis=1).sort_index(axis=1, level=0)

#     # # columns: YEAR, ES, PROV
#     # df = df.swaplevel(1, 2, axis=1).sort_index(axis=1, level=0)

#     print("\n\ndf: ", df)
#     print("index: ", index)

#     return df, balance_aggregates  # , #list(df.index)


def slice_pickled_eb_df(
    df: pd.DataFrame,
    balance_aggregates: List,
    years: List,
    provinces: List,
    energy_aggregates: List = None,
    energy_sources: List = None,
    is_res: bool = False,
):

    balance_aggregates = [
        "_".join(val).rstrip("_").split("_Gesamt")[0]
        for val in balance_aggregates
        if val != "Gesamt"
    ]

    # print()
    # pprint(balance_aggregates)

    # Flatten with underline separation, pass over "Gesamt" indices
    index = [
        "_".join(val).rstrip("_").split("_Gesamt")[0]
        for val in df.index.values
        if val != "Gesamt"
    ]
    df.index = index

    if is_res:

        # Slice
        df = df.loc[IDX[balance_aggregates], IDX[provinces, years]]

        # TODO: Add the level in the conversion process
        # Add another row level
        df = pd.concat({"RES": df}, names=["ES"])

        # Turn row into column index
        df = df.unstack("ES")

        # # Rename
        # df.index.name = "BAGG_0"

        # # columns: YEAR, PROV, ES
        df = df.swaplevel(1, 2, axis=1).sort_index(axis=1, level=0)

    else:

        # Filter energy sources for energy aggregates if necessary
        if energy_sources is None:

            energy_sources = list(
                flatten(
                    [
                        energy_aggregate_lookup[aggregate]
                        for aggregate in energy_aggregates
                    ]
                )
            )

        # Slice -> dummy indices will not be considered since not in index
        df = df.loc[IDX[balance_aggregates], IDX[provinces, energy_sources, years]]

    df.index.name = "BAGG_0"

    return df, balance_aggregates


def get_name_and_key(*args, **kwargs):
    name = "_".join((kwargs["data_type"], *args, str(kwargs["year"])))

    key = "_".join(
        [kwargs["key"], *[arg[:3].upper() for arg in args], str(kwargs["year"])[-2:],]
    )

    return name, key

    # new_cols is a single item tuple
    # assign back, the order will now be swapped

    # cols = ['IWWGCW', 'IWWGDW', 'BASE']

    # new_cols = df.columns.reindex(cols, level = 0)

    # return df.columns.reindex(col_list, level="PROV")


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


def extend_eb_row_index(balance_aggregates: Union[List, str]):
    """
    Takes a list or a single aggregates and adds additional indices.
    This way one don't have to specify all five levels of the row multiindex.

    add_all:
Adds ":" (without quotation marks!) for the missing
indices[balance_aggregate, :, : , : , :]

    add_total:
Adds "Gesamt" (without quotation marks!) for the missing
indices[balance_aggregate, "Gesamt", "Gesamt" , "Gesamt" , "Gesamt"]

    """
    # balance_aggregates_extended = []

    # for aggregate in balance_aggregates:
    #     print("aggregate: ", aggregate)

    if not isinstance(balance_aggregates, list):
        aggregate = list(balance_aggregates)

    # if add_all:

    #     # # Extend the  with : if not specified
    #     # for x in range(0, row_midx_addon):

    #     #     aggregate.append(IDX[:])
    # per: str,
    balance_aggregates = []
    for aggregate in balance_aggregates:

        # Check for missing level values (eb row idx == 5 Levels)
        row_midx_addon = 5 - len(aggregate)

        # Extend the  with "Gesamt" if not specified
        aggregate.extend(["Gesamt"] * row_midx_addon)

        balance_aggregates.append(aggregate)

        # balance_aggregates.append(
        #     IDX[aggregate, "Gesamt", "Gesamt", "Gesamt", "Gesamt"]
        # )

    balance_aggregates = IDX[aggregate, "Gesamt", "Gesamt", "Gesamt", "Gesamt"]
    print("balance_aggregates: ", balance_aggregates)

    # balance_aggregates_extended.append(aggregate)
    # print("balance_aggregates_extended: ", balance_aggregates_extended)

    return balance_aggregates


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
#         df.groupby(level=["BAGG_0"], axis=0).get_group(aggregate)
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
# d = data.groupby(level=["ES"], axis=0).get_group("SUM")
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

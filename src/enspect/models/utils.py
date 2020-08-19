import pandas as pd
import numpy as np
from copy import deepcopy
from enspect.settings import unit
from typing import List, Union
from pprint import pprint
import logging
import pickle
from enspect.conversion.energiebilanzen.data_structures import energy_aggregate_lookup
from enspect.paths import file_paths

from pandas.core.common import flatten


IDX = pd.IndexSlice


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


def apply_single_index(df: pd.DataFrame):

    # Validate type of df
    if not isinstance(df, pd.DataFrame):
        df = df.to_frame()

    # Only one year in YEARS index - drop it
    if len(df.columns.get_level_values("YEAR").unique()) == 1:
        df = df.droplevel(("YEAR"), axis="columns")

    df = df.T.reset_index(drop=True).T

    df
    print("df: ", df)

    # else:
    df = df.droplevel((1), axis=0)

    df = df.T.stack().droplevel((0), axis=0)

    df.index.name = ""

    # Put "AT" at the end
    if "AT" in df.columns:
        df = df.reindex(columns=list(df.columns[1:]) + ["AT"])

    return df


def convert(df: pd.DataFrame, conversion: str):

    # Transform data values to new unit scale
    df *= unit[conversion]

    # Assign new unit
    unit = conversion.split("_")[-1]

    return df, unit


# def extend_eb_row_index(balance_aggregates: Union[List, str]):
#     """
#     Takes a list or a single aggregates and adds additional indices.
#     This way one don't have to specify all five levels of the row multiindex.

#     add_all:
#         Adds ":" (without quotation marks!) for the missing indices[balance_aggregate, :, : , : , :]

#     add_total:
#         Adds "Gesamt" (without quotation marks!) for the missing indices[balance_aggregate, "Gesamt", "Gesamt" , "Gesamt" , "Gesamt"]

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


def reduce_eb_row_index(balance_aggregates: List):
    # Remove all indices with "Gesamt"
    return "_".join([x for x in aggregate if x != "Gesamt"])


def drop_eb_row_levels(balance_aggregates: Union[List, str], df: pd.DataFrame):

    ua_indices = 0
    ue_indices = 0

    for aggregate in balance_aggregates:

        if "Umwandlungsausstoß" in aggregate:
            try:
                ua_indices = len(aggregate.split("_"))
            except:
                pass
        if "Umwandlungseinsatz" in aggregate:
            try:
                ue_indices = len(aggregate.split("_"))
            except:
                pass

    cutoff_indices = list(range(4, max(ua_indices, ue_indices), -1))
    print("cutoff_indices: ", list(cutoff_indices))

    df = df.droplevel(level=cutoff_indices[::-1], axis=0)
    # df = df.droplevel(level=[1, 2, 3, 4], axis=0)

    return df


def post_process(df: pd.DataFrame, conversion: str):

    # Data tranformation
    # df = apply_single_index(df=df)

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


def convert_round_save(func):
    def wrapper(*args, **kwargs):

        data, conversion = func(*args, **kwargs)
        print("data: ", type(data))

        if isinstance(data, pd.DataFrame):
            data = [data]

        data = [f.round(2) * unit[conversion] for f in data]

        print("data: ", data)
        # print("frame: ", frame)
        # dataset.objects
        return

    return wrapper


@convert_round_save
def add_eb_data(
    dataset: object,
    provinces: List,
    years: List,
    # columns: Union[List, str],
    # rows: Union[List, str],
    conversion: str = None,
    balance_aggregates: List = None,
    energy_sources: List = None,
    energy_aggregates: List = None,
    sort_column_by: str = None,
    per_balance_aggregate: bool = False,
    per_energy_source: bool = False,
    per_energy_aggregate: bool = False,
    per_year: bool = False,
):
    """
    
    row index:
        balance aggregate = ["IDX_0", "IDX_1", "IDX_2", "IDX_3", "IDX_4"]
    
    col_index:
        province, source, year = ["BL", "ET", "YEAR"]

    """
    logging.getLogger().error("/" * 80)

    assert isinstance(
        balance_aggregates, (list, tuple)
    ), "Wrap list or tuple around aggregate!"

    df = pickle.load(open(file_paths["db_pickles"] / "eb.p", "rb"))

    df = drop_eb_row_levels(balance_aggregates=balance_aggregates, df=df)

    # Filter aggregates
    df = df.groupby(level=["IDX_0"], axis=0).filter(
        lambda x: x.index.unique() in balance_aggregates
    )

    # Filter years
    df = df.groupby(level=["YEAR"], axis=1).filter(
        lambda x: x.columns.get_level_values(2).unique() in years
    )

    data = []

    print("df init: ", df.head())
    if per_energy_aggregate:

        energy_sources = list(
            flatten([energy_aggregate_lookup[source] for source in energy_aggregates])
        )

        df = (
            df.groupby(level=["ET"], axis=1)
            .filter(lambda x: x.columns.get_level_values(1).unique() in energy_sources)
            .stack("ET")
            .unstack("IDX_0")
        )

        data = []

        for aggregate_name in energy_aggregates:
            print()
            print("name: ", aggregate_name)

            #     data
            energy_aggregate = df.groupby(level=["ET"], axis=0).filter(
                lambda x: x.index in energy_aggregate_lookup[aggregate_name]
            )

            energy_aggregate.loc["SUM", IDX[:]] = energy_aggregate.sum(
                numeric_only=True, axis=0
            )

            energy_aggregate.index = pd.MultiIndex.from_product(
                iterables=[
                    [aggregate_name],
                    list(energy_aggregate.index),
                ],  # .replace("_", "-").capitalize()],
                names=["ET_AGG", energy_aggregate.index.name],
            )

            data.append(energy_aggregate)

        data = pd.concat(data, axis=0)

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
        #     data

        # energy_sources
        print("energy_sources: ", energy_sources)
        # print("data: ", data)

        # return data, conversion
    else:
        # Filter sources
        df = df.groupby(level=["ET"], axis=1).filter(
            lambda x: x.columns.get_level_values(1).unique() in energy_sources
        )

        if per_balance_aggregate:
            print("per_balance_aggregate: ", per_balance_aggregate)

            for aggregate in balance_aggregates:
                print("aggregate: ", aggregate)

                data = df.groupby(level=["IDX_0"], axis=0).get_group(aggregate)

        elif per_energy_source:
            print("per_energy_source: ", per_energy_source)

            for energy_source in energy_sources:

                data.append(df.groupby(level=["ET"], axis=1).get_group(energy_source))

    # pass

    # if rows == "balance_aggregates" and columns == "energy_sources":
    # if per_year:

    #     # For each year
    #     for year in years:

    #         data = df.groupby(level=["YEAR"], axis=1).get_group(year)

    # if sort_column_by == "province":
    #     data = data.swaplevel(0, 1, axis=1).sort_index(axis=1, level=0)

    # data.loc["Column_Total"] = data.sum(numeric_only=True, axis=0)

    # if len(energy_sources) == 1:
    #     data.loc[:, "Row_Total"] = data.sum(numeric_only=True, axis=1).subtract(
    #         data[data.columns[0]]
    #     )

    # if rows == "energy_sources" and columns == "balance_aggregates":

    # data = data.groupby(level=["ET"], axis=1).filter(
    #     lambda x: x.columns.get_level_values(1).unique() in energy_sources
    # )

    # data = data.groupby(level=["IDX_0"], axis=0).filter(
    #     lambda x: x.index.unique() in balance_aggregates
    # )

    return data, conversion

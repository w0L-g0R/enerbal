from dataclasses import dataclass, field
from datetime import datetime
from pprint import pformat, pprint
from typing import Dict, List
from pandas.core.common import flatten

import pandas as pd
from pandas import IndexSlice as IDX

# from openpyxl.utils.dataframe import dataframe_to_rows, expand_levels

from enspect.models.utils import (
    add_total_per_col,
    add_total_per_row,
    slice_pickled_eb_df,
    check_balance_aggregates_type,
)
import pickle

from enspect.paths import file_paths

# NOTE:code_source=https://stackoverflow.com/questions/58309731/doing-class-objects-filter-pattern-in-python

import functools


def default_kwargs(**default_kwargs):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            default_kwargs.update(kwargs)
            return func(*args, **default_kwargs)

        return inner

    return wrapper


@dataclass
class Data:

    # __slots__ = ['name', 'key', 'frame', "energy_sources", "usage_categories"]
    # Shown as chart name
    name: str = None
    key: str = None

    # # Pickle file name
    # file: str = None

    # Origin of the data
    source: str = None
    created: datetime = datetime.now().strftime("%d_%m_%y_%Hh%Mm")

    # Values
    frame: pd.DataFrame = None
    # shares_over_rows: pd.DataFrame = None
    # shares_over_columns: pd.DataFrame = None
    # indexed: Dict = None
    unit: str = None

    # Data type
    balance_aggregates: List = None  # Balance aggregate e.g. "Importe"
    energy_sources: List = None  # e.g. "Steinkohle"
    energy_aggregates: List = None  # e.g. "Fossil-Fest"
    usage_categories: List = None
    emittents: List = None
    years: List = None
    provinces: List = None
    stats: List = None

    # Data classification
    per_balance_aggregate: bool = False
    per_energy_source: bool = False
    per_energy_aggregate: bool = False
    per_usage_category: bool = False
    per_years: bool = False
    energy_aggregates_sum_only: bool = False
    is_eb: bool = False
    is_res: bool = False
    is_nea: bool = False
    is_thg: bool = False
    is_stat: bool = False

    # # Chart specific
    # has_overlay: bool = False
    # overlays: List = field(default_factory=lambda: [])

    # # KPI
    # is_KPI: bool = False
    # denominator: pd.DataFrame = None
    # numerator: pd.DataFrame = None

    # # Search pattern
    # order: str = None

    def convert(self, *args):

        # TODO: Link to settings
        conversion = {
            "MWh_2_GWh": 0.001,
            "gwh_2_tj": (1 / 0.27778),
            "tj_2_pj": 0.001,
            "gwh_2_mwh": 1000,
            "tj_2_gwh": 0.27778,
            "tj_2_twh": 0.27778 / 1000,
            "pj_2_tj": 1000,
        }

        self.frame *= conversion[args]
        self.unit = args[0].split("_")[-1]

        return

    def __repr__(self):
        return pformat(
            self.__dict__
            # dict(
            #     name=self.name,
            #     key=self.key,
            #     frame=self.frame,
            #     unit=self.unit,
            #     balance_aggregates=self.balance_aggregates,
            #     energy_sources=self.energy_sources,
            #     energy_aggregates=self.energy_aggregates,
            #     years=self.years,
            #     provinces=self.provinces,
            #     per_balance_aggregate=self.per_balance_aggregate,
            #     per_energy_source=self.per_energy_source,
            #     per_energy_aggregate=self.per_energy_aggregate,
            #     per_years=self.per_years,
            #     show_source_values_for_energy_aggregates=self.show_source_values_for_energy_aggregates,
            # )
        )

    def __eq__(self, other):
        return self.key == other.key

    @check_balance_aggregates_type
    def create(
        self,
        provinces: List,
        years: List,
        balance_aggregates: List = None,
        energy_sources: List = None,
        energy_aggregates: List = None,
        usage_categories: List = None,
        per_balance_aggregate: bool = False,
        per_energy_source: bool = False,
        per_energy_aggregate: bool = False,
        per_usage_category: bool = False,
        per_years: bool = False,
        is_res: bool = False,
        is_eb: bool = False,
        is_nea: bool = False,
        unit: str = "TJ",
    ):

        if is_res:

            df = pickle.load(open(file_paths["db_pickles"] / "res.p", "rb"))

            # Midx after slicing => rows: BAGGS; columns: PROV, ES, YEAR
            df, balance_aggregates = slice_pickled_eb_df(
                df=df,
                provinces=provinces,
                balance_aggregates=balance_aggregates,
                years=years,
                is_res=True,
            )
            # Fill missing AT values
            # TODO: Put this into conversion process
            for year in years:

                df.loc[IDX[:], IDX["AT", "RES", year]] = (
                    df.loc[IDX[:], IDX[provinces, "RES", year]].copy().sum(axis=1)
                )

            energy_sources = ["RES"]

        elif is_eb:

            # Midx after slicing => rows: BAGGS; columns: PROV, YEAR, ES
            df = pickle.load(open(file_paths["db_pickles"] / "eb.p", "rb"))

            df, balance_aggregates = slice_pickled_eb_df(
                df=df,
                balance_aggregates=balance_aggregates,
                energy_aggregates=energy_aggregates,
                energy_sources=energy_sources,
                years=years,
                provinces=provinces,
                is_eb=True,
            )

        elif is_nea:

            df = (
                pickle.load(open(file_paths["db_pickles"] / "nea.p", "rb")).sort_index(
                    axis=1, level=0
                )
                # .swaplevel(0, 2, axis=1)
            )

            balance_aggregates = list(flatten(balance_aggregates))

            # Filter aggregates
            df = df.loc[
                IDX[balance_aggregates],
                IDX[provinces, energy_sources, usage_categories, years],
            ].copy()

        # Lex-sort for performance (and warnings)
        df = df.copy().fillna(0).sort_index()

        # TODO: Unit check for RES and STATS?

        self.frame = df
        self.unit = unit
        self.balance_aggregates = balance_aggregates
        self.energy_sources = energy_sources
        self.energy_aggregates = energy_aggregates
        self.usage_categories = usage_categories
        self.years = years
        self.provinces = provinces
        self.per_balance_aggregate = per_balance_aggregate
        self.per_energy_source = per_energy_source
        self.per_energy_aggregate = per_energy_aggregate
        self.per_years = per_years
        self.per_usage_category = per_usage_category
        self.is_eb = is_eb
        self.is_res = is_res
        self.is_nea = is_nea

        return


class FilterData:
    def __init__(self, data):
        self.data = data

    # def __repr__(self):
    #     return [x.name for x in self.data]

    def _filter_step(self, key, value, data):
        if not "__" in key:
            return (entry for entry in data if getattr(entry, key) == value)
        else:
            key, operator = key.split("__")
            if operator == "gt":  # greater than
                return (entry for entry in data if getattr(entry, key) > value)
            elif operator == "lt":  # less than
                return (entry for entry in data if getattr(entry, key) < value)
            elif operator == "startswith":  # starts with
                return (
                    entry for entry in data if getattr(entry, key).startswith(value)
                )
            elif operator == "in":  # is in
                return (entry for entry in data if getattr(entry, key) in value)
            elif operator == "contains":  # contains
                return (entry for entry in data if value in getattr(entry, key))
            else:
                raise UnknownOperator("operator %s is unknown" % operator)

    def _exclude_step(self, key, value, data):
        if not "__" in key:
            return (entry for entry in data if getattr(entry, key) != value)
        else:
            key, operator = key.split("__")
            if operator == "gt":  # greater than
                return (entry for entry in data if getattr(entry, key) <= value)
            elif operator == "lt":  # less than
                return (entry for entry in data if getattr(entry, key) >= value)
            elif operator == "startswith":  # starts with
                return (
                    entry for entry in data if not getattr(entry, key).startswith(value)
                )
            elif operator == "in":  # starts with
                return (entry for entry in data if getattr(entry, key) not in value)
            elif operator == "is_kpi":  # starts with
                return (entry for entry in data if getattr(entry, key) not in value)
            else:
                raise UnknownOperator("operator %s is unknown" % operator)

    def filter(self, **kwargs):
        data = (entry for entry in self.data)
        for key, value in kwargs.items():
            data = self._filter_step(key, value, data)

        return FilterData(data)

    def exclude(self, **kwargs):
        data = (entry for entry in self.data)
        for key, value in kwargs.items():
            data = self._exclude_step(key, value, data)

        return FilterData(data)

    def all(self):
        return FilterData(self.data)

    def count(self):
        cnt = 0
        for cnt, entry in enumerate(self.data, 1):
            pass
        return cnt

    def __iter__(self):
        for entry in self.data:
            yield entry


class UnknownOperator(Exception):
    """ custom exception """

    # def __repr__(self):
    #     return [entry for entry in self.data]


#    def xlsx_formatted(self):

# dfs = {}
# if self.per_balance_aggregate:

#     for year in self.years:
#         dfs[year] = {}

#         for energy_source in self.energy_sources:
#             print("energy_source: ", energy_source)

#             df = (
#                 self.frame.loc[IDX[:], IDX[year, energy_source, :,]]
#                 .swaplevel(0, 1, axis=1)
#                 .stack([0, 1])
#                 # .sort_values(["ET_AGG",])
#             )

#             df = add_total_per_col(df=df)

#             df.reset_index(inplace=True)

#             # df_sums = df.groupby("ES").get_group("SUM")
#             df.drop(["ES", "YEAR"], inplace=True, axis=1)
#             df = add_total_per_row(df=df)
#             df.iloc[-1, 0] = "SUM"

#             dfs[year][energy_source] = df

# All energy aggregates
# elif self.per_energy_aggregate:

#     for year in self.years:
#         dfs[year] = {}

#         for aggregate in self.balance_aggregates:

#             df = (
#                 self.frame.loc[IDX[:, :], IDX[year, aggregate, :,]]
#                 .swaplevel(0, 1, axis=1)
#                 .stack([0, 1])
#                 # .sort_values(["ET_AGG",])
#             )

#             df = add_total_per_col(df=df)

#             df.reset_index(inplace=True)

#             df_sums = df.groupby("ES").get_group("SUM")
#             df_sums.drop(["ES", "BAGG_0", "YEAR"], inplace=True, axis=1)
#             df_sums = add_total_per_row(df=df_sums)
#             df_sums.iloc[-1, 0] = "SUM"

#             _dfs = []
#             _dfs.append(df_sums)

#             df.drop(["BAGG_0", "YEAR"], inplace=True, axis=1)
#             _dfs.append(df)

#             dfs[year][aggregate] = _dfs

# # All years
# else:
#     for energy_source in self.energy_sources:

#         dfs[energy_source] = {}

#         for aggregate in self.balance_aggregates:

#             df = (
#                 self.frame.loc[IDX[:], IDX[energy_source, aggregate, :],]
#                 .swaplevel(0, 1, axis=1)
#                 .stack([0, 1])
#                 .sort_values(["ES", "YEAR"])
#             )

#             df.reset_index(inplace=True)

#             dfs[energy_source][aggregate] = df
#     # data

# return dfs

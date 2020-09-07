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
from enspect.settings import unit_conversions


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

    name: str = None
    key: str = None

    # Origin of the data
    source: str = None
    created: datetime = datetime.now().strftime("%d_%m_%y_%Hh%Mm")
    file: str = None
    # Values
    frame: pd.DataFrame = None
    unit: str = None

    # Data inputs
    provinces: List = None
    years: List = None
    balance_aggregates: List = None
    energy_sources: List = None
    energy_aggregates: List = None
    usage_categories: List = None
    emittent_sinks: List = None

    # Y-axis data
    stacked_balance_aggregates: bool = False
    stacked_energy_sources: bool = False
    stacked_energy_aggregates: bool = False
    stacked_usage_categories: bool = False
    timeseries: bool = False
    stacked_emittent_shares: bool = False

    # Flags
    is_eb: bool = False
    is_res: bool = False
    is_nea: bool = False
    is_thg: bool = False
    is_stat: bool = False
    energy_aggregates_sum_only: bool = False

    # Transformation
    transformed_to_new_unit: str = None
    transformed_column_percentages: bool = False
    transformed_row_percentages: bool = False
    transformed_reference_year: bool = False

    # Add on
    has_column_percentage: bool = False

    # # Chart specific
    # has_overlay: bool = False
    # overlays: List = field(default_factory=lambda: [])

    # # KPI
    # is_KPI: bool = False
    # denominator: pd.DataFrame = None
    # numerator: pd.DataFrame = None

    # # Search pattern
    # order: str = None

    @property
    def frame(self):

        frame = self._frame.copy()  # .sort_index()

        # Unit conversion
        if self.new_unit is not None:

            key = self.unit + "_2_" + self.new_unit

            frame = self._frame * unit_conversions[key]

        # Get shares for each each per column
        if self.is_column_percentages:

            numerator = frame.loc[
                IDX[:], IDX[frame.columns.isin(self.provinces)]
            ].copy()

            denominator = frame.loc[
                IDX["SUM"], IDX[frame.columns.isin(self.provinces)]
            ].copy()

            frame.loc[IDX[:], IDX[frame.columns.isin(self.provinces)]] = round(
                (numerator / denominator), 3
            )

            self.new_unit = "%"

        elif self.is_row_percentages:
            pass

        elif self.is_reference_year:
            pass

        return frame

    @frame.setter
    def frame(self, frame: pd.DataFrame):
        # TODO: Catch mispelled unit names here (lookup in dict)

        self._frame = frame

    def __repr__(self):
        return pformat(self.__dict__)

    def __eq__(self, other):
        return self.key == other.key

    @check_balance_aggregates_type
    def create(
        self,
        provinces: List,
        years: List,
        balance_aggregates: List = None,
        energy_sources: List = None,
        emittent_shares: List = None,
        energy_aggregates: List = None,
        usage_categories: List = None,
        stacked_balance_aggregates: bool = False,
        stacked_energy_sources: bool = False,
        stacked_energy_aggregates: bool = False,
        stacked_usage_categories: bool = False,
        timeseries: bool = False,
        stacked_emittent_shares: bool = False,
        is_res: bool = False,
        is_eb: bool = False,
        is_nea: bool = False,
        is_thg: bool = False,
        is_stat: bool = False,
        unit: str = "TJ",
        file: str = None,
    ):

        if is_res:

            source = "Energiebilanzen Österreich"
            energy_sources = ["RES"]
            file = file_paths["pickle_res"]

            with open(file, "rb") as f:
                df = pickle.load(f)

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

        elif is_eb:

            source = "Energiebilanzen Österreich"
            file = file_paths["pickle_eb"]

            with open(file, "rb") as f:
                df = pickle.load(f)

            # Midx after slicing => rows: BAGGS; columns: PROV, YEAR, ES
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

            source = "Nutzenergieanalysen Österreich"
            file = file_paths["pickle_eb"]

            with open(file, "rb") as f:

                df = pickle.load(f).sort_index(axis=1, level=0)

            balance_aggregates = list(flatten(balance_aggregates))

            # Filter aggregates
            df = df.loc[
                IDX[balance_aggregates],
                IDX[provinces, energy_sources, usage_categories, years],
            ].copy()

        elif is_thg:

            source = "Luftschadstoffinventur UBM"
            energy_sources = emittent_shares
            file = file_paths["pickle_thg"]

            with open(file, "rb") as f:
                df = pickle.load(f).sort_index(axis=1, level=0)

            balance_aggregates = list(flatten(balance_aggregates))

            # Filter aggregates
            df = df.loc[
                IDX[balance_aggregates], IDX[provinces, emittent_shares, years],
            ].copy()

            unit = "kton CO2-Eq."

        elif is_stat:

            with open(file, "rb") as f:
                stats = pickle.load(f)

            print("stats: ", stats)

            df = stats["df"]
            # print("frame: ", frame)

            source = stats["source"]
            # print("source: ", source)

            # print(df)
            name = stats["name"]

        # Lex-sort for performance (and warnings)
        df = df.copy().fillna(0).sort_index()

        print("\n CREATE DATA: \n", df)

        # TODO: Unit check for RES and STATS?

        self.frame = df
        self.unit = unit
        self.name = name
        self.balance_aggregates = balance_aggregates
        self.energy_sources = energy_sources
        self.emittent_shares = emittent_shares
        self.energy_aggregates = energy_aggregates
        self.usage_categories = usage_categories
        self.years = years
        self.provinces = provinces
        self.stacked_balance_aggregates = stacked_balance_aggregates
        self.stacked_energy_sources = stacked_energy_sources
        self.stacked_energy_aggregates = stacked_energy_aggregates
        self.timeseries = timeseries
        self.stacked_usage_categories = stacked_usage_categories
        self.stacked_emittent_shares = stacked_emittent_shares
        self.is_eb = is_eb
        self.is_res = is_res
        self.is_nea = is_nea
        self.is_thg = is_thg
        self.provinces = provinces
        self.file = file
        self.source = source

        return

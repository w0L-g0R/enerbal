from typing import NewType
import os
import logging
import pickle
from typing import List, Union, Optional
from copy import deepcopy
from time import gmtime, strftime

import pandas as pd
import numpy as np
from pathlib import Path
from pandas.core.common import flatten

from enspect.settings import (
    file_paths,
    provinces_hex,
    provinces,
    unit,
)
from enspect.files.energiebilanzen.data_structures import energy_aggregate_lookup
from enspect.models.utils import (
    # add_sums,
    # add_means,
    # get_shares,
    # apply_single_index,
    # convert,
    # drop_eb_row_levels,
    slice_eb_inputs,
    add_row_total,
    # get_eb_energy_aggregates,
    # get_eb_energy_soures,
    # get_eb_balance_aggregates,
    # get_eb_over_all_years,
    # post_process,
)

from enspect.models.data import Data, FilterData
from enspect.files.energiebilanzen.data_structures import (
    eev_aggregates,
    sectors,
    sector_energy,
)
from copy import deepcopy

IDX = pd.IndexSlice


class DataSet:
    def __init__(self, name: str, file_paths=file_paths):
        self._objects = []
        self.name = name
        logging.getLogger().error(f"Added: {self.name}")
        return

    @property
    def objects(self):
        return FilterData(self._objects)

    def __repr__(self):
        return self.name

    # @property
    # def data(self):
    #     return self._data

    @objects.setter
    def objects(self, _objects: List = list):
        # print(data)
        # if not isinstance(_objects, list):
        #     _objects = [_objects]

        _ids = [
            data._id
            for data in self._objects
            # if not isinstance(_object, list)
        ]

        print("_ids: ", _ids)

        # if not _ids:
        self._objects.append(_objects)
        # else:
        #     # for _id in _ids:
        #     #     print("_object: ", data.name)
        #     if data._id in _ids:
        #         pass
        #     else:
        #         self._objects.append(data)

        _ids = [
            data._id
            for data in self._objects
            # if not isinstance(_object, list)
        ]

        print("_ids: ", _ids)

    def add_eb_data(
        self,
        provinces: List,
        years: List,
        balance_aggregates: List = None,
        energy_sources: List = None,
        energy_aggregates: List = None,
        per_balance_aggregate: bool = False,
        per_energy_source: bool = False,
        per_energy_aggregate: bool = False,
        per_years: bool = False,
        show_source_values_for_energy_aggregates: bool = False,
    ):

        logging.getLogger().error("/" * 80)

        assert isinstance(
            balance_aggregates, (list, tuple)
        ), "Wrap list or tuple around aggregate!"

        df = (
            slice_eb_inputs(
                df=pickle.load(open(file_paths["db_pickles"] / "eb.p", "rb")),
                balance_aggregates=balance_aggregates,
                years=years,
            )
            .swaplevel(0, 2, axis=1)
            .sort_index(axis=1, level=0)
        )

        data = Data(
            # frame=frame,
            unit="TJ",
            balance_aggregates=balance_aggregates,
            energy_sources=energy_sources,
            energy_aggregates=energy_aggregates,
            years=years,
            provinces=provinces,
            per_balance_aggregate=per_balance_aggregate,
            per_energy_source=per_energy_source,
            per_energy_aggregate=per_energy_aggregate,
            per_years=per_years,
            show_source_values_for_energy_aggregates=show_source_values_for_energy_aggregates,
        )

        print("df head: ", df.head())

        if per_energy_aggregate:

            self.add_eb_energy_aggregates(df=df, data=data)

        else:
            # TODO: Get rid of lambda - replace with loc
            # Filter sources
            df = df.groupby(level=["ET"], axis=1).filter(
                lambda x: x.columns.get_level_values(1).unique() in energy_sources
            )

            if per_balance_aggregate:

                self.add_eb_balance_aggregates(df=df, data=data)

            elif per_energy_source:

                self.add_eb_balance_aggregates(df=df, data=data)

            # All years
            elif per_years:
                self.add_eb_over_all_years(df=df, data=data)
        return

    # ////////////////////////////////////////////////////////////////// E-AGGS

    def add_eb_energy_aggregates(self, df: pd.DataFrame, data: Data):

        # Get all energy sources for selected energy aggregates
        energy_sources = list(
            flatten(
                [energy_aggregate_lookup[source] for source in data.energy_aggregates]
            )
        )

        # Filter energy sources from pickled df
        # TODO: Get rid of lambda - replace with loc

        df = (
            df.groupby(level=["ET"], axis=1)
            .filter(lambda x: x.columns.get_level_values(1).unique() in energy_sources)
            .stack("ET")
            .unstack("IDX_0")
        )

        for balance_aggregate in data.balance_aggregates:

            # Use lookup table for slicing
            _df = df.groupby(level=["IDX_0"], axis=1).get_group(balance_aggregate)

            _energy_aggregates = []

            # Iter over energy aggregates
            for energy_aggregate in data.energy_aggregates:

                # Use lookup table for slicing
                # TODO: Maybe Get rid of lambda - replace with loc

                __df = _df.groupby(level=["ET"], axis=0).filter(
                    lambda x: x.index in energy_aggregate_lookup[energy_aggregate]
                )

                __df.loc["SUM", :] = __df.sum(numeric_only=True, axis=0)

                # Create multiindex with energy_aggregate as first idx
                __df.index = pd.MultiIndex.from_product(
                    iterables=[[energy_aggregate], list(__df.index),],
                    names=["ET_AGG", __df.index.name],
                )

                name = "_".join(["Energie_Aggregate", balance_aggregate])

                _id = "_".join(
                    [
                        "EAGGS",
                        balance_aggregate[:3].upper(),
                        str(data.years[0])[-2:],
                        str(data.years[-1])[-2:],
                    ]
                )

                _energy_aggregates.append(__df)

            # Copy
            _data = deepcopy(data)

            # Concat
            _df = pd.concat(_energy_aggregates, axis=0)

            # Swap
            _df = _df.swaplevel("BL", "IDX_0", axis=1).sort_index(axis=1, level=0)

            # Assign and rename
            _data.name, _data._id, _data.frame = (name, _id, _df)

            self.objects = _data

    # ////////////////////////////////////////////////////////////////// E-SRCS

    def add_eb_balance_aggregates(self, df: pd.DataFrame, data: pd.DataFrame):

        for energy_source in data.energy_sources:
            # Copy
            _data = deepcopy(data)

            # Info update
            _data.energy_aggregates = None
            _data.energy_sources = energy_source

            name = "_".join([energy_source.replace(" ", "_"), "Bilanz_Aggregate",])

            _id = "_".join(
                [
                    "BAGGS",
                    energy_source.replace(" ", "_")[:3].upper(),
                    str(data.years[0])[-2:],
                    str(data.years[-1])[-2:],
                ]
            )

            # Slice
            _df = df.groupby(level=["ET"], axis=1).get_group(energy_source)

            _data.name, _data._id, _data.frame = (name, _id, _df)

            # self.add_object(data=_data)
            self.objects = _data

        return data

    # ////////////////////////////////////////////////////////////////// YEARLY

    def add_eb_over_all_years(self, df: pd.DataFrame, data: Data):

        name = "Year"

        _id = "_".join(("YEARS", str(data.years[0])[-2:], str(data.years[-1])[-2:]))

        _df = df.stack("YEAR").unstack("IDX_0")

        _df = _df.swaplevel("BL", "IDX_0", axis=1).sort_index(axis=1, level=0)

        data.name, data._id, data.frame = (name, _id, _df)

        # self.add_object(data=_data)
        self.objects = data

    # //////////////////////////////////////////////////////////////// E-SRCS

    def add_nea_data(
        self,
        provinces: List,
        years: List,
        balance_aggregates: List = None,
        energy_sources: List = None,
        usage_categories: List = None,
        per_usage_category: bool = False,
        per_balance_aggregate: bool = False,
        per_energy_source: bool = False,
        and_usage_category: bool = False,
        and_balance_aggregate: bool = False,
        and_energy_source: bool = False,
        per_years: bool = False,
    ):

        logging.getLogger().error("/" * 80)

        assert isinstance(
            balance_aggregates, (list, tuple)
        ), "Wrap list or tuple around aggregate!"

        df = (
            pickle.load(open(file_paths["db_pickles"] / "nea.p", "rb")).sort_index(
                axis=1, level=0
            )
            # .swaplevel(0, 2, axis=1)
        )

        print("df head: ", df.head())
        # df = df.sort_index()
        print("df head: ", df.head())
        # Filter aggregates
        df = df.loc[
            IDX[balance_aggregates],
            IDX[provinces, energy_sources, usage_categories, years],
        ]

        data = Data(
            # frame=frame,
            unit="TJ",
            balance_aggregates=balance_aggregates,
            energy_sources=energy_sources,
            usage_categories=usage_categories,
            years=years,
            provinces=provinces,
            per_usage_category=per_usage_category,
            per_balance_aggregate=per_balance_aggregate,
            per_energy_source=per_energy_source,
            and_usage_category=and_usage_category,
            and_balance_aggregate=and_balance_aggregate,
            and_energy_source=and_energy_source,
            per_years=per_years,
        )

        # /////////////////////////////////////////////////////////// PER E-SRC

        # CASE 1.1: X-Axis: UC, Y-Axis: Stacked SEC
        if int(per_energy_source) + int(and_usage_category) == 2:

            for energy_source in data.energy_sources:
                _df = df.groupby(level=["ET"], axis=1).get_group(energy_source)

                for usage_category in data.usage_categories:
                    __df = _df.groupby(level=["USAGE"], axis=1).get_group(
                        usage_category
                    )
                    for year in years:
                        ___df = __df.groupby(level=["YEAR"], axis=1).get_group(year)
                        print("___df: ", ___df)

            pass
        # CASE 1.2: X-Axis: SEC, Y-Axis: Stacked UC
        elif int(per_energy_source) + int(and_balance_aggregate) == 2:

            for energy_source in data.energy_sources:
                _df = df.groupby(level=["ET"], axis=1).get_group(energy_source)

                for balance_aggregate in data.balance_aggregates:
                    __df = _df.groupby(level=["SECTOR"], axis=0).get_group(
                        balance_aggregate
                    )
                    for year in years:
                        ___df = __df.groupby(level=["YEAR"], axis=1).get_group(year)

                        index = ___df.columns.get_level_values(level="USAGE").unique()

                        ___df = ___df.stack("USAGE").unstack("SECTOR")

                        ___df = ___df.reindex(index)

                        print("___df: ", ___df)
                        print()

        # /////////////////////////////////////////////////////////// PER B-AGG

        # CASE 2.1: X-Axis: ET, Y-Axis: Stacked UC
        elif per_balance_aggregate:

            for balance_aggregate in data.balance_aggregates:
                _df = df.groupby(level=["SECTOR"], axis=0).get_group(balance_aggregate)

                # for energy_source in data.energy_sources:
                #     __df = _df.groupby(level=["ET"], axis=1).get_group(energy_source)

                for year in years:

                    __df = _df.groupby(level=["YEAR"], axis=1).get_group(year)

                    # CASE 3.1: X-Axis: SEC, Y-Axis: Stacked ET
                    if and_usage_category:
                        index = __df.columns.get_level_values(level="USAGE").unique()

                        __df = __df.stack("USAGE").unstack("SECTOR")

                        __df = __df.reindex(index)

                        print("_df: ", _df)

                    if and_energy_source:

                        print("__df: ", __df)

        # CASE 2.2: X-Axis: UC, Y-Axis: Stacked ET
        # elif int(per_balance_aggregate) + int(and_usage_category) == 2:

        #     for balance_aggregate in data.balance_aggregates:
        #         _df = df.groupby(level=["SECTOR"], axis=0).get_group(balance_aggregate)

        #         # for usage_category in data.usage_categories:
        #         #     __df = _df.groupby(level=["USAGE"], axis=1).get_group(
        #         #         usage_category
        #         #     )
        #         for year in years:
        #             ___df = __df.groupby(level=["YEAR"], axis=1).get_group(year)

        #             index = ___df.columns.get_level_values(level="ET").unique()

        #             ___df = ___df.stack("ET").unstack("SECTOR")

        #             ___df = ___df.reindex(index)

        #             print("___df: ", ___df)
        #             print()

        # /////////////////////////////////////////////////////////// PER UC

        elif per_usage_category:

            for usage_category in data.usage_categories:
                _df = df.groupby(level=["USAGE"], axis=1).get_group(usage_category)

                # for energy_source in data.energy_sources:
                #     __df = _df.groupby(level=["ET"], axis=1).get_group(energy_source)

                for year in data.years:
                    __df = _df.groupby(level=["YEAR"], axis=1).get_group(year)

                    # CASE 3.1: X-Axis: SEC, Y-Axis: Stacked ET
                    if and_balance_aggregate:

                        index = __df.columns.get_level_values(level="ET").unique()

                        __df = __df.stack("ET").unstack("SECTOR")

                        __df = __df.reindex(index)

                        print("___df: ", ___df)

                    # CASE 3.2: X-Axis: ET, Y-Axis: Stacked SEC

                    elif and_energy_source:
                        print("__df: ", __df)

        # CASE 2.2: X-Axis: ET, Y-Axis: Stacked UC
        # elif int(per_usage_category) + int(and_energy_source) == 2:

        #     for usage_category in data.usage_categories:
        #         _df = df.groupby(level=["USAGE"], axis=1).get_group(usage_category)

        #         for balance_aggregate in data.balance_aggregates:
        #             __df = _df.groupby(level=["SECTOR"], axis=0).get_group(
        #                 balance_aggregate
        #             )

        #             for year in years:
        #                 ___df = __df.groupby(level=["YEAR"], axis=1).get_group(year)

        #                 # index = ___df.columns.get_level_values(level="ET").unique()

        #                 # ___df = ___df.stack("ET").unstack("SECTOR")

        #                 # ___df = ___df.reindex(index)

        #                 print("___df: ", ___df)
        #                 print()
        return

    # def get_data_per_energy_source_and_usage_category(
    #     self, df: pd.DataFrame, data: pd.DataFrame
    # ):

    #     for energy_source in data.energy_sources:
    #         # Copy
    #         _data = deepcopy(data)

    #         # Info update
    #         _data.energy_aggregates = None
    #         _data.energy_sources = energy_source

    #         name = "_".join([energy_source.replace(" ", "_"), "Bilanz_Aggregate",])

    #         _id = "_".join(
    #             [
    #                 "BAGGS",
    #                 energy_source.replace(" ", "_")[:3].upper(),
    #                 str(data.years[0])[-2:],
    #                 str(data.years[-1])[-2:],
    #             ]
    #         )

    #         # Slice
    #         _df = df.groupby(level=["ET"], axis=1).get_group(energy_source)

    #         _data.name, _data._id, _data.frame = (name, _id, _df)

    #         # self.add_object(data=_data)
    #         self.objects = _data

    #     return data

    # @staticmethod
    # def get_eb_balance_aggregates(df: pd.DataFrame, data: Data):
    #     for aggregate in data.balance_aggregates:

    #         data.frame = df.groupby(
    #             level=["IDX_0"], axis=0).get_group(aggregate)
    #         # data.frame

    #     return data
    # if rows == "balance_aggregates" and columns == "energy_sources":
    # if per_year:

    #     data = [
    #         df.groupby(level=["YEAR"], axis=1).get_group(year) for year in years
    #     ]

    # print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEE: ", data)
    #     data = data
    # print("data: ", data)

    # self.objects = [
    #     Data(
    #         frame=frame,
    #         unit="Tj",
    #         balance_aggregates=balance_aggregates,
    #         energy_sources=energy_sources,
    #         energy_aggregates=energy_aggregates,
    #         years=years,
    #         provinces=provinces,
    #         per_balance_aggregate=per_balance_aggregate,
    #         per_energy_source=per_energy_source,
    #         per_energy_aggregate=per_energy_aggregate,
    #         per_year=per_year,
    #     )
    #     for frame in data
    # ]

    # def add_eb_data_per_sector(
    #     self,
    #     file: Union[str, Path],
    #     aggregate: List,
    #     provinces: List,
    #     years: List,
    #     conversion: Optional[str] = None,
    #     energy_sources: Optional[List] = None,
    #     sectors: Optional[List] = None,
    # ):
    #     logging.getLogger().error("/" * 80)
    #     logging.getLogger().info(f"Adding {file} data per sector:\n{sectors}\n")

    #     # Fetch data
    #     data = pickle.load(open(self.file_paths[file], "rb"))
    #     unit = "TJ"

    #     for year in years:

    #         logging.getLogger().info(f"Year: {year}")

    #         for energy_source in energy_sources:

    #             # Output df which holds sector series
    #             df = pd.DataFrame(index=sectors, columns=provinces)

    #             # Iter over sectors (= actually list of aggregates)
    #             for sector in sectors:

    #                 # Extend with energy source
    #                 name = "_".join([sector, energy_source, str(year),])

    #                 # Slice data for all given provinces and years
    #                 s = data.loc[
    #                     IDX[sector], IDX[tuple(provinces), energy_source, year],
    #                 ]

    #                 # Copy series to output df
    #                 df.loc[sector, provinces] = s.droplevel((1, 2), axis=0).T

    #             # Add sum row and column
    #             df = add_sums(df=df)

    #             # If all sum of sum column == 0, than all values are NaN
    #             if df["Sum"].sum() != 0:

    #                 if conversion is not None:
    #                     df, unit = convert(df=df, conversion=conversion)

    #                 # Share of each province over total provinces per year
    #                 df_shares_per_province = get_shares(df=df, provinces=True)
    #             else:
    #                 # Write NaN df to shares
    #                 df_shares_per_province = df

    #             logging.getLogger().info(f"Added {name} to {self.name}.data_manager")

    #             # Create a Data object
    #             self.data.append(
    #                 Data(
    #                     name=name,
    #                     file="sec",
    #                     source="Energiebilanzen Bundesländer, EEV nach Sektoren",
    #                     unit=unit,
    #                     frame=df,
    #                     aggregate=aggregate,
    #                     energy_source=energy_source,
    #                     shares_over_columns=df_shares_per_province,
    #                     provinces=provinces,
    #                     years=years,
    #                     sectors=sectors,
    #                     order="per_sector",
    #                 )
    #             )

    # def add_stats_data_per_years(
    #     self, file: Union[str, Path], provinces: List, years: List, name: str,
    # ):
    #     logging.getLogger().error("/" * 80)

    #     data = pickle.load(open(self.file_paths[file], "rb"))

    #     if file == "pop":

    #         # Unit
    #         unit = "Person"
    #         aggregate = name
    #         name = "_".join(
    #             [aggregate, str(data["df"].index[0]), str(data["df"].index[-1])]
    #         )

    #     if file == "km_pkw":

    #         # Unit
    #         unit = "km"
    #         aggregate = name
    #         name = "_".join(
    #             [aggregate, str(data["df"].index[0]), str(data["df"].index[-1])]
    #         )

    #     # Slice pickled dataframe
    #     df = pd.DataFrame(index=years, columns=provinces)

    #     logging.getLogger().info(f"Adding {file} data per years:\n{df.index}\n")

    #     # _df = data["df"].loc[years, provinces]

    #     for index, row in df.iterrows():
    #         try:
    #             df.loc[index, :] = data["df"].loc[index, provinces]
    #         except BaseException:
    #             pass

    #     # Compute sums on rows axis (years) and on col axis (provinces)
    #     df = add_sums(df=df)

    #     # Create shares
    #     # Share of each year over total years per province
    #     df_shares_per_year = get_shares(df=df, years=True)
    #     # print("pop_shares_years: ", df_shares_per_year)

    #     # Share of each province over total provinces per year
    #     df_shares_per_province = get_shares(df=df, provinces=True)
    #     # print("pop_shares_provinces: ", df_shares_per_province)

    #     logging.getLogger().info(f"Added {name} to {self.name}.data_manager")

    #     # Create a Data object
    #     self.data.append(
    #         Data(
    #             name=name,
    #             source=df.index.name,
    #             aggregate=aggregate,
    #             frame=df,
    #             shares_over_rows=df_shares_per_year,
    #             shares_over_columns=df_shares_per_province,
    #             unit=unit,
    #             file=file,
    #             provinces=provinces,
    #             years=years,
    #             order="per_years",
    #         )
    #     )
    #     return

    # def add_overlay(
    #     self,
    #     chart_type: str,
    #     to_data: List = None,
    #     overlays: List = None,
    #     scalings: List = ["absolute"],
    # ):

    #     assert overlays != [], "No data for overlay"
    #     assert to_data != [], "No dataset to write overlay to."

    #     # If only one scale arg, use this one for all overlay series
    #         if not isinstance(scalings, list):
    #         scalings = [scalings]
    #         if len(scalings) != len(overlays):
    #             scalings = [scalings[0] for x in range(len(scalings))]

    #     # Iter over datasets and add overlay
    #     for overlay, scale in zip(overlays, scalings):

    #         for data in to_data:

    #             data.overlays.append({"data": overlay, "scale": scale})

    #             logging.getLogger().info(
    #                 f"Added {overlay.name} to {data.name} as overlay."
    #             )

    #             data.has_overlay = True

    #     return

    def add_indicator(
        self,
        aggregate: str,
        numerator: Data,
        denominator: Data,
        # years: List,
        # provinces: List,
    ):

        logging.getLogger().error("/" * 80)

        assert numerator != [], "No data for numerator."
        assert denominator != [], "No data for denominator."
        # print('denominator: ', denominator)
        # print('numerator: ', numerator)

        name = "_pro_".join([numerator[0].name, denominator[0].name])
        unit = " / ".join([numerator[0].unit, denominator[0].unit])

        # Select first year
        # years_start = max(denominator.years[0], numerator.years[0], years[0])
        # years_end = min(denominator.years[-1], numerator.years[-1], years[-1])
        # years = list(range(years_start, years_end + 1, 1))
        # NOTE: years index of stats gets adapted in add_stats functions!
        # years.append("Sum")
        df_numerator = numerator[0].frame
        df_denominator = denominator[0].frame

        assert len(df_numerator) == len(
            df_numerator
        ), "Dataframe index length mismatch!"

        df = df_numerator / df_denominator

        df = df.drop("Sum", axis=1)
        df = df.drop("Sum", axis=0)

        # Compute sums on rows axis (years) and on col axis (provinces)
        df = add_means(df=df)

        # Create shares
        # Share of each year over total years per province
        df_shares_per_year = get_shares(df=df, years=True)
        # print("df_shares_years: ", df_shares_per_year)

        # Share of each province over total provinces per year
        df_shares_per_province = get_shares(df=df, provinces=True)
        # print("df_shares_provinces: ", df_shares_per_province)

        logging.getLogger().info(
            f"Added KPI with {name} with unit {unit} to {self.name}.data_manager as KPI"
        )

        self.data.append(
            Data(
                name=name,
                frame=df,
                aggregate=aggregate,
                shares_over_rows=df_shares_per_year,
                shares_over_columns=df_shares_per_province,
                unit=unit,
                provinces=provinces,
                years=[x for x in df.index if not isinstance(x, str)],
                denominator=denominator[0],
                numerator=numerator[0],
                is_KPI=True,
                order="per_years",
            )
        )
        return

    # def add_nea_per_years(
    #     self,
    #     file: Union[str, Path],
    #     provinces: List,
    #     years: List,
    #     energy_sources: List = None,
    #     usage_categories: List = None,
    #     sectors: List = None,
    #     conversion: str = None,
    # ):
    #     logging.getLogger().error("/" * 80)
    #     logging.getLogger().info(f"Adding {file} data per years:\n{years}\n")

    #     # Fetch data
    #     data = pickle.load(open(self.file_paths[file], "rb"))

    #     for year in years:

    #         logging.getLogger().info(f"Year: {year}")

    #         # Create a searchable name
    #         name = "_".join(
    #             [
    #                 "Energetischer_Endverbrauch",
    #                 energy_source,
    #                 usage_category,
    #                 sectors,
    #                 str(years[0]),
    #                 str(years[-1]),
    #             ]
    #         )

    #         # # IDX rows = ENERGY SOURCE
    #         # # IDX columns PROV, AGGREGATE, USAGE CAT, YEARS
    #         # nea_df.loc[IDX[:], IDX["Ktn", "Gesamt (ohne E1 - E7)", "Dampferzeugung", 2000]]

    #         # Slice data for all given provinces and years
    #         df = data.loc[
    #             # Energy Source
    #             IDX[tuple(aggregate)],
    #             # Provinde, Sector, Usage Cat, Year
    #             IDX[tuple(provinces), tuple(sectors), tuple(usage_categories), tuple(years)
    #                 ],
    #         ]

    #         # Transform data values to new unit scale
    #         if conversion is not None:

    #             # Convert to other units
    #             df *= conversion_multiplicators[conversion]

    #             # Assign new unit
    #             unit = conversion.split("_")[-1]
    #             print('unit: ', unit)

    #         df = apply_single_index(df=df)

    #         # Sum column and row
    #         df = add_sums(df=df)

    #         # # Share of each year over total years per province
    #         # df_shares_per_year = get_shares(df=df, years=True)

    #         # # Share of each province over total provinces per year
    #         # df_shares_per_province = get_shares(df=df, provinces=True)

    #         logging.getLogger().info(
    #             f"Added {name} to {self.name}.data_manager")

    #         # Create Data object
    #         self.data.append(
    #             Data(
    #                 # title=name,
    #                 name=name,
    #                 file="nea",
    #                 source="Nutzenergieanalysen Bundesländer",
    #                 unit="TJ",
    #                 frame=df,
    #                 aggregate=aggregate[0],
    #                 energy_source=energy_source,
    #                 shares_over_rows=df_shares_per_year,
    #                 shares_over_columns=df_shares_per_province,
    #                 provinces=provinces,
    #                 years=years,
    #                 order="per_years"
    #             )
    #         )

    #         return

    # for year in years:

    #     data = group.groupby(level=["YEAR"], axis=1).get_group(year)

    # shares_over_rows = (
    #     data.groupby(level="BL", axis=1)
    #     .apply(lambda x: 100 * x / float(x.sum()))
    #     .round(2)
    # )

    # shares_over_rows_sum = data.groupby(level="BL", axis=1).sum()
    # print("shares_over_rows_sum: ", shares_over_rows_sum)
    # shares_over_rows = data / shares_over_rows_sum

    # shares_over_cols = (
    #     data.groupby(level=0, axis=0)
    #     .apply(lambda x: 100 * x / float(x.iloc[:, 1:].sum(axis=1)))
    #     .round(2)
    # )

    # if sort_column_by == "province":
    #     data = data.swaplevel(0, 1, axis=1).sort_index(axis=1, level=0)

    # data.loc["Column_Total"] = data.sum(numeric_only=True, axis=0)

    # if len(energy_sources) == 1:
    #     data.loc[:, "Row_Total"] = data.sum(
    #         numeric_only=True, axis=1
    #     ).subtract(data[data.columns[0]])

    # data *= unit[conversion]
    # data = round(data, 2)
    # print("data: ", data)

    # print("shares_over_rows: ", shares_over_rows)
    # print("shares_over_cols: ", shares_over_cols)
    # Slice data for all given provinces and years
    # eb_df = data.loc[
    #     IDX[aggregates], IDX[provinces, energy_sources, years],
    # ]

    # print("per: ", per)
    # if per == "sources_per_agg_and_year":

    #     for aggregate in aggregates:
    #         print("aggregate: ", aggregate)

    #         for year in years:
    #             print("_" * 70)
    #             print("year: ", year)

    #             # Slice data for all given provinces and years
    #             df = eb_df.loc[
    #                 IDX[aggregate], IDX[provinces, energy_sources, year],
    #             ]

    #             aggregate_name = "_".join([x for x in aggregate if x != "Gesamt"])

    #             aggregate_name = aggregate_name.replace(" ", "_")
    #             aggregate_name = aggregate_name.replace(".", "")

    #             df.index.name = "_".join(["SRC", aggregate_name, str(year)])

    #             # df, df_shares, unit = post_process(df=df, conversion=conversion)

    #             # Create Data object
    #             self.data.append(
    #                 Data(
    #                     # title=name,
    #                     name="_".join(["SRC", aggregate_name, str(year)]),
    #                     file="eb",
    #                     source="Energiebilanzen Bundesländer",
    #                     unit=unit,
    #                     frame=df,
    #                     balance_aggregates=aggregates,
    #                     energy_sources=energy_sources,
    #                     shares_over_rows=df_shares["rows"],
    #                     shares_over_columns=df_shares["cols"],
    #                     provinces=provinces,
    #                     years=years,
    #                     order="per",
    #                 )
    #             )

    # if per == "aggs_per_source_and_year":

    #     print("PRINTS")

    #     for source in energy_sources:

    #         for year in years:

    #             # Slice data for all given provinces and years
    #             df = eb_df.loc[
    #                 IDX[aggregates], IDX[provinces, source, year],
    #             ]

    #             print("df: ", df)

    #             df.index.name = "_".join(("AGG", source, str(year)))

    #             df, df_shares, unit = post_process(df=df, conversion=conversion)

    #             # Create Data object
    #             self.data.append(
    #                 Data(
    #                     # title=name,
    #                     name="_".join(("AGG", year)),
    #                     file="eb",
    #                     source="Energiebilanzen Bundesländer",
    #                     unit=unit,
    #                     frame=df,
    #                     balance_aggregates=aggregates,
    #                     energy_sources=energy_sources,
    #                     shares_over_rows=df_shares["rows"],
    #                     shares_over_columns=df_shares["cols"],
    #                     provinces=provinces,
    #                     years=years,
    #                     order="per",
    #                 )
    #             )

    # elif per == "agg_and_source_for_all_years ":

    #     for source in energy_sources:

    #         for aggregate in aggregates:

    #             # Slice data for all given provinces and years
    #             df = eb_df.loc[
    #                 IDX[aggregate], IDX[provinces, source, years],
    #             ]

    #             aggregate = "_".join([x for x in aggregate if x != "Gesamt"])

    #             aggregate_name = aggregate_name.replace(" ", "_")
    #             aggregate_name = aggregate_name.replace(".", "")

    #             df.index.name = "_".join(("YEARS_", source, aggregate))

    #             logging.getLogger().info(f"Added {df.index.name }")

    #             df, df_shares, unit = post_process(df=df, conversion=conversion)

    #             # Create Data object
    #             self.data.append(
    #                 Data(
    #                     # title=name,
    #                     name=df.index.name,
    #                     file="eb",
    #                     source="Energiebilanzen Bundesländer",
    #                     unit=unit,
    #                     frame=df,
    #                     balance_aggregates=aggregates,
    #                     energy_sources=energy_sources,
    #                     shares_over_rows=df_shares["rows"],
    #                     shares_over_columns=df_shares["cols"],
    #                     provinces=provinces,
    #                     years=years,
    #                     order="per",
    #                 )
    #             )

    # # Add-ons

    # # If all sum of sum column == 0, than all values are # NaN
    # if df["Sum"].sum() != 0:

    #     # Share of each year over total years per province
    #     # df_shares_per_year = get_shares(df=df, years=True)

    # else:
    #     # Write NaN df to shares

    # df_shares_per_year = df

    # # # Transform data values to new unit scale
    # # df, unit = convert(df=df, conversion=conversion)

    # # # Share of each year over total years per province
    # # df_shares_per_year = get_shares(df=df, years=True)

    # # # Share of each province over total provinces per year
    # # df_shares_per_province = get_shares(df=df, provinces=True)

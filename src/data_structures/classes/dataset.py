import os
import logging
import pickle
from typing import List, Union
from copy import deepcopy
from time import gmtime, strftime

import pandas as pd
import numpy as np
from pathlib import Path

from settings import file_paths, provinces_hex, provinces

from data_structures.utils import (add_sums,
                                   add_means,
                                   get_shares,
                                   apply_single_index)

from data_structures.classes.data import Data, FilterData


IDX = pd.IndexSlice


class DataSet:
    def __init__(self, name: str, file_paths=file_paths, data: List = list()):
        self.data = data
        self.name = name
        self.file_paths = file_paths
        logging.getLogger().error(f"Added: {self.name}")
        return

    @property
    def objects(self):
        return FilterData(self.data)

    def __repr__(self):
        return self.name

    def add_eb_data_per_years(
        self,
        file: Union[str, Path],
        aggregate: List,
        provinces: List,
        years: List,
        energy_sources: List = None,
    ):
        logging.getLogger().error("/" * 80)
        logging.getLogger().info(f"Adding {file} data per years:\n{years}\n")

        # Fetch data
        data = pickle.load(open(self.file_paths[file], "rb"))

        # Aggregate name without "Gesamt"
        aggregate_cleaned = "_".join(
            [x for x in [aggregate] if x != "Gesamt"])

        for energy_source in energy_sources:

            logging.getLogger().info(f"Energy source: {energy_source}")

            # Create a searchable name
            name = "_".join(
                [
                    aggregate_cleaned,
                    energy_source,
                    str(years[0]),
                    str(years[-1]),
                ]
            )

            # Multi row index
            if file == "eev":

                # Change str to list with string element
                if not isinstance(aggregate, list):
                    aggregate = [aggregate]

                # Use the aggregate as the row index
                row_midx_addon = 5 - len(aggregate)

                # Extend the  with "Gesamt" if not specified
                aggregate.extend(["Gesamt"] * row_midx_addon)

                # Slice data for all given provinces and years
                df = data.loc[
                    IDX[tuple(aggregate)],
                    IDX[tuple(provinces), energy_source, years],
                ]

                df = apply_single_index(df=df)

            else:

                # Slice data for all given provinces and years
                df = data.loc[
                    IDX[tuple(aggregate)],
                    IDX[tuple(provinces), energy_source, years],
                ]

            # Sum column and row
            df = add_sums(df=df)

            # Share of each year over total years per province
            df_shares_per_year = get_shares(df=df, years=True)

            # Share of each province over total provinces per year
            df_shares_per_province = get_shares(df=df, provinces=True)

            logging.getLogger().info(
                f"Added {name} to {self.name}.data_manager")

            # Create Data object
            self.data.append(
                Data(
                    # title=name,
                    name=name,
                    file="eb",
                    source="Energiebilanzen Bundesländer",
                    unit="TJ",
                    frame=df,
                    aggregate=aggregate[0],
                    energy_source=energy_source,
                    shares_over_rows=df_shares_per_year,
                    shares_over_columns=df_shares_per_province,
                    provinces=provinces,
                    years=years,
                    order="per_years"
                )
            )

            return

    def add_eb_data_per_sector(
        self,
        file: Union[str, Path],
        aggregate: List,
        provinces: List,
        years: List,
        energy_sources: List = None,
        sectors: List = None,
    ):
        logging.getLogger().error("/" * 80)
        logging.getLogger().info(
            f"Adding {file} data per sector:\n{sectors}\n")

        # Fetch data
        data = pickle.load(open(self.file_paths[file], "rb"))

        for year in years:

            logging.getLogger().info(f"Year: {year}")

            for energy_source in energy_sources:

                # Helper structure
                df = pd.DataFrame(index=sectors, columns=provinces)

                # Extend with energy source
                name = "_".join([aggregate,
                                 energy_source,
                                 str(year),
                                 ])

                for sector in sectors:

                    # Slice data for all given provinces and years
                    s = data.loc[
                        IDX[sector], IDX[tuple(
                            provinces), energy_source, year],
                    ]

                    df.loc[sector, provinces] = s.droplevel(
                        (1, 2), axis=0).T

                # dfs.append(df)
                df = add_sums(df=df)

                # Share of each province over total provinces per year
                df_shares_per_province = get_shares(
                    df=df, provinces=True)

                logging.getLogger().info(
                    f"Added {name} to {self.name}.data_manager")

                # Create a Data object
                self.data.append(
                    Data(
                        name=name,
                        file="sec",
                        source="Energiebilanzen Bundesländer, Verbrauch nach Sektoren",
                        unit="TJ",
                        frame=df,
                        aggregate=aggregate,
                        energy_source=energy_source,
                        shares_over_columns=df_shares_per_province,
                        provinces=provinces,
                        years=years,
                        sectors=sectors,
                        order="per_sector"
                    )
                )

    def add_stats_data_per_years(
        self,
        file: Union[str, Path],
        provinces: List,
        years: List,
        name: str,
    ):
        logging.getLogger().error("/" * 80)

        data = pickle.load(open(self.file_paths[file], "rb"))

        if file == "pop":

            # Unit
            unit = "Person"
            aggregate = name
            name = "_".join(
                [aggregate, str(data["df"].index[0]), str(data["df"].index[-1])])

        if file == "km_pkw":

            # Unit
            unit = "km"
            aggregate = name
            name = "_".join(
                [aggregate, str(data["df"].index[0]), str(data["df"].index[-1])])

        # Slice pickled dataframe
        df = pd.DataFrame(index=years, columns=provinces)

        logging.getLogger().info(
            f"Adding {file} data per years:\n{df.index}\n")

        # _df = data["df"].loc[years, provinces]

        for index, row in df.iterrows():
            try:
                df.loc[index, :] = data["df"].loc[index, provinces]
            except:
                pass

        # Compute sums on rows axis (years) and on col axis (provinces)
        df = add_sums(df=df)

        # Create shares
        # Share of each year over total years per province
        df_shares_per_year = get_shares(df=df, years=True)
        # print("pop_shares_years: ", df_shares_per_year)

        # Share of each province over total provinces per year
        df_shares_per_province = get_shares(df=df, provinces=True)
        # print("pop_shares_provinces: ", df_shares_per_province)

        logging.getLogger().info(
            f"Added {name} to {self.name}.data_manager")

        # Create a Data object
        self.data.append(
            Data(
                name=name,
                source=df.index.name,
                aggregate=aggregate,
                frame=df,
                shares_over_rows=df_shares_per_year,
                shares_over_columns=df_shares_per_province,
                unit=unit,
                file=file,
                provinces=provinces,
                years=years,
                order="per_years"
            )
        )
        return

    def add_overlay(
        self, chart_type: str, to_data: List = None, overlays: List = None, scalings: List = ["absolute"]
    ):

        assert overlays != [], "No data for overlay"
        assert to_data != [], "No dataset to write overlay to."

        # If only one scale arg, use this one for all overlay series
        if not isinstance(scalings, list):
            scalings = [scalings]
            if len(scalings) != len(overlays):
                scalings = [scalings[0] for x in range(len(scalings))]

        # Iter over datasets and add overlay
        for overlay, scale in zip(overlays, scalings):

            for data in to_data:

                data.overlays.append(
                    {"data": overlay, "scale": scale}
                )

                logging.getLogger().info(
                    f"Added {overlay.name} to {data.name} as overlay.")

                data.has_overlay = True

        return

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
            df_numerator), "Dataframe index length mismatch!"

        df = df_numerator/df_denominator

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
            f"Added KPI with {name} with unit {unit} to {self.name}.data_manager as KPI")

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
                order="per_years"
            )
        )
        return

    # def compute_KPI():
    #     return

    # if provinces:

    #     for col in df_shares.columns:

    #         # NOTE: Cumbersome, but the sum gets computed as 1

    #         # Province value as a share of "AT"
    #         if "AT" in df_shares.columns:
    #             AT = df_shares[col].iloc[:-2].sum(axis=0) / df_shares.loc["AT", col]

    #         # Province share with respect to selected provinces
    #         df_shares[col] = df_shares[col] / df_shares[col].iloc[:-2].sum(axis=0)

    #         if "AT" in df_shares.columns:
    #             df_shares.loc["AT", col] = AT

    #         return df_shares

    # if file == "pop":

    #     # Fetch data
    #     data = pickle.load(open(self.file_paths["pop"], "rb"))

    #     df = data["df"].loc[years, provinces]

    #     # Compute sums on rows axis (years) and on col axis (provinces)
    #     df = add_sums(df=df)
    #     # df = df.T
    #     print("df: ", df)

    # df_shares = deepcopy(df)
    # df_row_perc = deepcopy(df.T)

    # for col in df_shares.columns:
    #     df_shares = df_shares[col].value_counts(normalize=True) * 100

    # for col in df_row_perc.columns:
    #     df_shares = df_shares[col].value_counts(normalize=True) * 100

    # print("df_shares: ", df_shares)

    # self.data["Bevölkerung"] = Data(
    #     values=df,
    #     percentage_cols=df_shares,
    #     percentage_rows=df_row_perc,
    #     unit=df.iloc[1, -1],
    #     file=data["df"].iloc[0, 0],
    #     provinces=provinces,
    #     years=years,
    # )

    # if file == "brp":

    #     # Fetch data
    #     data = pickle.load(open(self.file_paths["brp"], "rb"))

    # if years[0] < data["df"].index[0]:
    #     idx = years.index(data["df"].index[0])
    #     years = years[idx:]
    # if years[-1] > data["df"].index[-1]:
    #     idx = years.index(data["df"].index[-1])
    #     years = years[:idx]

    # df = data["df"].loc[years, provinces]
    # # df = data["df"].iloc[:10, :]
    # df_shares = deepcopy(df)

    # for col in df_shares.columns:
    #     df_shares[col].value_counts(normalize=True) * 100

    # self.kpi["BRP"] = Data(
    #     values=df,
    #     unit="Millionen Euro",
    #     file=data["df"].iloc[0, 0],
    #     provinces=provinces,
    #     years=years,
    # )

        # Select first year
        # years_start = max(data["df"].index[0], years[0])
        # # Select last year
        # years_end = min(data["df"].index[-1], years[-1])
        # years = tuple(range(years_start, years_end + 1, 1))
        # print("years: ", years)
        # return

        # else:
        #     # Iter over energy sources
        #     for energy_source in energy_sources:
        #         print("energy_source: ", energy_source)

        #         # Extend with energy source
        #         title = " - ".join([title, energy_source])

        #         # Slice data for all given provinces and years
        #         df = data.loc[
        #             IDX[tuple(aggregate)],
        #             IDX[tuple(provinces), energy_source, years],
        #         ]

        #         df = apply_single_index(df=df)
        #         # print("df: ", df)

        #         # Compute sums on rows axis (years) and on col axis (provinces)
        #         df = add_sums(df=df)

        #         # Create shares
        #         # Share of each year over total years per province
        #         df_shares_per_year = get_shares(df=df, years=True)
        #         # print("df_shares_years: ", df_shares_per_year)

        #         # Share of each province over total provinces per year
        #         df_shares_per_province = get_shares(df=df, provinces=True)
        #         # print("df_shares_provinces: ", df_shares_per_province)

        #         # Prepare data storage structure
        #         try:
        #             storage = self.data[file][aggregate[0]]
        #             # storage[aggregate] = {}
        #             # storage[aggregate][energy_source]
        #         except:
        #             storage = self.data[file]
        #             storage[aggregate[0]] = {}

        #         # Create a Data object
        #         storage[energy_source] = Data(
        #             title=title,
        #             values=df,
        #             aggregate=aggregate[0],
        #             energy_source=energy_source,
        #             shares_over_rows=df_shares_per_year,
        #             shares_over_columns=df_shares_per_province,
        #             unit=unit,
        #             file=file,
        #             provinces=provinces,
        #             years=years,
        #         )
        #     return

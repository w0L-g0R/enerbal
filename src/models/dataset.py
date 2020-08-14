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

from settings import file_paths, provinces_hex, provinces, conversion_multiplicators

from models.utils import (add_sums,
                          add_means,
                          get_shares,
                          apply_single_index,
                          convert)

from models.data import Data, FilterData
from files.energiebilanzen.convert.get_eb_data_structures import (
    eev_aggregates,
    sectors_aggregates,
    sector_energy,
)

IDX = pd.IndexSlice

EnergySourceAggregate = NewType("EnergySourceAggregate", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)


def get_eb_data_by_aggregate(aggregate: str):
    '''
    Takes an aggregate and gives back the data from the according pickle file.
    Used to differentiate "eev", "sectors_consumption" and "sector_energy_consumption" data (dfs with different indices).
    '''

    if aggregate in eev_aggregates:

        data = pickle.load(open(self.file_paths["eev"], "rb"))

    elif aggregate in sectors_aggregates:

        data = pickle.load(open(self.file_paths["sec"], "rb"))

    elif aggregate in sector_energy:

        data = pickle.load(open(self.file_paths["sec_nrg"], "rb"))

    return data

    # Create a searchable name
    # name = "_".join(
    #     [
    #         aggregate,
    #         energy_source,
    #         str(years[0]),
    #         str(years[-1]),
    #     ]
    # )


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

    def add_eb_data(
        self,
        provinces: List,
        years: List,
        balance_aggregates: List,
        energy_sources: List = None,
        conversion: str = None,
    ):
        logging.getLogger().error("/" * 80)
        logging.getLogger().info(f"Adding {file} data per years:\n{years}\n")

        # Fetch data
        data = get_eb_data
        unit = "TJ"
        # data_type = None

        data = get_eb_data_by_aggregate

        logging.getLogger().info(f"Energy source: {energy_source}")

        # Change str to list with string element
        if not isinstance(aggregate, (list, tuple)):
            aggregate = [aggregate]

        # Aggregate name without "Gesamt"
        aggregate = "_".join(
            [x for x in aggregate if x != "Gesamt"])

        # Extend eev data index -> multi index
        row_midx_addon = 5 - len(aggregate)

        # Extend the  with "Gesamt" if not specified
        aggregate.extend(["Gesamt"] * row_midx_addon)

        # Slice data for all given provinces and years
        df = data.loc[
            IDX[tuple(aggregate)],
            IDX[tuple(provinces), energy_source, years],
        ]

        # _______________________________________ EEV ONLY
        df = apply_single_index(df=df)

        # else:

        #     # Slice data for all given provinces and years
        #     df = data.loc[
        #         IDX[tuple(aggregate)],
        #         IDX[tuple(provinces), energy_source, years],
        #     ]

        # Sum column and row
        df = add_sums(df=df)

        # If all sum of sum column == 0, than all values are # NaN
        if df["Sum"].sum() != 0:

            if conversion is not None:
                df, unit = convert(df=df, conversion=conversion)

            # Share of each year over total years per province
            # df_shares_per_year = get_shares(df=df, years=True)

            # Share of each province over total provinces per year
            df_shares_per_province = get_shares(
                df=df, provinces=True)

        else:
            # Write NaN df to shares
            df_shares_per_province = df

        df_shares_per_year = df

        # # Transform data values to new unit scale
        # df, unit = convert(df=df, conversion=conversion)

        # # Share of each year over total years per province
        # df_shares_per_year = get_shares(df=df, years=True)

        # # Share of each province over total provinces per year
        # df_shares_per_province = get_shares(df=df, provinces=True)

        logging.getLogger().info(
            f"Added {name} to {self.name}.data_manager")

        # Create Data object
        self.data.append(
            Data(
                # title=name,
                name=name,
                file="eb",
                source="Energiebilanzen Bundesländer",
                unit=unit,
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
        conversion: Optional[str] = None,
        energy_sources: Optional[List] = None,
        sectors: Optional[List] = None,
    ):
        logging.getLogger().error("/" * 80)
        logging.getLogger().info(
            f"Adding {file} data per sector:\n{sectors}\n")

        # Fetch data
        data = pickle.load(open(self.file_paths[file], "rb"))
        unit = "TJ"

        for year in years:

            logging.getLogger().info(f"Year: {year}")

            for energy_source in energy_sources:

                # Output df which holds sector series
                df = pd.DataFrame(index=sectors, columns=provinces)

                # Iter over sectors (= actually list of aggregates)
                for sector in sectors:

                    # Extend with energy source
                    name = "_".join([sector,
                                     energy_source,
                                     str(year),
                                     ])

                    # Slice data for all given provinces and years
                    s = data.loc[
                        IDX[sector], IDX[tuple(
                            provinces), energy_source, year],
                    ]

                    # Copy series to output df
                    df.loc[sector, provinces] = s.droplevel(
                        (1, 2), axis=0).T

                # Add sum row and column
                df = add_sums(df=df)

                # If all sum of sum column == 0, than all values are NaN
                if df["Sum"].sum() != 0:

                    if conversion is not None:
                        df, unit = convert(df=df, conversion=conversion)

                    # Share of each province over total provinces per year
                    df_shares_per_province = get_shares(
                        df=df, provinces=True)
                else:
                    # Write NaN df to shares
                    df_shares_per_province = df

                logging.getLogger().info(
                    f"Added {name} to {self.name}.data_manager")

                # Create a Data object
                self.data.append(
                    Data(
                        name=name,
                        file="sec",
                        source="Energiebilanzen Bundesländer, EEV nach Sektoren",
                        unit=unit,
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
            except BaseException:
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

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

from enspect.settings import (
    file_paths,
    provinces_hex,
    provinces,
    unit,
)

from enspect.models.utils import (
    add_sums,
    add_means,
    get_shares,
    apply_single_index,
    convert,
    drop_eb_row_levels,
    post_process,
)

from enspect.models.data import Data, FilterData
from enspect.conversion.energiebilanzen.data_structures import (
    eev_aggregates,
    sectors,
    sector_energy,
)

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

    def add_eb_data(
        self,
        provinces: List,
        years: List,
        columns: Union[List, str],
        rows: Union[List, str],
        conversion: str = None,
        balance_aggregates: List = None,
        energy_sources: List = None,
        energy_sources_aggregates: List = None,
        sort_column_by: str = None,
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
        print("df: ", df.head())

        if rows == "balance_aggregates" and columns == "energy_sources":

            group = df.groupby(level=["ET"], axis=1).filter(
                lambda x: x.columns.get_level_values(1).unique() in energy_sources
            )

            group = group.groupby(level=["IDX_0"], axis=0).filter(
                lambda x: x.index.unique() in balance_aggregates
            )

            for year in years:

                data = group.groupby(level=["YEAR"], axis=1).get_group(year)

                if sort_column_by == "province":
                    data = data.swaplevel(0, 1, axis=1).sort_index(axis=1, level=0)

                data.loc["Column_Total"] = data.sum(numeric_only=True, axis=0)

                if len(energy_sources) == 1:
                    data.loc[:, "Row_Total"] = data.sum(
                        numeric_only=True, axis=1
                    ).subtract(data[data.columns[0]])

                data *= unit[conversion]
                data = round(data, 2)

                print("data: ", data)

        if rows == "balance_aggregates" and columns == "energy_sources":

            group = df.groupby(level=["ET"], axis=1).filter(
                lambda x: x.columns.get_level_values(1).unique() in energy_sources
            )

            group = group.groupby(level=["IDX_0"], axis=0).filter(
                lambda x: x.index.unique() in balance_aggregates
            )

            for year in years:

                data = group.groupby(level=["YEAR"], axis=1).get_group(year)

                shares_over_rows = (
                    data.groupby(level="BL", axis=1)
                    .apply(lambda x: 100 * x / float(x.sum()))
                    .round(2)
                )

                shares_over_cols = (
                    data.groupby(level=0, axis=0)
                    .apply(lambda x: 100 * x / float(x.iloc[:, 1:].sum(axis=1)))
                    .round(2)
                )

                if sort_column_by == "province":
                    data = data.swaplevel(0, 1, axis=1).sort_index(axis=1, level=0)

                data.loc["Column_Total"] = data.sum(numeric_only=True, axis=0)

                if len(energy_sources) == 1:
                    data.loc[:, "Row_Total"] = data.sum(
                        numeric_only=True, axis=1
                    ).subtract(data[data.columns[0]])

                data *= unit[conversion]
                data = round(data, 2)
                print("data: ", data)

                print("shares_over_rows: ", shares_over_rows)
                print("shares_over_cols: ", shares_over_cols)
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
        logging.getLogger().info(f"Adding {file} data per sector:\n{sectors}\n")

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
                    name = "_".join([sector, energy_source, str(year),])

                    # Slice data for all given provinces and years
                    s = data.loc[
                        IDX[sector], IDX[tuple(provinces), energy_source, year],
                    ]

                    # Copy series to output df
                    df.loc[sector, provinces] = s.droplevel((1, 2), axis=0).T

                # Add sum row and column
                df = add_sums(df=df)

                # If all sum of sum column == 0, than all values are NaN
                if df["Sum"].sum() != 0:

                    if conversion is not None:
                        df, unit = convert(df=df, conversion=conversion)

                    # Share of each province over total provinces per year
                    df_shares_per_province = get_shares(df=df, provinces=True)
                else:
                    # Write NaN df to shares
                    df_shares_per_province = df

                logging.getLogger().info(f"Added {name} to {self.name}.data_manager")

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
                        order="per_sector",
                    )
                )

    def add_stats_data_per_years(
        self, file: Union[str, Path], provinces: List, years: List, name: str,
    ):
        logging.getLogger().error("/" * 80)

        data = pickle.load(open(self.file_paths[file], "rb"))

        if file == "pop":

            # Unit
            unit = "Person"
            aggregate = name
            name = "_".join(
                [aggregate, str(data["df"].index[0]), str(data["df"].index[-1])]
            )

        if file == "km_pkw":

            # Unit
            unit = "km"
            aggregate = name
            name = "_".join(
                [aggregate, str(data["df"].index[0]), str(data["df"].index[-1])]
            )

        # Slice pickled dataframe
        df = pd.DataFrame(index=years, columns=provinces)

        logging.getLogger().info(f"Adding {file} data per years:\n{df.index}\n")

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

        logging.getLogger().info(f"Added {name} to {self.name}.data_manager")

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
                order="per_years",
            )
        )
        return

    def add_overlay(
        self,
        chart_type: str,
        to_data: List = None,
        overlays: List = None,
        scalings: List = ["absolute"],
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

                data.overlays.append({"data": overlay, "scale": scale})

                logging.getLogger().info(
                    f"Added {overlay.name} to {data.name} as overlay."
                )

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

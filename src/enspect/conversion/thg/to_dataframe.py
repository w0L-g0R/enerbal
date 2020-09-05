import pickle
from pathlib import Path

import pandas as pd
from enspect.paths import file_paths
from enspect.utils import timeit

from enspect.conversion.thg.utils import fetch_from_xlsx
from enspect.aggregates.common import provinces

from pandas import IndexSlice as IDX


@timeit
def convert_thg_to_dataframe():

    files = (
        file_paths["files_thg"] / "THG_1990_2006.xlsx",
        file_paths["files_thg"] / "THG_2000_2017.xlsx",
        file_paths["files_thg"] / "THG_ETS_2005_2017.xlsx",
    )
    # Main frame
    y_0 = [x for x in range(1990, 2018)]

    # THG_1990_2006
    y_1 = [x for x in range(1990, 2007)]

    # THG_2000_2017
    y_2 = [1990, 1995]
    y_2.extend([x for x in range(2000, 2017 + 1)])

    # THG_ETS_2005_2017
    y_3 = [x for x in range(2005, 2018)]

    emittent_sources = ["TOTAL", "ETS", "NON_ETS"]

    df = pd.DataFrame(
        index=[
            "Energieversorgung",
            "Energie",
            "Kleinverbrauch",
            "Industrie",
            "Verkehr",
            "Landwirtschaft",
            "Sonstige",
            "Gebäude",
            "Abfallwirtschaft",
            "Fluorierte Gase",
            "Gesamt",
        ],
        columns=pd.MultiIndex.from_product(
            [provinces, emittent_sources, y_0], names=["PROV", "ES", "YEAR"],
        ),
    )

    for file, years in zip(files, [y_1, y_2]):

        data = fetch_from_xlsx(file=file)
        dfs = []

        for province, data in data.items():

            df.loc[IDX[data.index], IDX[province, "TOTAL", data.columns]] = data.values

    # Fill missing values in col "Energie" with values from "Energieversorgung"
    energie_row_updated = df.loc[IDX["Energie"], IDX[:, "TOTAL", :]].fillna(
        df.loc[IDX["Energieversorgung"], IDX[:, "TOTAL", :]]
    )
    # Update
    df.loc[IDX["Energie"], IDX[:, "TOTAL", :]] = energie_row_updated

    # Delete Energieversorgung
    df.drop("Energieversorgung", inplace=True)

    # Compute AT values
    df.loc[IDX[:], IDX["AT", "TOTAL", :]] = (
        df.groupby(level="YEAR", axis=1).sum().values
    )

    ets_data = fetch_from_xlsx(file=files[-1])

    for source, data in ets_data.items():
        print("source: ", source)
        data.index = provinces
        data.index.name = "PROV"
        data = (
            data.T.unstack()
        )  # .sort_values()  # .swaplevel(axis=0)  # .sort_values()
        # data = data.T.sort_index().stack().swaplevel().sort_values()

        # Update index
        data.index = df.loc[IDX[source], IDX[:, "ETS", y_3]].index

        # Write ETS data to main frame
        df.loc[IDX[source], IDX[:, "ETS", y_3]] = data.values

        # Compute Non-ETS values
        total = df.loc[IDX[source], IDX[:, "TOTAL", y_3]].fillna(0).copy().astype(int)

        # Assign Non-ETS values
        df.loc[IDX[source], IDX[:, "NON_ETS", y_3]] = total.values - data.values
        print("df: ", df)

    df.index.name = "BAGG_0"

    with open(file_paths["db_pickles"] / "thg.p", "wb") as file:
        pickle.dump(df, file)

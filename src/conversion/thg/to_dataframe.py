from paths import file_paths
from utils import timeit
from conversion.thg.utils import fetch_from_xlsx
from pathlib import Path
import pandas as pd
import pickle

IDX = pd.IndexSlice


@timeit
def convert_thg_to_dataframe():
    """
    Make sure energy balance files follow the name convention: prefix "EB" + provinces_name + year_start(last two digits only) + year_end(last two digits only) , connected with underlines, eg. EB_Bgd_88_18

    row index = [SRC, CLS]
    col index = [BL, YEAR]

    """
    provinces = [
        "Bgd",
        "Ktn",
        "Noe",
        "Ooe",
        "Sbg",
        "Stk",
        "Tir",
        "Vbg",
        "Wie",
        "AT",
    ]

    file = Path.cwd() / "conversion/thg/files/THG_1990_2017.xlsx"

    thg_sheets = fetch_from_xlsx(file=file)

    thg_sources = thg_sheets["AT_THG_TOTAL"].iloc[0, :-1].unique()
    print("thg_sources: ", thg_sources)

    years = thg_sheets["AT_THG_TOTAL"].index[1:]

    midx = pd.MultiIndex.from_product(
        [provinces, thg_sources, ["TOTAL", "ETS", "NON_ETS"]],
        names=["BL", "SRC", "CLS"],
    )
    # print("midx: ", midx)

    thg_df = pd.DataFrame(index=years, columns=midx)
    thg_df.index.name = "YEAR"

    # Copy total thg values
    df = thg_sheets["AT_THG_TOTAL"]

    # Drop sources row
    df.drop([""], axis=0, inplace=True)

    # Add two-level midx
    df.columns = pd.MultiIndex.from_product(
        [provinces[:-1], thg_sources], names=["BL", "SRC"],
    )

    # Add THG total values
    for province in provinces[:-1]:

        for source in thg_sources:

            thg_df.loc[IDX[:], IDX[province, source, "TOTAL"]] = df.loc[
                IDX[:], IDX[province, source]
            ]

    # Add ETS Energy and ETS Industry data
    for df, source in zip(
        [thg_sheets["AT_THG_ETS_ENERGY"], thg_sheets["AT_THG_ETS_INDUSTRY"], ],
        ["Energie", "Industrie"],
    ):
        for province in provinces[:-1]:

            thg_df.loc[IDX[df.index], IDX[province, source, "ETS"]] = df.loc[
                :, province
            ]

            thg_df.loc[IDX[:], IDX[province, source, "NON_ETS"]] = thg_df.loc[
                IDX[:], IDX[province, source, "TOTAL"]
            ].subtract(thg_df.loc[IDX[:], IDX[province, source, "ETS"]])

    thg_df.grouby("")

    # Rearrange column and row indices (new row idx == SECTOR)
    thg_df = thg_df.unstack(level="YEAR")

    # New Column_midx
    thg_df = thg_df.unstack(level=["BL", "YEAR"])

    print("thg_df: ", thg_df)

    pickle.dump(thg_df, open(file_paths["db_pickles"] / "thg.p", "wb"))

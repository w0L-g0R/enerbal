# %%
import pickle
from enspect.paths import file_paths
from pandas import IndexSlice as IDX
import pandas as pd
import itertools

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", 40)  # or 1000
pd.set_option("display.min_rows", 40)  # or 1000
pd.set_option("display.width", None)  # or 1000
pd.set_option("max_colwidth", 15)  # or 1000
# pd.set_option("display.multi_sparse", True)  # or 1000
# pd.set_option("display.column_space", 5)  # or 1000
# pd.set_option("display.colheader_justify", "left")  # or 1000
# pd.set_option("display.precision", 2)  # or 1000


# ////////////////////////////////////////////////////////////////////////// EB
# Midx after slicing => rows: BAGGS; columns: PROV, YEAR, ES
df = pickle.load(open(file_paths["db_pickles"] / "eb.p", "rb"))


balance_aggregates = [
    # [
    #     "Umwandlungsausstoß",
    #     # "Umwandlungseinsatz",
    #     "Heizwerke",
    #     "davon: EVU",
    #     "aus Biogenen",
    #     "Gesamt",
    #     # "Gesamt",
    # ],
    [
        "Umwandlungsausstoß",
        # "Umwandlungseinsatz",
        "Kraftwerke",
        "davon: UEA",
        # "aus Biogenen",
        # "Gesamt",
        # "Gesamt",
    ],
    # ["Umwandlungseinsatz", "Kraftwerke", "davon: EVU"],
]

# In case all baggs elements only contain less than the max nr of levels..
# dummy = ["Gesamt", "Gesamt", "Gesamt", "Gesamt", "Gesamt"]

# .. add this dummy, wich gets used as ref to fill missing index values ..
# balance_aggregates.insert(0, dummy)

balance_aggregates = [
    "_".join(val).rstrip("_").split("_Gesamt")[0]
    for val in balance_aggregates
    if val != "Gesamt"
]

# balance_aggregates = tuple(

#     itertools.zip_longest(*balance_aggregates, fillvalue="Gesamt")
# )

index = [
    "_".join(val).rstrip("_").split("_Gesamt")[0]
    for val in df.index.values
    if val != "Gesamt"
]


df.index = index

balance_aggregates
print("balance_aggregates: ", balance_aggregates)

energy_sources = "KOHLE"
years = [2010]
df = df.loc[IDX[balance_aggregates], IDX[:, energy_sources, years]]
# df = df.loc[
#     # slice("Umwandlungseinsatz", "Kraftwerke", "davon: EVU"),
#     IDX[
#         ("Umwandlungsausstoß", "Umwandlungseinsatz",),
#         (("Kraftwerke"), ("Heizwerke")),
#         ("davon: EVU", "davon: UEA"),
#     ],
#     IDX["AT", energy_sources, years],
# ]
# str(df)
df

# %%

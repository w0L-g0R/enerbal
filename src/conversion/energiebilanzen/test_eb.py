# %%

import pandas as pd
from pathlib import Path
from typing import Union, List

import numpy as np
import pickle

pd.set_option("display.max_columns", 10)  # or 1000
pd.set_option("display.max_rows", None)  # or 1000
pd.set_option("display.width", None)  # or 1000

IDX = pd.IndexSlice

# sheets = pickle.load(
#     open("D:/_WORK/AEA/Projekte/bilanzen_monitor/src/sheets_ktn.p", "rb")
# )
# %%
path_eb_df = Path.cwd() / "database/pickles/eb.p"

eb_df = pickle.load(
    open(
        path_eb_df,
        "rb",
    )
)
# eb_df.index.name = "ET"
eb_df.head()

fossil_fest = [
    "aus Steinkohle",
    "aus Braunkohle",
    "aus Brennbare Abfälle",
]

fossil_flüssig = [
    "aus Öl"
]

fossil_gas = [
    "aus Erdgas",
    "aus Kohlegase",
]


bio_fest = [
    "aus Scheitholz",
    "aus Holzpellets",
    "aus Hausmüll - Bioanteil",
    "aus Holzabfall",
    "aus Ablauge",
    "aus sonst. festen Biogenen",
]

bio_flüssig = [
    "aus flüssigen Biogenen"
]

bio_gas = [
    "aus Deponiegas",
    "aus Klärgas",
    "aus Biogas",
]

res = ["aus Wasserkraft",
       "aus Wind,PV, Geothermie"
       ]

aggs = [fossil_fest,
        fossil_flüssig,
        fossil_gas,
        # bio_fest,
        # bio_flüssig,
        # bio_gas,
        res
        ]

agg_names = [
    "UA_fossil_fest",
    "UA_fossil_flüssig",
    "UA_fossil_gas",
    # "UA_bio_fest",
    # "UA_bio_flüssig",
    # "UA_bio_gas",
    "UA_res",
]


imp_sources = [
    "Steinkohle",
    "Braunkohle",
    "Brennbare Abfälle",
    "Sonst. Biogene fest",
    "ÖL",
    "Erdgas",
    "Kohlegase",
    "Scheitholz",
    "Holzpellets",
    "Hausmüll Bioanteil",
    "Holzabfall",
    "Ablauge",
    "Sonst. Biogene flüssig",
    "Deponiegas",
    "Klärgas",
    "Biogas",
    "Wasserkraft",
    "Wind",
    "Photovoltaik",
]

df = eb_df.loc[
    IDX["Importe", :, :, :, :],
    IDX[:, "Elektrische Energie", 2018],
]

with pd.ExcelWriter("Importe_Elektrisch" + '.xlsx') as writer:
    df.to_excel(writer)


# e_sources = fossil_fest + fossil_flüssig + \
#     fossil_gas + bio_fest + bio_flüssig + bio_gas + res

# print('e_source: ', e_source)

# fossil_fest
# print('fossil_fest: ', fossil_fest)

# for agg, name in zip(aggs, agg_names):
#     print('agg: ', agg)
#     print('name: ', name)

#     df = eb_df.loc[
#         IDX["Umwandlungsausstoß", :, :, agg, :], IDX[:,
#                                                      "Elektrische Energie", 2018],
#     ]

#     with pd.ExcelWriter(name + '.xlsx') as writer:
#         df.to_excel(writer)


# with pd.ExcelWriter("UA_bio_flüssig" + '.xlsx') as writer:
#     df.to_excel(writer)

# df = eb_df.loc[
#     IDX["Umwandlungsausstoß", :, :, "aus Biogenen", bio_gas], IDX[:,
#                                                                   "Elektrische Energie", 2018],
# ]

# with pd.ExcelWriter("UA_bio_gas" + '.xlsx') as writer:
#     df.to_excel(writer)

# df = eb_df.loc[
#     IDX["Umwandlungsausstoß", :, :, "aus Biogenen", bio_fest], IDX[:,
#                                                                    "Elektrische Energie", 2018],
# ]

# with pd.ExcelWriter("UA_bio_fest" + '.xlsx') as writer:
#     df.to_excel(writer)


# IDX rows = ENERGY SOURCE
# IDX columns PROV, AGGREGATE, USAGE CAT, YEARS
# s = eb_df.loc[
#     IDX["Binnenschiffahrt", "Papier und Druck"],
#     IDX["Ktn", "Steinkohle", "Dampferzeugung", 2000],
# ]
# s
# %%
# eb_df = eb_df.unstack(level="ET")  # .stack("BL")
# eb_df = eb_df.unstack(level=["BL", "ET", "USAGE", "YEAR"])  # .stack("BL")
# # eb_df = eb_df.unstack(level="USAGE")  # .stack("BL")
# # eb_df = eb_df.unstack(level="USAGE")  # .stack("BL")
# # eb_df = eb_df.stack("BL")  # .stack("BL")

# # eb_df.unstack("SECTOR")#.stack("SECTOR")
# eb_df.head()

# %%

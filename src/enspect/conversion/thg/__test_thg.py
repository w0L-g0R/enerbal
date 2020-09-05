# # %%
# import pandas as pd
# from pathlib import Path
# from typing import Union, List

# import numpy as np
# import pickle

# from enspect.settings import provinces
# from enspect.paths import file_paths
# # from IPython.display import display


# pd.set_option("display.max_columns", 50)  # or 1000
# pd.set_option("display.max_rows", None)  # or 1000
# pd.set_option("display.width", None)  # or 1000

# from pandas import IndexSlice as IDX

# # %%


# thg_df = pickle.load(
#     open(
#         file_paths["db_pickles"] / "thg.p",
#         "rb",
#     )
# )
# # # nea_df.index.name = "ES"
# # thg_df.head()
# # IDX rows = ENERGY SOURCE
# # IDX columns PROV, AGGREGATE, USAGE CAT, YEARS
# sources = thg_df.index.get_level_values(0).unique()
# print('sources: ', sources)

# # for province in provinces[:-1]:
# #     s = thg_df.loc[
# #         IDX["Energie"],
# #         IDX[province, :]
# #     ]
# #    display(s)

# for source in sources:
#     s = thg_df.loc[
#         IDX[:, "TOTAL"],
#         IDX[:, :]
#     ]

# s = thg_df.T.groupby(["YEAR"]).sum()
# # s = s.T.groupby("PROV")
# print("\n")
# # print("/" * 79)
# # print("\n")
# # display(s)

# # s

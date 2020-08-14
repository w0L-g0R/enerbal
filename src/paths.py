from pathlib import Path

CWD = Path.cwd()

file_paths = {

    "eb_indices_pickled": CWD / Path(
        "files/energiebilanzen/pickles/indices.p"
    ),

    "eb_midx_xlsx": CWD / Path(
        "files/energiebilanzen/indices/midx_.xlsx"
    ),

    "eb_xlsx_dir": CWD / Path(
        "files/energiebilanzen/xlsx"
    ),
    # "eev": CWD / Path(
    #     "files/energiebilanzen/pickles/eev_df.p"
    # ),
    # "sec": CWD / Path(
    #     "files/energiebilanzen/pickles/sectors_df.p"
    # ),
    # "sec_nrg": CWD / Path(
    #     "files/energiebilanzen/pickles/sectors_energy_df.p"
    ),
    "nea": CWD / Path(
        "files/nea/pickles/nea_df.p"
    ),
    "nea_data_dir": CWD / Path(
        "files/nea/data"
    ),
    "pop": CWD / Path(
        "files/stats/pickles/AT_BEVÖLKERUNG.pkl"
    ),
    "brp": CWD / Path(
        "files/stats/pickles/AT_BRP_REAL.pkl"
    ),
    "km_pkw": CWD / Path(
        "files/stats/pickles/AT_PRIVATE_PKW_KM.pkl"
    ),
}

# balances_directory_path = Path.cwd() / "/files/energiebilanzen/data"
# print("balances_directory_path: ", balances_directory_path)

# row_indices_file_path = Path.cwd() / "/files/energiebilanzen/index/row_indices_eb.xlsx"
# print("row_indices_file_path: ", row_indices_file_path)

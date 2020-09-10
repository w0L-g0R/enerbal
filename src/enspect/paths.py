from pathlib import Path

# App entrypoint
CWD = Path(__file__).parent.resolve()  # / ("src/enspect")

# App routing
file_paths = {
    "folder_eb": CWD / Path("database/files/energiebilanzen"),
    "folder_nea": CWD / Path("database/files/nutzenergieanalysen"),
    "folder_thg": CWD / Path("database/files/luftschadstoffinventur"),
    "folder_area": CWD / Path("database/files/landesfläche") / "DF_AREA.xlsx",
    #
    "folder_mileage": CWD / Path("database/files/fahrleistung") / "DF_PKW_MILEAGE.xlsx",
    #
    "folder_liv_space": CWD
    / Path("database/files/wohnfläche")
    / "DF_AVG_LIV_SPACE_PRIVATE.xlsx",
    #
    "folder_population": CWD
    / Path("database/files/bevölkerungsanzahl")
    / "DF_POPULATION.xlsx",
    #
    "pickle_eb": CWD / Path("database/pickles" / Path("eb.p")),
    "pickle_res": CWD / Path("database/pickles" / Path("res.p")),
    "pickle_nea": CWD / Path("database/pickles" / Path("nea.p")),
    "pickle_thg": CWD / Path("database/pickles" / Path("thg.p")),
    "pickle_area": CWD / Path("database/pickles/stats" / Path("AT_AREA.p")),
    "pickle_mileage": CWD / Path("database/pickles/stats" / Path("AT_MILEAGE.p")),
    "pickle_pop": CWD / Path("database/pickles/stats" / Path("AT_POPULATION.p")),
    "pickle_liv_space": CWD
    / Path("database/pickles/stats" / Path("AT_WOHNFLÄCHE_AVG.p")),
    # "db_pickles": CWD / Path("database/pickles"),
    "conversion_logs": CWD / Path("conversion/logs"),
}

# balances_directory_path = Path.cwd() / "/files/energiebilanzen/data"
# print("balances_directory_path: ", balances_directory_path)

# row_indices_file_path = Path.cwd() / "/files/energiebilanzen/index/row_indices_eb.xlsx"
# print("row_indices_file_path: ", row_indices_file_path)

from pathlib import Path

# App entrypoint
CWD = Path(__file__).parent.resolve()  # / ("src/enspect")

# App routing
file_paths = {
    "files_eb": CWD / Path("database/energiebilanzen"),
    "files_nea": CWD / Path("database/nutzenergieanalysen"),
    "files_thg": CWD / Path("database/luftschadstoffinventur"),
    "db_pickles": CWD / Path("database/pickles"),
    "conversion_logs": CWD / Path("conversion/logs"),
}

# balances_directory_path = Path.cwd() / "/files/energiebilanzen/data"
# print("balances_directory_path: ", balances_directory_path)

# row_indices_file_path = Path.cwd() / "/files/energiebilanzen/index/row_indices_eb.xlsx"
# print("row_indices_file_path: ", row_indices_file_path)

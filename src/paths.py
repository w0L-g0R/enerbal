from pathlib import Path

CWD = Path.cwd()

file_paths = {
    "files_eb": CWD / Path("conversion/energiebilanzen/files"),
    "files_nea": CWD / Path("conversion/nea/files"),
    "files_thg": CWD / Path("conversion/thg/files"),
    "db_pickles": CWD / Path("database/pickles"),
}

# balances_directory_path = Path.cwd() / "/files/energiebilanzen/data"
# print("balances_directory_path: ", balances_directory_path)

# row_indices_file_path = Path.cwd() / "/files/energiebilanzen/index/row_indices_eb.xlsx"
# print("row_indices_file_path: ", row_indices_file_path)

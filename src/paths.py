from pathlib import Path

file_paths = {
    "eb_indices": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/energiebilanzen/pickles/indices.p"
    ),
    "eb_row_indices": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/energiebilanzen/index/row_indices_eb.xlsx"
    ),
    "eb_data_dir": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/energiebilanzen/data"
    ),
    "eev": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/energiebilanzen/pickles/eev_df.p"
    ),
    "sec": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/energiebilanzen/pickles/sector_consumptions_df.p"
    ),
    "pop": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/stats/pickles/AT_BEVÖLKERUNG.pkl"
    ),
    "brp": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/stats/pickles/AT_BRP_REAL.pkl"
    ),
    "km_pkw": Path(
        "D:/_WORK/AEA/Projekte/bilanzen_monitor/enerbal/src/files/stats/pickles/AT_PRIVATE_PKW_KM.pkl"
    ),
}

balances_directory_path = Path.cwd() / "/files/energiebilanzen/data"
print("balances_directory_path: ", balances_directory_path)

row_indices_file_path = Path.cwd() / "/files/energiebilanzen/index/row_indices_eb.xlsx"
print("row_indices_file_path: ", row_indices_file_path)

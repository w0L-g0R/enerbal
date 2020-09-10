from enspect.paths import file_paths
from enspect.conversion.stats.to_dataframe import convert_stats_to_dataframe

convert_stats_to_dataframe(
    xlsx_file_path=file_paths["folder_population"],
    pickle_path=file_paths["pickle_pop"],
)

convert_stats_to_dataframe(
    xlsx_file_path=file_paths["folder_mileage"],
    pickle_path=file_paths["pickle_mileage"],
)

# from settings import file_paths

from enspect.settings import set_pd_options
from enspect.conversion.thg.to_dataframe import convert_thg_to_dataframe

setup_logging(
    console_log_actived=True,
    console_log_filter=None,
    console_out_level=logging.DEBUG,
    log_file=file_paths["conversion_logs" / "thg_conversion.log"],
)


set_pd_options()
convert_thg_to_dataframe()

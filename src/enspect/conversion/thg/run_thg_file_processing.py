# from settings import file_paths

from enspect.conversion.thg.to_dataframe import convert_thg_to_dataframe
from enspect.settings import set_pd_options

set_pd_options()
convert_thg_to_dataframe()

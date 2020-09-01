from enspect.conversion.nea.to_dataframe import convert_nea_to_dataframe
from enspect.settings import set_pd_options


set_pd_options()
convert_nea_to_dataframe(last_year=2018,)

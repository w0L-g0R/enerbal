# from settings import file_paths
from enspect.conversion.energiebilanzen.to_dataframe import (
    convert_energy_balances_to_dataframe,
)
from enspect.settings import set_pd_options

set_pd_options()
convert_energy_balances_to_dataframe(last_year=2018,)

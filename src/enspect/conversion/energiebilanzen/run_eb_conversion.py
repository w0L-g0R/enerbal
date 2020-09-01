# from settings import file_paths
from enspect.settings import set_pd_options
from enspect.conversion.energiebilanzen.to_dataframe import \
    convert_energy_balances_to_dataframe

set_pd_options()
convert_energy_balances_to_dataframe(
    last_year=2018,
)

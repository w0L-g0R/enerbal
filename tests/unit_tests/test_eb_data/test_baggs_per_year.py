import pytest
import os


# def test_add_multiple_baggs_per_year(
#     test_dataset,
#     test_workbooks_eb,
#     test_provinces,
#     test_balance_aggregates_sectors,
#     test_energy_source_elektrische_energie,
#     test_energy_source_gesamtbilanz,
#     test_launch_xlsx,
#     test_write_to_xlsx,
# ):
#     years = [2000, 2018]

#     wb = test_workbooks_eb["test_eb"]
#     ds = test_dataset

#     ds.add_eb_data(
#         energy_sources=test_energy_source_elektrische_energie
#         + test_energy_source_gesamtbilanz,
#         balance_aggregates=test_balance_aggregates_sectors,
#         years=years,
#         provinces=test_provinces,
#         per_balance_aggregate=True,
#     )

#     test_write_to_xlsx(wb=wb, ds=ds)

#     test_launch_xlsx(wb=wb)

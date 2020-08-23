import pytest
import os


# def test_eggs_per_year(
#     test_dataset,
#     test_workbooks_eb,
#     test_provinces,
#     test_energy_aggregates,
#     test_balance_aggregates_energetischer,
#     test_launch_xlsx,
#     test_write_to_xlsx,
# ):
#     years = [2000, 2018]

#     wb = test_workbooks_eb["test_eb"]
#     ds = test_dataset

#     ds.add_eb_data(
#         energy_aggregates=test_energy_aggregates,
#         balance_aggregates=test_balance_aggregates_energetischer,
#         years=years,
#         provinces=test_provinces,
#         per_energy_aggregate=True,
#     )

#     test_write_to_xlsx(wb=wb, ds=ds, sheet_name="EGGS_PER_YEAR")

#     test_launch_xlsx(wb=wb)

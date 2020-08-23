# import pytest
# import os


# def test_esrc_over_years(
#     test_dataset,
#     test_workbooks_eb,
#     test_provinces,
#     test_main_energy_sources,
#     test_balance_aggregates_sectors,
#     test_launch_xlsx,
#     test_write_to_xlsx,
# ):
#     years = list(range(2000, 2019))

#     wb = test_workbooks_eb["test_eb"]
#     ds = test_dataset

#     ds.add_eb_data(
#         energy_sources=test_main_energy_sources,
#         balance_aggregates=test_balance_aggregates_sectors,
#         years=years,
#         provinces=test_provinces,
#         per_years=True,
#     )

#     test_write_to_xlsx(wb=wb, ds=ds, sheet_name="ESRC_OVER_YEARS")

#     test_launch_xlsx(wb=wb)

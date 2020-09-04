import os

import pytest


@pytest.mark.dependency()
def test_eb_eggs_per_year(
    test_dataset,
    test_eb_workbook,
    test_provinces,
    test_eb_energy_aggregates,
    test_eb_balance_aggregates_energetischer,
    test_eb_balance_aggregates_sectors,
    test_write_to_xlsx,
):
    years = [2000, 2018]

    ds = test_dataset

    ds.add_eb_data(
        energy_aggregates=test_eb_energy_aggregates,
        balance_aggregates=test_eb_balance_aggregates_sectors,
        years=years,
        provinces=test_provinces,
        per_energy_aggregate=True,
        show_source_values_for_energy_aggregates=True,
    )

    data_objects = [_data for _data in ds.objects.filter(per_energy_aggregate=True)]

    test_write_to_xlsx(
        wb=test_eb_workbook, data_objects=data_objects, sheet_name="EGGS_PER_YEAR"
    )


@pytest.mark.dependency(depends=["test_eb_eggs_per_year"])
def test_launch(test_launch_xlsx, test_eb_workbook):

    test_launch_xlsx(wb=test_eb_workbook)

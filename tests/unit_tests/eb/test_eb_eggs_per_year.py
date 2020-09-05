import os

import pytest


@pytest.mark.dependency()
def test_eb_eggs_per_year(
    test_data_instance,
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

    test_data_instance.create(
        energy_aggregates=test_eb_energy_aggregates,
        balance_aggregates=test_eb_balance_aggregates_sectors,
        years=years,
        provinces=test_provinces,
        stacked_energy_aggregates=True,
        is_eb=True,
    )

    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [
        _data for _data in test_dataset.objects.filter(stacked_energy_aggregates=True)
    ]

    test_write_to_xlsx(
        wb=test_eb_workbook,
        data_objects=test_data_objects,
        sheet_name="EGGS_PER_YEAR",
        # energy_aggregates_sum_only=True,
    )


@pytest.mark.dependency(depends=["test_eb_eggs_per_year"])
def test_launch(test_launch_xlsx, test_eb_workbook):

    test_launch_xlsx(wb=test_eb_workbook)

import os

import pytest


@pytest.mark.dependency()
def test_nea_years(
    test_data_instance,
    test_dataset,
    test_nea_workbook,
    test_provinces,
    test_nea_energy_sources,
    test_nea_usage_categories,
    test_nea_balance_aggregates,
    test_launch_xlsx,
    test_write_to_xlsx,
):

    years = list(range(2000, 2019))

    test_data_instance.create(
        energy_sources=test_nea_energy_sources,
        balance_aggregates=test_nea_balance_aggregates,
        usage_categories=test_nea_usage_categories,
        years=years,
        provinces=test_provinces,
        timeseries=True,
        is_nea=True,
    )

    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [
        _data for _data in test_dataset.objects.filter(timeseries=True)
    ]

    test_write_to_xlsx(
        wb=test_nea_workbook, data_objects=test_data_objects, sheet_name="YEARS",
    )


@pytest.mark.dependency(depends=["test_nea_years"])
def test_launch(test_launch_xlsx, test_nea_workbook):

    test_launch_xlsx(wb=test_nea_workbook)

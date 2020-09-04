import os

import pytest


@pytest.mark.dependency()
def test_stacked_usage_categories_per_year(
    test_dataset,
    test_nea_workbook,
    test_provinces,
    test_nea_energy_sources,
    test_nea_usage_categories,
    test_nea_balance_aggregates,
    test_launch_xlsx,
    test_write_to_xlsx,
):

    years = [2000, 2018]

    ds = test_dataset

    ds.add_nea_data(
        energy_sources=test_nea_energy_sources,
        balance_aggregates=test_nea_balance_aggregates,
        usage_categories=test_nea_usage_categories,
        years=years,
        provinces=test_provinces,
        per_usage_category=True,
        # per_balance_aggregate=True,
        # per_energy_source=True,
        # stacked_usage_categories=True,
        # stacked_balance_aggregates=True,
        # stacked_energy_sources=True,
        # per_years=True,
    )

    data_objects = [_data for _data in ds.objects.filter(per_usage_category=True,)]

    test_write_to_xlsx(
        wb=test_nea_workbook, data_objects=data_objects, sheet_name="STACKED_UC",
    )


@pytest.mark.dependency(depends=["test_stacked_usage_categories_per_year"])
def test_launch(test_launch_xlsx, test_nea_workbook):

    test_launch_xlsx(wb=test_nea_workbook)

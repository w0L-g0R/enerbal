import os

import pytest


@pytest.mark.dependency()
def test_nea_es_per_year(
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

    years = [2000, 2018]

    test_data_instance.create(
        energy_sources=test_nea_energy_sources,
        balance_aggregates=test_nea_balance_aggregates,
        usage_categories=test_nea_usage_categories,
        years=years,
        provinces=test_provinces,
        per_energy_source=True,
        is_nea=True,
    )

    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [
        _data for _data in test_dataset.objects.filter(per_energy_source=True)
    ]

    test_write_to_xlsx(
        wb=test_nea_workbook, data_objects=test_data_objects, sheet_name="ES_PER_YEAR",
    )


@pytest.mark.dependency(depends=["test_nea_es_per_year"])
def test_launch(test_launch_xlsx, test_nea_workbook):

    test_launch_xlsx(wb=test_nea_workbook)

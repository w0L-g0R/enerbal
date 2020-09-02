import os
import time
import pytest


@pytest.mark.dependency()
def test_all_nea(
    test_dataset,
    test_nea_workbook,
    test_provinces,
    test_nea_energy_sources,
    test_nea_usage_categories,
    test_nea_balance_aggregates,
    test_launch_xlsx,
    test_write_to_xlsx,
):

    from tests.unit_tests.nea.test_es_baggs_stacked_uc import (
        test_per_energy_source_and_balance_aggregate_stacked_usage_categories,
    )

    test_per_energy_source_and_balance_aggregate_stacked_usage_categories(
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )

    from tests.unit_tests.nea.test_es_uc_stacked_baggs import (
        test_per_energy_source_and_usage_category_stacked_balance_aggregates,
    )

    test_per_energy_source_and_usage_category_stacked_balance_aggregates(
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )
    return


@pytest.mark.dependency(depends=["test_all_nea"])
def test_launch(test_launch_xlsx, test_nea_workbook):

    test_launch_xlsx(wb=test_nea_workbook)

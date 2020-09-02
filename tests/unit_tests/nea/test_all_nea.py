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

    from tests.unit_tests.nea.test_uc_per_year import (
        test_stacked_usage_categories_per_year,
    )

    test_stacked_usage_categories_per_year(
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )

    from tests.unit_tests.nea.test_es_per_year import (
        test_stacked_energy_sources_per_year,
    )

    test_stacked_energy_sources_per_year(
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )
    from tests.unit_tests.nea.test_baggs_per_year import (
        test_stacked_balance_aggregates_per_year,
    )

    test_stacked_balance_aggregates_per_year(
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )

    from tests.unit_tests.nea.test_over_years import test_over_years

    test_over_years(
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

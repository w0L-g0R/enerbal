import os
import time
import pytest


@pytest.mark.dependency()
def test_all_nea(
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

    from tests.unit_tests.nea.test_nea_uc_per_year import test_nea_uc_per_year

    test_nea_uc_per_year(
        test_data_instance,
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )

    from tests.unit_tests.nea.test_nea_es_per_year import test_nea_es_per_year

    test_nea_es_per_year(
        test_data_instance,
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )
    from tests.unit_tests.nea.test_nea_baggs_per_year import test_nea_baggs_per_year

    test_nea_baggs_per_year(
        test_data_instance,
        test_dataset,
        test_nea_workbook,
        test_provinces,
        test_nea_energy_sources,
        test_nea_usage_categories,
        test_nea_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )

    from tests.unit_tests.nea.test_nea_years import test_nea_years

    test_nea_years(
        test_data_instance,
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

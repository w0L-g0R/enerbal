import os
import time

import pytest


@pytest.mark.dependency()
def test_all_thg(
    test_data_instance,
    test_dataset,
    test_thg_workbook,
    test_provinces,
    test_emittent_shares,
    test_thg_balance_aggregates,
    test_launch_xlsx,
    test_write_to_xlsx,
):

    from tests.unit_tests.thg.test_thg_es_per_year import test_thg_es_per_year

    test_thg_es_per_year(
        test_data_instance,
        test_dataset,
        test_thg_workbook,
        test_provinces,
        test_emittent_shares,
        test_thg_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )
    from tests.unit_tests.thg.test_thg_baggs_per_year import test_thg_baggs_per_year

    test_thg_baggs_per_year(
        test_data_instance,
        test_dataset,
        test_thg_workbook,
        test_provinces,
        test_emittent_shares,
        test_thg_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )

    from tests.unit_tests.thg.test_thg_years import test_thg_years

    test_thg_years(
        test_data_instance,
        test_dataset,
        test_thg_workbook,
        test_provinces,
        test_emittent_shares,
        test_thg_balance_aggregates,
        test_launch_xlsx,
        test_write_to_xlsx,
    )
    return


@pytest.mark.dependency(depends=["test_all_thg"])
def test_launch(test_launch_xlsx, test_thg_workbook):

    test_launch_xlsx(wb=test_thg_workbook)

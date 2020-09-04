import os
import time

import pytest


@pytest.mark.dependency()
def test_all_res(
    test_dataset,
    test_provinces,
    test_res_workbook,
    test_res_shares,
    test_res_balance_aggregates,
    test_write_to_xlsx,
):

    from tests.unit_tests.res.test_res_baggs_per_year import test_res_baggs_per_year

    test_res_baggs_per_year(
        test_dataset,
        test_provinces,
        test_res_workbook,
        test_res_shares,
        test_res_balance_aggregates,
        test_write_to_xlsx,
    )

    from tests.unit_tests.res.test_res_over_years import test_res_over_years

    test_res_over_years(
        test_dataset,
        test_provinces,
        test_res_workbook,
        test_res_shares,
        test_res_balance_aggregates,
        test_write_to_xlsx,
    )

    return


@pytest.mark.dependency(depends=["test_all_res"])
def test_launch(test_launch_xlsx, test_res_workbook):

    test_launch_xlsx(wb=test_res_workbook)

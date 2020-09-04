import os

import pytest


@pytest.mark.dependency()
def test_res_baggs_per_year(
    test_dataset,
    test_provinces,
    test_res_workbook,
    test_res_shares,
    test_res_balance_aggregates,
    test_write_to_xlsx,
):

    years = list(range(2015, 2019))

    ds = test_dataset

    ds.add_eb_data(
        balance_aggregates=test_res_balance_aggregates,
        years=years,
        provinces=test_provinces,
        is_res=True,
        per_balance_aggregate=True,
    )

    # data_objects = [_data for _data in ds.objects.filter(per_years=True)]
    data_objects = ds.objects

    test_write_to_xlsx(
        wb=test_res_workbook, data_objects=data_objects, sheet_name="RES_PER_YEAR"
    )


@pytest.mark.dependency(depends=["test_res_baggs_over_years"])
def test_launch(test_launch_xlsx, test_res_workbook):

    test_launch_xlsx(wb=test_res_workbook)

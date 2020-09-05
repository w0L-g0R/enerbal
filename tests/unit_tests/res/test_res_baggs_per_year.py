import os

import pytest


@pytest.mark.dependency()
def test_res_baggs_per_year(
    test_data_instance,
    test_dataset,
    test_provinces,
    test_res_workbook,
    test_res_shares,
    test_res_balance_aggregates,
    test_write_to_xlsx,
):

    years = list(range(2015, 2019))
    test_data_instance.create(
        balance_aggregates=test_res_balance_aggregates,
        years=years,
        provinces=test_provinces,
        per_balance_aggregate=True,
        is_res=True,
    )

    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [
        _data for _data in test_dataset.objects.filter(per_balance_aggregate=True)
    ]

    test_write_to_xlsx(
        wb=test_res_workbook, data_objects=test_data_objects, sheet_name="RES_PER_YEAR"
    )


@pytest.mark.dependency(depends=["test_res_baggs_per_year"])
def test_launch(test_launch_xlsx, test_res_workbook):

    test_launch_xlsx(wb=test_res_workbook)

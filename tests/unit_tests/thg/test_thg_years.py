import os

import pytest


@pytest.mark.dependency()
def test_thg_years(
    test_data_instance,
    test_dataset,
    test_thg_workbook,
    test_provinces,
    test_emittent_shares,
    test_thg_balance_aggregates,
    test_launch_xlsx,
    test_write_to_xlsx,
):

    years = list(range(2000, 2019))

    test_data_instance.create(
        emittent_shares=test_emittent_shares,
        balance_aggregates=test_thg_balance_aggregates,
        years=years,
        provinces=test_provinces,
        timeseries=True,
        is_thg=True,
    )

    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [
        _data for _data in test_dataset.objects.filter(timeseries=True)
    ]

    test_write_to_xlsx(
        wb=test_thg_workbook, data_objects=test_data_objects, sheet_name="YEARS",
    )


@pytest.mark.dependency(depends=["test_thg_years"])
def test_launch(test_launch_xlsx, test_thg_workbook):

    test_launch_xlsx(wb=test_thg_workbook)

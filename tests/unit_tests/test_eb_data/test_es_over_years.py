import os

import pytest


def test_es_over_years(
    test_dataset,
    test_workbook,
    test_provinces,
    test_main_energy_sources,
    test_balance_aggregates_sectors,
    test_write_to_xlsx,
):
    years = list(range(2010, 2019))

    wb = test_workbook["test_eb"]
    ds = test_dataset

    ds.add_eb_data(
        energy_sources=test_main_energy_sources,
        balance_aggregates=test_balance_aggregates_sectors,
        years=years,
        provinces=test_provinces,
        per_years=True,
    )

    data_objects = [_data for _data in ds.objects.filter(per_years=True)]

    test_write_to_xlsx(wb=wb, data_objects=data_objects, sheet_name="ESRC_OVER_YEARS")


def test_launch(test_launch_xlsx, test_workbook):

    wb = test_workbook["test_eb"]
    test_launch_xlsx(wb=wb)

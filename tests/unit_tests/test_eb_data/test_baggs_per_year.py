import os

import pytest


def test_baggs_per_year(
    test_dataset,
    test_workbook,
    test_provinces,
    test_balance_aggregates_sectors,
    test_energy_source_elektrische_energie,
    test_energy_source_gesamtbilanz,
    test_launch_xlsx,
    test_write_to_xlsx,
):
    years = [2000, 2018]

    wb = test_workbook["test_eb"]
    ds = test_dataset

    ds.add_eb_data(
        energy_sources=test_energy_source_elektrische_energie
        + test_energy_source_gesamtbilanz,
        balance_aggregates=test_balance_aggregates_sectors,
        years=years,
        provinces=test_provinces,
        per_balance_aggregate=True,
    )

    data_objects = [_data for _data in ds.objects.filter(per_balance_aggregate=True)]

    test_write_to_xlsx(wb=wb, data_objects=data_objects, sheet_name="BAGGS_PER_YEAR")


def test_launch(test_launch_xlsx, test_workbook):

    wb = test_workbook["test_eb"]
    test_launch_xlsx(wb=wb)

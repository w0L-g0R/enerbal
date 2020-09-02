import os

import pytest


@pytest.mark.dependency()
def test_baggs_per_year(
    test_dataset,
    test_provinces,
    test_eb_workbook,
    test_eb_balance_aggregates_sectors,
    test_eb_energy_source_elektrische_energie,
    test_eb_energy_source_gesamtbilanz,
    test_write_to_xlsx,
):

    years = [2000, 2018]

    ds = test_dataset

    ds.add_eb_data(
        energy_sources=test_eb_energy_source_elektrische_energie
        + test_eb_energy_source_gesamtbilanz,
        balance_aggregates=test_eb_balance_aggregates_sectors,
        years=years,
        provinces=test_provinces,
        per_balance_aggregate=True,
    )

    data_objects = [_data for _data in ds.objects.filter(per_balance_aggregate=True)]

    test_write_to_xlsx(
        wb=test_eb_workbook, data_objects=data_objects, sheet_name="BAGGS_PER_YEAR"
    )


@pytest.mark.dependency(depends=["test_baggs_per_year"])
def test_launch(test_launch_xlsx, test_eb_workbook):

    test_launch_xlsx(wb=test_eb_workbook)

import os

import pytest


def test_per_et_and_uc(
    test_dataset,
    test_workbooks_eb,
    test_provinces,
    test_main_energy_sources,
    test_balance_aggregates_sectors,
    test_write_to_xlsx,
):
    years = list(range(2000, 2019))

    wb = test_workbooks_eb["test_eb"]
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


def test_per_et_and_bagg(
    test_dataset,
    test_workbooks_eb,
    test_provinces,
    test_energy_aggregates,
    test_balance_aggregates_energetischer,
    test_balance_aggregates_sectors,
    test_launch_xlsx,
    test_write_to_xlsx,
):
    years = [2000, 2018]

    wb = test_workbooks_eb["test_eb"]
    ds = test_dataset

    ds.add_eb_data(
        energy_aggregates=test_energy_aggregates,
        balance_aggregates=test_balance_aggregates_sectors,
        years=years,
        provinces=test_provinces,
        per_energy_aggregate=True,
        show_source_values_for_energy_aggregates=True,
    )

    data_objects = [_data for _data in ds.objects.filter(per_energy_aggregate=True)]

    test_write_to_xlsx(wb=wb, data_objects=data_objects, sheet_name="EGGS_PER_YEAR")


def test_per_sec_and_et(
    test_dataset,
    test_workbooks_eb,
    test_provinces,
    test_balance_aggregates_sectors,
    test_energy_source_elektrische_energie,
    test_energy_source_gesamtbilanz,
    test_launch_xlsx,
    test_write_to_xlsx,
):
    years = [2000, 2018]

    wb = test_workbooks_eb["test_eb"]
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


def test_launch(test_launch_xlsx, test_workbooks_eb):

    wb = test_workbooks_eb["test_eb"]
    test_launch_xlsx(wb=wb)

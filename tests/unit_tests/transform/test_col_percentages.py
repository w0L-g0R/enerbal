import os

import pytest


@pytest.mark.dependency()
def test_unit_conversion(
    test_data_instance,
    test_dataset,
    test_provinces,
    test_eb_workbook,
    test_eb_main_energy_sources,
    test_eb_energy_source_gesamtbilanz,
    test_eb_balance_aggregates_sectors,
    test_eb_umwandlungsausstoss_and_umwandlungseinsatz,
    test_write_to_xlsx,
):
    years = list(range(2012, 2017))

    test_data_instance.create(
        energy_sources=test_eb_main_energy_sources,
        balance_aggregates=test_eb_balance_aggregates_sectors,
        # balance_aggregates=[["Energetischer Endverbrauch"]],
        years=years,
        provinces=test_provinces,
        timeseries=True,
        is_eb=True,
    )

    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [
        _data for _data in test_dataset.objects.filter(timeseries=True)
    ]

    for test_data_object in test_data_objects:
        test_data_object.columns_to_percentages = True
        # print("\ntest_data_object: ", test_data_object.frame)

    test_write_to_xlsx(
        wb=test_eb_workbook,
        data_objects=test_data_objects,
        sheet_name="ES_OVER_YEARS_UNIT_CONV",
    )


@pytest.mark.dependency(depends=["test_unit_conversion"])
def test_launch(test_launch_xlsx, test_eb_workbook):

    test_launch_xlsx(wb=test_eb_workbook)

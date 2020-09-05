import os

import pytest


@pytest.mark.dependency()
def test_eb_years(
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
    years = list(range(2010, 2019))

    test_data_instance.create(
        energy_sources=test_eb_energy_source_gesamtbilanz,
        balance_aggregates=test_eb_balance_aggregates_sectors
        + test_eb_umwandlungsausstoss_and_umwandlungseinsatz,
        years=years,
        provinces=test_provinces,
        per_years=True,
        is_eb=True,
    )

    test_dataset.add_data(data=test_data_instance)

    test_data_objects = [_data for _data in test_dataset.objects.filter(per_years=True)]

    test_write_to_xlsx(
        wb=test_eb_workbook, data_objects=test_data_objects, sheet_name="ES_OVER_YEARS"
    )


@pytest.mark.dependency(depends=["test_eb_es_over_years"])
def test_launch(test_launch_xlsx, test_eb_workbook):

    test_launch_xlsx(wb=test_eb_workbook)

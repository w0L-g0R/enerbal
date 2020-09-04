import os
import time

import pytest


@pytest.mark.dependency()
def test_all_eb(
    test_dataset,
    test_provinces,
    test_eb_workbook,
    test_eb_energy_aggregates,
    test_eb_balance_aggregates_energetischer,
    test_eb_balance_aggregates_sectors,
    test_eb_energy_source_elektrische_energie,
    test_eb_energy_source_gesamtbilanz,
    test_eb_main_energy_sources,
    test_eb_umwandlungsausstoss_and_umwandlungseinsatz,
    test_write_to_xlsx,
):

    from tests.unit_tests.eb.test_eb_baggs_per_year import test_eb_baggs_per_year

    test_eb_baggs_per_year(
        test_dataset,
        test_provinces,
        test_eb_workbook,
        test_eb_balance_aggregates_sectors,
        test_eb_energy_source_elektrische_energie,
        test_eb_energy_source_gesamtbilanz,
        test_write_to_xlsx,
    )
    from tests.unit_tests.eb.test_eb_eggs_per_year import test_eb_eggs_per_year

    test_eb_eggs_per_year(
        test_dataset,
        test_eb_workbook,
        test_provinces,
        test_eb_energy_aggregates,
        test_eb_balance_aggregates_energetischer,
        test_eb_balance_aggregates_sectors,
        test_write_to_xlsx,
    )
    from tests.unit_tests.eb.test_eb_es_over_years import test_eb_es_over_years

    test_eb_es_over_years(
        test_dataset,
        test_provinces,
        test_eb_workbook,
        test_eb_main_energy_sources,
        test_eb_energy_source_gesamtbilanz,
        test_eb_balance_aggregates_sectors,
        test_eb_umwandlungsausstoss_and_umwandlungseinsatz,
        test_write_to_xlsx,
    )
    return


@pytest.mark.dependency(depends=["test_all_eb"])
def test_launch(test_launch_xlsx, test_eb_workbook):

    test_launch_xlsx(wb=test_eb_workbook)

import os
import time
from pathlib import Path

import pytest

from enspect.models.dataset import DataSet
from enspect.models.workbook import Workbook
from enspect.paths import file_paths

CWD = Path(__file__).parents[1].resolve()

# /////////////////////////////////////////////////////////////////// WB


@pytest.fixture(scope="session")
def test_eb_workbook():

    os.system("TASKKILL /F /IM excel.exe")

    time.sleep(2)

    filename = CWD / "unit_tests/results/test_eb.xlsx"

    if Path(filename).exists():
        os.remove(filename)

    wb = Workbook(name="WB_TEST", filename=filename)

    for sheet in wb.book.sheetnames:
        if sheet in ["Sheet", "Tabelle1"]:
            pass
        else:
            del wb.book[sheet]

    wb.add_sheets(["EGGS_PER_YEAR", "BAGGS_PER_YEAR", "ES_OVER_YEARS"])

    wb.save()

    return wb


# /////////////////////////////////////////////////////////////////// E-SOURCES


@pytest.fixture(scope="session")
def test_eb_main_energy_sources():
    return [
        "Gesamtenergiebilanz",
        "Elektrische Energie",
        "Fernwärme",
        "Brennbare Abfälle",
        "ERNEUERBARE",
        "KOHLE",
        "ÖL",
        "GAS",
    ]


@pytest.fixture(scope="session")
def test_eb_energy_source_gesamtbilanz():
    return [
        "Gesamtenergiebilanz",
    ]


@pytest.fixture(scope="session")
def test_eb_energy_source_elektrische_energie():
    return [
        "Elektrische Energie",
    ]


# ////////////////////////////////////////////////////////////////////// E-AGGS
@pytest.fixture(scope="session")
def test_eb_energy_aggregates():
    return [
        "Elektrische",
        "Fernwärme",
        "Erneuerbare",
        "Fossil-fest",
        "Fossil-flüssig",
        "Fossil-gasförmig",
        "Biogen-fest",
        "Biogen-flüssig",
        "Biogen-gasförmig",
    ]


# ////////////////////////////////////////////////////////////////////// B-AGGS
@pytest.fixture(scope="session")
def test_eb_balance_aggregates_inputs_output():
    return [
        "Inländ. Erzeugung v. Rohenergie",
        "Importe",
        "Lager",
        "Recycling/Prod. Trans.",
        "Exporte",
        "Bruttoinlandsverbrauch",
        "Umwandlungseinsatz",
        "Umwandlungsausstoß",
        "Verbrauch des Sektors Energie",
        "Transportverluste",
        "Nichtenergetischer Verbrauch",
        "Energetischer Endverbrauch",
    ]


@pytest.fixture(scope="session")
def test_eb_balance_aggregates_energetischer():
    return [
        "Energetischer Endverbrauch",
    ]


# ////////////////////////////////////////////////////////////////// B-SECTORS
@pytest.fixture(scope="session")
def test_eb_balance_aggregates_sectors():
    return [
        "Energetischer Endverbrauch",
        "Produzierender Bereich",
        "Verkehr",
        "Öffentliche und Private Dienstleistungen",
        "Private Haushalte",
        "Landwirtschaft",
    ]

import pytest
from pathlib import Path
import os
from enspect.paths import file_paths
from enspect.models.dataset import DataSet
from enspect.models.workbook import Workbook
import time

CWD = Path(__file__).parent.resolve()

# /////////////////////////////////////////////////////////////////// PROVINCES
@pytest.fixture(scope="session")
def test_provinces():
    return [
        "Bgd",
        "Ktn",
        "Noe",
        "Ooe",
        "Sbg",
        "Stk",
        "Tir",
        "Vbg",
        "Wie",
        "AT",
    ]


# /////////////////////////////////////////////////////////////////// E-SOURCES
@pytest.fixture(scope="session")
def test_main_energy_sources():
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
def test_energy_source_gesamtbilanz():
    return [
        "Gesamtenergiebilanz",
    ]


@pytest.fixture(scope="session")
def test_energy_source_elektrische_energie():
    return [
        "Elektrische Energie",
    ]


# ////////////////////////////////////////////////////////////////////// E-AGGS
@pytest.fixture(scope="session")
def test_energy_aggregates():
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
def test_balance_aggregates_inputs_output():
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
def test_balance_aggregates_energetischer():
    return [
        "Energetischer Endverbrauch",
    ]


# ////////////////////////////////////////////////////////////////// B-SECTORS
@pytest.fixture(scope="session")
def test_balance_aggregates_sectors():
    return [
        "Energetischer Endverbrauch",
        "Produzierender Bereich",
        "Verkehr",
        "Öffentliche und Private Dienstleistungen",
        "Private Haushalte",
        "Landwirtschaft",
    ]

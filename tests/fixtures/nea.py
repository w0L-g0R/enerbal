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
def test_nea_workbook():

    os.system("TASKKILL /F /IM excel.exe")

    time.sleep(2)

    filename = CWD / "unit_tests/results/test_nea.xlsx"

    if Path(filename).exists():
        os.remove(filename)

    wb = Workbook(name="WB_TEST", filename=filename)

    for sheet in wb.book.sheetnames:
        sheet
        if sheet in ["Sheet", "Tabelle1"]:
            pass
        else:
            del wb.book[sheet]

    wb.add_sheets(["STACKED_UC", "STACKED_BAGGS", "STACKED_ES", "YEARS"])

    wb.save()

    return wb


# /////////////////////////////////////////////////////////////////// E-SOURCES


@pytest.fixture(scope="session")
def test_nea_energy_sources():
    return [
        "Steinkohle",
        "Insgesamt",
    ]


@pytest.fixture(scope="session")
def test_nea_usage_categories():
    return [
        "Raumheizung und Klimaanlagen",
        "Dampferzeugung",
        # "Industrieöfen",
        # "Standmotoren",
        # "Traktion",
        # "Beleuchtung und EDV",
        # "Elektrochemische Zwecke",
        # "Summe",
    ]


# ////////////////////////////////////////////////////////////////// B-SECTORS
@pytest.fixture(scope="session")
def test_nea_balance_aggregates():
    return [
        "Gesamt (ohne E1 - E7)",
        "Produzierender Bereich Gesamt",
        "Transport Gesamt",
        "Offentliche und Private Dienstleistungen",
        "Private Haushalte",
        "Landwirtschaft",
    ]

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
def test_res_workbook():

    os.system("TASKKILL /F /IM excel.exe")

    time.sleep(2)

    filename = CWD / "unit_tests/results/test_res.xlsx"

    if Path(filename).exists():
        os.remove(filename)

    wb = Workbook(name="WB_TEST", filename=filename)

    for sheet in wb.book.sheetnames:
        if sheet in ["Sheet", "Tabelle1"]:
            pass
        else:
            del wb.book[sheet]

    wb.add_sheets(["RES_OVER_YEARS", "RES_PER_YEAR"])

    wb.save()

    return wb


# /////////////////////////////////////////////////////////////////// E-SOURCES


@pytest.fixture(scope="session")
def test_res_balance_aggregates():
    return [
        ["Anteil anrechenbare Erneuerbare insgesamt"],
        ["Anteil anrechenbare Erneuerbare Elektrizitätserzeugung"],
        [
            "Elektrische Energie Produktion erneuerbar (TJ)",
            "Wasserkraft ohne Pumpe normalisiert (MWh)",
            "Ausnutzungsdauer (h)",
        ],
        ["Fernwärme Produktion erneuerbar (TJ)", "Laugen"],
        ["Energetischer Endverbrauch Erneuerbare (TJ)", "Scheitholz"],
    ]


@pytest.fixture(scope="session")
def test_res_shares():
    return [
        ["Anteil anrechenbare Erneuerbare insgesamt"],
        ["Anteil anrechenbare Erneuerbare Elektrizitätserzeugung"],
        ["Anteil anrechenbare Erneuerbare Fernwärmeerzeugung"],
        ["Anteil anrechenbare Erneuerbare Verkehr"],
        ["Anteil anrechenbare Erneuerbare Industrie"],
        ["Anteil anrechenbare Erneuerbare Dienstleistungen"],
        ["Anteil anrechenbare Erneuerbare Haushalte"],
        ["Anteil Erneuerbare Landwirtschaft"],
    ]


@pytest.fixture(scope="session")
def test_res_intalled_cap_hydro():
    return [
        "Elektrische Energie Produktion erneuerbar (TJ)",
        "Wasserkraft mit Pumpe normalisiert (MWh)",
        "Installierte Kapazität mit Pumpe (MW)",
    ]

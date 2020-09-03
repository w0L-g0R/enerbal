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

    wb.add_sheets(["RES"])

    wb.save()

    return wb


# /////////////////////////////////////////////////////////////////// E-SOURCES

@pytest.fixture(scope="session")
def test_res_shares():
    return [
        "Anteil anrechenbare Erneuerbare insgesamt",
        "Anteil anrechenbare Erneuerbare Elektrizitätserzeugung",
        "Anteil anrechenbare Erneuerbare Fernwärmeerzeugung",
        "Anteil anrechenbare Erneuerbare Verkehr",
        "Anteil anrechenbare Erneuerbare Industrie",
        "Anteil anrechenbare Erneuerbare Dienstleistungen",
        "Anteil anrechenbare Erneuerbare Haushalte",
        "Anteil Erneuerbare Landwirtschaft",
    ]


@pytest.fixture(scope="session")
def test_res_intalled_cap_hydro():

    midx = {
        "bagg_0": [
            "Elektrische Energie Produktion erneuerbar (TJ)"
        ],
        "bagg_1": [
            "Wasserkraft mit Pumpe normalisiert (MWh)",
        ],
        "bagg_2": [
            "Installierte Kapazität mit Pumpe (MW)",
        ],

    }

    return midx


@pytest.fixture(scope="session")
def test_res_usage_time_hydro():

    midx = {
        "bagg_0": [
            "Elektrische Energie Produktion erneuerbar (TJ)"
        ],
        "bagg_1": [
            "Wasserkraft ohne Pumpe normalisiert (MWh)",
        ],
        "bagg_2": [
            "Ausnutzungsdauer (h)",
        ],
    }

    return midx


@pytest.fixture(scope="session")
def test_res_generation_run_of_river():

    # midx = {
    #     "bagg_0": [
    #         "Elektrische Energie Produktion erneuerbar (TJ)"
    #     ],
    #     "bagg_1": [
    #         "Wasserkraft ohne Pumpe normalisiert (MWh)",
    #     ],
    #     "bagg_2": [
    #         "Erzeugung aus natürlichem Zufluß (MWh)",
    #     ],
    # }

    # return midx
    return [
        "Elektrische Energie Produktion erneuerbar (TJ)",
        "Wasserkraft ohne Pumpe normalisiert (MWh)",
        "Erzeugung aus natürlichem Zufluß (MWh)",
    ]

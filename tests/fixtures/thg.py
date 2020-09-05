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
def test_thg_workbook():

    os.system("TASKKILL /F /IM excel.exe")

    time.sleep(2)

    filename = CWD / "unit_tests/results/test_thg.xlsx"

    if Path(filename).exists():
        os.remove(filename)

    wb = Workbook(name="WB_TEST", filename=filename)

    for sheet in wb.book.sheetnames:
        if sheet in ["Sheet", "Tabelle1"]:
            pass
        else:
            del wb.book[sheet]

    wb.add_sheets(["ES_PER_YEAR", "BAGGS_PER_YEAR", "YEARS"])

    wb.save()

    return wb


# /////////////////////////////////////////////////////////////////// E-SOURCES


@pytest.fixture(scope="session")
def test_thg_balance_aggregates():
    return [
        ["Energie"],
        ["Kleinverbrauch"],
        ["Industrie"],
        ["Verkehr"],
        ["Landwirtschaft"],
        ["Sonstige"],
        ["Gebäude"],
    ]


@pytest.fixture(scope="session")
def test_emittent_shares():
    return [
        "TOTAL",
        "ETS",
        "NON_ETS",
    ]

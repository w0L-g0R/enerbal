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
def test_stats_workbook():

    os.system("TASKKILL /F /IM excel.exe")

    time.sleep(2)

    filename = CWD / "unit_tests/results/test_stats.xlsx"

    if Path(filename).exists():
        os.remove(filename)

    wb = Workbook(name="WB_TEST", filename=filename)

    for sheet in wb.book.sheetnames:
        if sheet in ["Sheet", "Tabelle1"]:
            pass
        else:
            del wb.book[sheet]

    wb.add_sheets(["PRI_CARS", "AREA", "POP"])

    wb.save()

    return wb


# @pytest.fixture(scope="session")
# def test_HGS_data():

#     filename = file_paths["pickle_hgs"] / "AT_HGS.p"

#     return filename

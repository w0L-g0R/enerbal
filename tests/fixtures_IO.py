import os
import time
from pathlib import Path
from pprint import pprint

import pytest

from enspect.models.dataset import DataSet
from enspect.models.workbook import Workbook
from enspect.paths import file_paths

CWD = Path(__file__).parent.resolve()


def print_inside_tests(*args, **kwargs):

    with capsys.disabled():
        for arg in args:
            pprint(arg)

        for kwarg in kwargs:
            pprint(kwarg)


# assert out == "hello\n"
# assert err == "world\n"


@pytest.fixture(scope="session")
def test_dataset():
    """
    Pass the templates filesystem from src to tests
    """
    return DataSet(name=f"Testset", file_paths=file_paths)


@pytest.fixture(scope="session")
def test_workbooks_eb():

    os.system("TASKKILL /F /IM excel.exe")

    time.sleep(2)

    workbooks = dict.fromkeys(
        [
            # "test_eaggs_for_sectors_per_year",
            # "test_add_multiple_baggs_per_year",
            # "test_yearly_data",
            "test_eb"
        ]
    )

    files_path = CWD / "unit_tests/test_eb_data/result_files"

    for name in workbooks.keys():

        filename = files_path / Path(name + ".xlsx")

        if Path(filename).exists():
            os.remove(filename)

        workbooks[name] = Workbook(
            name="WB_TEST", filename=files_path / Path(name + ".xlsx")
        )

        for sheet in workbooks[name].book.sheetnames:
            sheet
            if sheet in ["Sheet", "Tabelle1"]:
                pass
            else:
                del workbooks[name].book[sheet]

        workbooks[name].add_sheets(
            ["EGGS_PER_YEAR", "BAGGS_PER_YEAR", "ESRC_OVER_YEARS"]
        )

        workbooks[name].save()

    return workbooks


@pytest.fixture(scope="session")
def test_write_to_xlsx():
    def _write(wb, data_objects, sheet_name):
        # data_objects = [_data for _data in ds.objects.filter()]

        # data_object_ids = [_data._id for _data in ds.objects.filter()]

        # wb.add_sheets(sheets=sheet_name)

        for data in data_objects:

            wb.write_to_sheet(data=data, sheet=sheet_name)

        wb.save()

        return

    return _write


@pytest.fixture(scope="session")
def test_close_xlsx():
    os.system("TASKKILL /F /IM excel.exe")


@pytest.fixture()
def test_launch_xlsx(scope="session"):
    def _launch(wb):
        wb.launch()
        time.sleep(25)

        return

    return _launch

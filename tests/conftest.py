import pytest
from pathlib import Path
import os
from enspect.paths import file_paths
from enspect.models.dataset import DataSet

from enspect.xlsx.utils import get_workbook, write_to_sheet
from enspect.xlsx.workbook import xlsx

# def pytest_setup_options():
#     """called before webdriver is initialized"""
#     options = Options()
#     options.add_argument('--disable-gpu')
#     return options


# User
TEST_USER = "WG"
# Namespaces
#
# Pointer to working directory
WORKING_DIRECTORY = Path.cwd()

# ROOT and FS of test package
SRC_ROOT = Path("src/dispat").resolve()

# Helper prints
# print("\n{}  TEST CONFIG  {}".format("/"*30, "/"*30))
# print('\nTEST_FS.getsyspath("local_test_projects"):\n',
#       TEST_FS.getsyspath("local_test_projects"))
# print('\nTEST_FS.root_path:\n', TEST_FS.root_path)
# print('\nTEST_FS.getsyspath(TEST_FS.root_path):\n',
#       TEST_FS.getsyspath(TEST_FS.root_path))


@pytest.fixture(scope="session")
def test_dataset():
    """
    Pass the templates filesystem from src to tests
    """
    return DataSet(name=f"Testset", file_paths=file_paths)


@pytest.fixture(scope="session")
def test_workbook():
    """
    Pass the templates filesystem from src to tests
    """

    wb = xlsx(name="WB1", path="test.xlsx")

    for sheet in wb.book.sheetnames:
        print("sheet: ", sheet)
        if sheet not in ["Sheet1"]:
            del wb.book[sheet]

    wb.book.save("test.xlsx")

    return wb


@pytest.fixture(scope="session")
def test_provinces():
    """
    Pass the templates filesystem from src to tests
    """
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


@pytest.fixture(scope="session")
def test_main_energy_aggregates():
    """
    Pass the templates filesystem from src to tests
    """
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
def test_balance_aggregates_index_0():
    """
    Pass the templates filesystem from src to tests
    """

    return [
        # "Inländ. Erzeugung v. Rohenergie",
        "Importe",
        # "Lager",
        # "Recycling/Prod. Trans.",
        # "Exporte",
        # "Bruttoinlandsverbrauch",
        # "Umwandlungseinsatz",
        # "Umwandlungsausstoß",
        # "Verbrauch des Sektors Energie",
        # "Transportverluste",
        # "Nichtenergetischer Verbrauch",
        "Energetischer Endverbrauch",
    ]

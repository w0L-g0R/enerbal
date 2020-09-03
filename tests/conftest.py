import os
import time
from pathlib import Path

import pytest

from src.enspect.models.dataset import DataSet
from src.enspect.models.workbook import Workbook
from src.enspect.paths import file_paths
from src.enspect.settings import set_pd_options
from tests.fixtures.eb import *
from tests.fixtures.IO import *
from tests.fixtures.nea import *
from tests.fixtures.res import *


@pytest.fixture(scope="session")
def test_provinces():

    from src.enspect.aggregates.common import provinces

    return provinces


set_pd_options()
TEST_USER = "WG"
SRC_ROOT = Path("src/dispat").resolve()

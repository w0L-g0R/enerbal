# NOTE: Prints in pytest -> fixture capsys

NOTE: Use capsys as test function argument!

def print_inside_tests(\*args, \*\*kwargs):

    with capsys.disabled():
       for arg in args:
            pprint.PrettyPrinter(indent=4, depth=4).pprint(arg)

        for kwarg in kwargs:
            pprint.PrettyPrinter(indent=4, depth=4).pprint(kwarg)

****\*\*\*\*****\*\*****\*\*\*\*****\_\_****\*\*\*\*****\*\*****\*\*\*\***** PYTESTDOCS
@ https://docs.pytest.org/en/latest/usage.html#cmdline

Running pytest can result in six different exit codes:

Exit code 0: All tests were collected and passed successfully
Exit code 1: Tests were collected and run but some of the tests failed
Exit code 2: Test execution was interrupted by the user
Exit code 3: Internal error happened while executing tests
Exit code 4: pytest command line usage error
Exit code 5: No tests were collected

pytest --version # shows where pytest was imported from
pytest --fixtures # show available builtin function arguments
pytest -h | --help # show help on command line and config file options


# Collecting info about existing tests

pytest --collect-only

# Calling pytest through python -m pytest

python -m pytest [...]

# Run tests in a module

pytest test_mod.py

# Run tests in a directory

pytest testing/

# Run tests by keyword expressions

pytest -k "MyClass and not method"

Modifying Python traceback printing

pytest --showlocals # show local variables in tracebacks
pytest -l # show local variables (shortcut)

pytest --tb=auto # (default) 'long' tracebacks for the first and last # entry, but 'short' style for the other entries
pytest --tb=long # exhaustive, informative traceback formatting
pytest --tb=short # shorter traceback format
pytest --tb=line # only one line per failure
pytest --tb=native # Python standard library formatting
pytest --tb=no # no traceback at all

The "-r" options accepts a number of characters after it,
with "a" used above meaning “all except passes”.

Here is the full list of available characters that can be used:

f - failed
E - error
s - skipped
x - xfailed
X - xpassed
p - passed
P - passed with output
Special characters for (de)selection of groups:

a - all except pP
A - all
N - none, this can be used to display nothing (since fE is the default)

****\*\*\*\*****\*\*****\*\*\*\*****\_\_****\*\*\*\*****\*\*****\*\*\*\***** PYTESTGUIDE
@ https://pytestguide.readthedocs.io/en/latest/pytestGuide/

1.2. Test Code
pytext -x runs the test and stops as soon as the test fails.
py.test it runs all the tests in the directory, which start with name ‘test’ or classes which start with name ‘Test’. Note that, these names are case sensitive i.e. we can not use test and Test interchangeably.
py.test filename.py runs all the test in the filename.py
pytext -v : it is same as above commands but results are verbose,
i.e. gives some details about the results.

1.4. Mark
@pytest.mark.pyfile
def test_stat2Num():
""" Test method for stat2Num """

    assert stat2Num(3, 2) == (5, 2.5)
    assert stat2Num(3, 2.0) == (5, 2.5)
    assert stat2Num(3.5, 2.5) == (6, 3)
    assert stat2Num(3.5, 2.5) == (6.0, 3.0)

\$ py.test -m pyfile
[...]
=== 2 tests deselected by "-m 'pyfile'" ========
=== 3 passed, 2 deselected in 0.11 seconds =====

1.5. Parameterized test
@pytest.mark.parametrize("x, y", [(3,2), (3, 2.0), (3.5, 2.5)])
def test_stat2Num(x, y):
""" Parameterized test method for stat2Num """

    assert stat2Num(x, y) == (x+y, (x+y)/2)

****\*\*\*\*****\*\*****\*\*\*\*****\_\_****\*\*\*\*****\*\*****\*\*\*\***** PYTESTDOCS
@ https://docs.pytest.org/en/latest/fixture.html#fixtures

Parametrizing fixtures

# content of conftest.py

import pytest
import smtplib

@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
yield smtp_connection
print("finalizing {}".format(smtp_connection))
smtp_connection.close()

"

We can flag the fixture to create two smtp_connection
fixture instances which will cause all tests using the
fixture to run twice. The fixture function gets access
to each parameter through the special request object.

"

Use fixtures marker:

# content of conftest.py

import os
import shutil
import tempfile

import pytest

@pytest.fixture
def cleandir():
old_cwd = os.getcwd()
newpath = tempfile.mkdtemp()
os.chdir(newpath)
yield
os.chdir(old_cwd)
shutil.rmtree(newpath)

and declare its use in a test module via a usefixtures marker:

# content of test_setenv.py

import os
import pytest

@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit:
def test_cwd_starts_empty(self):
assert os.listdir(os.getcwd()) == []
with open("myfile", "w") as f:
f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []

****\*\*\*\*****\*\*****\*\*\*\*****\_\_****\*\*\*\*****\*\*****\*\*\*\***** PYTESTDOCS
https://docs.pytest.org/en/latest/monkeypatch.html

Monkeypatching/mocking modules and environments

2. Modifying the values of dictionaries e.g. you have a global
   configuration that you want to modify for certain test cases.
   Use monkeypatch.setitem() to patch the dictionary for the test.
   monkeypatch.delitem() can be used to remove items.

3. Use monkeypatch.syspath_prepend() to modify sys.path which will
   also call pkg_resources.fixup_namespace_packages() and importlib.
   invalidate_caches().

# import pytest
# from fs import path
# from fs.osfs import OSFS
# from pathlib import Path

# # NOTE: DUMMY NAMESPACE ONLY FOR MANUALLY COPYING AND PASTING


# class OEMODELL:

#     # User
#     TEST_USER = "GADMIN"
#     # Namespaces
#     TEST_PROJECT_NAME = "SC_OEMODELL_BENCHMARK"
#     TEST_PROJECT_DESCRIPTION = "This project simulates the austrian energy system (without cross-border flows) and compares the results of the dispat model with the OEMODELL simulation output. Simulation covers a full year in total, with a 15 minutes resolution (35 040‬ steps) on the dispat model and 60 minute resolution on the OEMODELL model. Both models take into account the same power plant setup, demand curves and VRES timeseries."

#     TEST_SC_NAME = "SC_ONLY_THERMAL"
#     TEST_SC_DESCRIPTION = "In this run we exclude all energy generation which comes from renewable sources (including hydro), and run only thermal power units"

#     TEST_SENSITIVITY_NAME = "SA_GAS_POWER_SWEEP"
#     TEST_SENSITIVITY_DESCRIPTION = "A sensitivity analysis in which the amount of power supplied from gas generators gets sweeped from 0% of total supply power to 100%, applying a 10% inclinement in each of the consecutive cases"

#     TEST_CASE_NAME = "CASE_3_GAS_POWER_SUPPLY_20_PERC"
#     TEST_CASE_DESCRIPTION = "In this case, we test a share of 20 % of total power supply provided gas generators."

#     # Pointer to working directory
#     WORKING_DIRECTORY = Path.cwd()

#     # ROOT and FS of test package
#     TESTS_ROOT = Path(__file__).parent.resolve()
#     TEST_FS = OSFS(str(TESTS_ROOT))

#     # ROOT and FS of src package
#     SRC_ROOT = Path("src/dispat").resolve()
#     SRC_FS = OSFS(str(SRC_ROOT))

#     # Filesystem for templates
#     SRC_TEMPLATES_FS = SRC_FS.opendir("filesystem/templates")


# class DUMMY:

#     # User
#     TEST_USER = "TEST_DUMMY"
#     # Namespaces
#     TEST_PROJECT_NAME = "SC_DUMMY_TEST"
#     TEST_PROJECT_DESCRIPTION = "This project simulates pure dumbness"

#     TEST_SC_NAME = "SC_ONLY_THE DUMBEST_UNITS"
#     TEST_SC_DESCRIPTION = "In this run we exclude all intelligence from our units and run them as dumb as possible"

#     TEST_SENSITIVITY_NAME = "SA_MAX_DUMBNESS_SWEEP"
#     TEST_SENSITIVITY_DESCRIPTION = "A sensitivity analysis in which the max amount of dumbness supplied from the dumbest units gets sweeped from 0 MegaFonzie to to 100 MegaFonzie total dumbness generation (we are even too dumb to use the right unit here, which actually is so dumb that it's cool again (~ 2-4 MegaFonzies))"

#     TEST_CASE_NAME = "CASE_555_MAX_DUMBNESS_20_MEGAFONZIE"
#     TEST_CASE_DESCRIPTION = "In this case, we test a share of 20 MegaFonzies"

#     # Pointer to working directory
#     WORKING_DIRECTORY = Path.cwd()

#     # ROOT and FS of test package
#     TESTS_ROOT = Path(__file__).parent.resolve()
#     TEST_FS = OSFS(str(TESTS_ROOT))

#     # ROOT and FS of src package
#     SRC_ROOT = Path("src/dispat").resolve()
#     SRC_FS = OSFS(str(SRC_ROOT))

#     # Filesystem for templates
#     SRC_TEMPLATES_FS = SRC_FS.opendir("filesystem/templates")


# class TWO_ZONES:

#     # User
#     TEST_USER = "WG"
#     # Namespaces
#     TEST_PROJECT_NAME = "SC_TWO_ZONES"
#     TEST_PROJECT_DESCRIPTION = "This project simulates the default two-zones test case, given by the dispaset model"

#     TEST_SC_NAME = "RUN_FULL_SETUP"
#     TEST_SC_DESCRIPTION = "In this run we include all settings as given by the default preset (within the provided excel file)"

#     TEST_SENSITIVITY_NAME = "SA_REPLACE_COAL_WITH_GAS_GENERATORS"
#     TEST_SENSITIVITY_DESCRIPTION = "A sensitivity analysis in which all coal generation units gets replaced by gas generators"

#     TEST_CASE_NAME = "CASE_01_REPLACE_HALF_OF_THE_UNITS"
#     TEST_CASE_DESCRIPTION = "In this case, we replace half of the units."

#     # Pointer to working directory
#     WORKING_DIRECTORY = Path.cwd()

#     # ROOT and FS of test package
#     TESTS_ROOT = Path(__file__).parent.resolve()
#     TEST_FS = OSFS(str(TESTS_ROOT))

#     # ROOT and FS of src package
#     SRC_ROOT = Path("src/dispat").resolve()
#     SRC_FS = OSFS(str(SRC_ROOT))

#     # Filesystem for templates
#     SRC_TEMPLATES_FS = SRC_FS.opendir("filesystem/templates")

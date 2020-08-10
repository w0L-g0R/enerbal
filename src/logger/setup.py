import logging
import logging.config
from typing import Optional

from .filters import (
    DebugFilter,
    InfoFilter,
    WarningFilter,
    CriticalFilter,
)

from .utils import (
    add_file_handler,
    change_logger_state,
)


# /////////////////////////////////////////////////////////////////// CONSTANTS

# ______________________________________________________________________ FORMAT

LOG_OUTPUT_STANDARD = "TIME: %(asctime)s | LOGGER: %(name)s [%(levelname)-s] {} @ %(filename)s -> def %(funcName)s:\n\n>>> %(message)s\n".format(
    "_" * 5
)

LOG_OUTPUT_STANDARD_NO_TIME = "| LOGGER: %(name)s [%(levelname)-s] {} @ %(filename)s -> def %(funcName)s:\n\n>>> %(message)s\n".format(
    "_" * 24
)

LOG_DATE_FORMAT = "% y/%m/%d %H:%M:%S"

# /////////////////////////////////////////////////////////////////// FUNCTIONS

# _______________________________________________________________________ SETUP


def setup_logging(
    # project_name: str,
    # scenario_name: str,
    console_log_filter: bool = False,
    console_log_actived: bool = True,
    console_out_level: str = logging.DEBUG,
    # dash_log_actived: bool = True,
    # built_logs_activated: bool = True,
    # GAMS_logs_activated: bool = True,
    # disable_all_logs: bool = False,
    # console_interface_log_filter: Union[None, logging.Filter],
    # build_file_logs_filter: Union[None, logging.Filter],
):
    """
    Creates a logging configuration and sets up different loggers and handlers
    """

    # ------------------------------------------------------------------- DICT

    _LOGCONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "debug_only": {"()": DebugFilter, },
            "info_only": {"()": InfoFilter, },
            "warning_only": {"()": WarningFilter, },
            "critical_only": {"()": CriticalFilter, },
        },
        "formatters": {
            "standard": {"format": LOG_OUTPUT_STANDARD, "datefmt": LOG_DATE_FORMAT},
            "notime": {
                "format": LOG_OUTPUT_STANDARD_NO_TIME,
                "datefmt": LOG_DATE_FORMAT,
            },
        },
        "handlers": {
            "null_out": {"class": "logging.NullHandler"},
            "console_out": {
                "class": "logger.colorstreamhandler.ColorStreamHandler",
                "stream": "ext://sys.stdout",
                # 'filters': ["last_part"],
                # "stream": "ext://sys.stdout",
                "level": console_out_level,
                "formatter": "notime",
            },
            # "gui_debug_out": {
            #     "class": "dispaset.misc.colorstreamhandler.ColorStreamHandler",
            #     "stream": "ext://sys.stderr",
            #     'filters': ["debug_only"],
            #     # "stream": "ext://sys.stdout",
            #     "level": "DEBUG",
            #     'formatter': 'notime',
            # },
            # "dash_html_out": {
            #     "class": "dispat.logger.setup.DashHandler",
            #     "stream": "sys.stdout",
            #     # 'filters': [],
            #     "level": "INFO",
            # },
            # "warning_html_out": {
            #     "class": "settings.DashHandler",
            #     "stream": "ext://sys.stderr",
            #     "level": "WARNING",
            # },
        },
        "root": {"level": "DEBUG", "handlers": [], },
        # "interface": {
        #     "level": "INFO",
        #     "handlers": ["info_html_out", "warning_html_out"],
        # },
    }

    # ----------------------------------------------------------------- DISABLE

    # if disable_all_logs:
    #     change_logger_state(disable_all=True)
    #     return

    # ------------------------------------------------------------ CONSOLE LOGS

    # MODEL (BUILT + GAMS)

    # if console_log_filter is not None:
    #     _LOGCONFIG["root"]["handlers"]["console_out"]["filter"].append(
    #         console_log_filter)

    if console_log_actived:
        _LOGCONFIG["root"]["handlers"].append("console_out")

    else:
        _LOGCONFIG["root"]["handlers"].append("null_out")

    # ---------------------------------------------------------- DASH LOGS

    # if dash_log_actived:
    # _LOGCONFIG["root"]["handlers"].append("dash_html_out")

    # else:
    #     _LOGCONFIG["root"]["handlers"].append("null_out")

    # if gui_debug_log_actived:
    #     _LOGCONFIG["interface"]["handlers"].append("gui_debug_out")

    # else:
    #     _LOGCONFIG["interface"]["handlers"].append("null")

    # -------------------------------------------------------- ACTIVATE CONFIG

    try:
        logging.config.dictConfig(_LOGCONFIG)
    except Exception:
        # if it didn't work, it might be due to ipython messing with the output
        # typical error: Unable to configure handler 'console': IOStream has no fileno
        # try without console output:
        print(
            "WARNING: the colored console output is failing (possibly because of ipython). Switching to monochromatic output"
        )
        _LOGCONFIG["handlers"]["console_out"]["class"] = "logging.StreamHandler"
        logging.config.dictConfig(_LOGCONFIG)

    # ----------------------------------------------------------- FILE HANDLERS

    # if built_logs_activated:
    #     # Create a folder
    #     create_folder(
    #         _type=logging.FileHandler,
    #         scenario_name=scenario_name,
    #         run_name=run_name,
    #     )
    # Add a file handler
    # add_file_handler(
    #     _type=logging.FileHandler,
    #     # filename=,
    #     level=logging.INFO,
    # )

    return

import functools
import logging
import sys
from logging import FileHandler
from logging.handlers import RotatingFileHandler
from pprint import pprint
from typing import Union


class RootLogger(object):

    """A tiny python root log decorator

    .. seealso::
    https://dev.to/mandrewcito/a-tiny-python-log-decorator-1o5m

    """

    def __init__(self, _type):
        self.logger = logging.getLogger(_type)

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                self.logger.debug("{0} - {1} - {2}".format(fn.__name__, args, kwargs))
                logger_msg = fn(*args, **kwargs)
                self.logger.debug(result)
                return logger_msg
            except Exception as e:
                self.logger.debug("Exception {0}".format(e))
                raise e
            return logger_msg

        return decorated


# /////////////////////////////////////////////////////////////////// FUNCTIONS

# ________________________________________________________________ SHOW_LOGGERS


def show_loggers():
    """
    Returns a pretty-printed list of all logger that get found
    """
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    return pprint("Loggers found: ", loggers)


# _______________________________________________________________ SHOW_HANDLERS


def show_handlers(logger_name: str = ""):
    """Returns a pretty-printed list of all handlers for a single logger or all available loggers that get found

    If no logger_name gets passed, the function shows the handlers for the root logger. If "all_loggers" gets passed the function iters over all loggers and shows the available handlers
    """
    if "all" in logger_name:

        for k, v in logging.Logger.manager.loggerDict.items():
            pprint("+ [%s] {%s} " % (str.ljust(k, 40), str(v.__class__)[8:-2]))
            if not isinstance(v, logging.PlaceHolder):
                for h in v.handlers:
                    print("'+ |{}> {}".format("-" * 16, str(h.__class__)[8:-2]))

    else:
        handlers = [handler for handler in logging.getLogger(logger_name).handlers]
        return pprint("Handlers found: ", handlers)


# ____________________________________________________________ ADD_FILE_HANDLER


def add_file_handler(
    _type: Union[FileHandler, RotatingFileHandler],
    filename: str,
    level: str = logging.INFO,
    _filter: logging.Filter = None,
    logger_name: str = "",
    maxBytes: int = 20000,
    backupCount: int = 10,
):
    """Adds a specific type of file handler to a logger. Could either be a normal FileHandler or a RotatingFileHandler"""

    if isinstance(obj=_type, class_or_tuple=FileHandler):

        handler = FileHandler(filename=filename)
    else:

        handler = RotatingFileHandler(filename=filename, maxBytes=2000, backupCount=10)

    handler.setLevel(level)

    if _filter is not None:
        handler.addFilter(_filter)

    logging.getLogger(logger_name).addHandler(handler)

    return


# ______________________________________________________________ REMOVE_HANDLER


def remove_handler():
    pass


# ________________________________________________________________ CHANGE_STATE


def change_logger_state(logger_name: str = None, disable_all: bool = False):

    # Option 1) Disable all loggers
    if disable_all:
        return logging.disable(sys.maxsize)

    # Option 2) Enable/Disable a specific logger by name
    if logger_name is not None:

        current_state = logging.getLogger(logger_name).disabled

        print('BEFORE: Logger "{}" disabled: {}'.format(logger_name, current_state))

        # Logger is currently disabled
        if current_state:

            current_state = False
            return

        else:
            current_state = True
            return

        print('AFTER: Logger "{}" disabled: {}'.format(logger_name, current_state))


# _______________

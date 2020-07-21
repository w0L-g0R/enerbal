import logging

# ///////////////////////////////////////////////////////////////////// CLASSES


class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


class NotDebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


class WarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR


class CriticalFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.CRITICAL

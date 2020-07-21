
import platform
import logging

# ///////////////////////////////////////////////////////////////////// CLASSES


class DashHandler(logging.StreamHandler):
    '''
    Saves logger streams temporarily, in order to display them in the GUI
    '''

    def __init__(self, stream=None):
        super().__init__(stream=stream)
        self.logs = list()

    def emit(self, record):
        try:
            msg = self.format(record)
            self.logs.append(msg)
            self.logs = self.logs[-1000:]
            self.flush()
        except Exception:
            self.handleError(record)

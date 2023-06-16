import logging
import sys


class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler("error.log")
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_exception(self, exc_type, exc_value, exc_traceback):
        self.logger.error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )


def log_uncaught_exceptions():
    error_handler = ErrorHandler()
    sys.excepthook = error_handler.log_exception

# -*- coding: utf-8 -*-
import logging
import traceback
from functools import wraps


def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"An exception occurred in {func.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            raise

    return wrapper


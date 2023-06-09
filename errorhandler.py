# -*- coding: utf-8 -*-

import functools
import traceback
import logging

def handle_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"An exception occurred in {func.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            raise
    return wrapper


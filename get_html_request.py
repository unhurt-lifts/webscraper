# -*- coding: utf-8 -*-

import requests
from errorhandler import handle_exception

@handle_exception
def get_html_code(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# -*- coding: utf-8 -*-

import requests
import logging
from errorhandler import handle_exception

logging.basicConfig(filename="error.log", level=logging.ERROR)


@handle_exception
def get_html_code(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    try:
        url = input("Enter the URL: ")
        html_code = get_html_code(url)
        print(html_code)
    except Exception as e:
        print(f"Failed to get HTML code:\n{str(e)}")
        logging.error(f"An exception occurred in get_html_code: {str(e)}")

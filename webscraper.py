import requests
import pandas as pd
from bs4 import BeautifulSoup
from errorhandler import handle_exception


class WebScraper:
    def __init__(self):
        self.data = []

    @staticmethod
    @handle_exception
    def is_valid_url(url):
        # Check if the URL is valid
        return requests.get(url).ok

    @staticmethod
    @handle_exception
    def fetch_html(url):
        # Fetch HTML code from the provided URL
        response = requests.get(url)
        return response.text

    @handle_exception
    def scrape_data_from_elements(self, html_code, elements):
        # Parse the HTML code
        soup = BeautifulSoup(html_code, "html.parser")

        # Scrape data from selected elements
        for element in elements:
            tag, attrs = self.parse_element(element)
            elements = soup.find_all(tag, attrs=attrs)
            data = [self.get_element_data(e) for e in elements]
            self.data.extend(data)

    @staticmethod
    def parse_element(element):
        # Parse the element string into tag and attributes
        parts = element.split(" ")
        tag = parts[0]
        attrs = {}
        for attr in parts[1:]:
            attr_parts = attr.split("=")
            key = attr_parts[0]
            value = attr_parts[1].strip('"') if len(attr_parts) > 1 else ""
            attrs[key] = value
        return tag, attrs


    @staticmethod
    def get_element_data(element):
        # Get data from the element
        tag = element.name
        text = element.text.strip()
        attrs = element.attrs
        return {"tag": tag, "text": text, "attrs": attrs}

    def create_dataframe(self):
        # Create a pandas DataFrame from the scraped data
        return pd.DataFrame(self.data)

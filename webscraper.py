import requests
import pandas as pd
from bs4 import BeautifulSoup
from errorhandler import handle_exception


class WebScraper:
    def __init__(self):
        self.data = []

    @handle_exception
    def is_valid_url(self, url):
        return requests.get(url).ok

    @handle_exception
    def fetch_html(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @handle_exception
    def scrape_data_from_elements(self, html_code, elements):
        soup = BeautifulSoup(html_code, "html.parser")

        for element in elements:
            tag, attrs = self.parse_element(element)
            elements = soup.find_all(tag, attrs=attrs)
            data = [self.get_element_data(e) for e in elements]
            self.data.extend(data)

    @staticmethod
    def parse_element(element):
        parts = element.split(" ")
        tag = parts[0]
        attrs = {}
        for attr in parts[1:]:
            attr_parts = attr.split("=")
            if len(attr_parts) >= 2:
                key = attr_parts[0]
                value = attr_parts[1].strip("'\"")
                attrs[key] = value
        return tag, attrs

    @staticmethod
    def get_element_data(element):
        return element.text.strip()

    def create_dataframe(self):
        df = pd.DataFrame(data=self.data, columns=["Scraped Data"])
        return df

    @staticmethod
    def save_to_excel(data_frame, filename):
        data_frame.to_excel(filename, index=False)

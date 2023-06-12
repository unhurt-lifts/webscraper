import requests
import pandas as pd
import logging
from errorhandler import handle_exception
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import certifi
import requests

logging.basicConfig(filename="error.log", level=logging.ERROR)


class WebScraper:
    @handle_exception
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception as e:
            raise Exception(f"Error validating URL: {str(e)}")

    @handle_exception
    def fetch_html(self, url):
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise Exception(f"Invalid URL: {url}")
            response = requests.get(url, verify=certifi.where())
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching HTML: {str(e)}")



    @handle_exception
    def scrape_data_from_elements(self, urls, elements):
        try:
            scraped_data = []

            for url in urls:
                html_content = self.fetch_html(url)

                # Scenario: Parsing HTML and scraping data from selected elements
                soup = BeautifulSoup(html_content, "html.parser")
                for element in elements:
                    # Find and extract the desired data from the selected element
                    data = soup.select_one(element).text
                    scraped_data.append(data)

            # Store the scraped data
            self.data = scraped_data
            print(self.data)
        except Exception as e:
            raise Exception(f"Error scraping data from elements: {str(e)}")

    @handle_exception
    def create_dataframe(self):
        try:
            # Scenario: Creating a pandas DataFrame from scraped data
            data_frame = pd.DataFrame({"Scraped Data": self.data})
            return data_frame

        except Exception as e:
            raise Exception(f"Error creating DataFrame: {str(e)}")

    @handle_exception
    def save_to_excel(self, filename):
        try:
            # Scenario: Saving the DataFrame to an Excel file
            data_frame = self.create_dataframe()
            data_frame.to_excel(filename, index=False)

        except Exception as e:
            raise Exception(f"Error saving to Excel: {str(e)}")

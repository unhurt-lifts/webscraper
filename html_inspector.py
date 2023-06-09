# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging
from errorhandler import handle_exception

logging.basicConfig(filename="error.log", level=logging.ERROR)


class HTMLInspector:
    @handle_exception
    def parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Scenario: Parsing HTML and returning selected elements
            selected_elements = soup.find_all()  # Replace with specific logic
            
            return selected_elements

        except Exception as e:
            raise Exception(f"Error parsing HTML: {str(e)}")

    @handle_exception
    def select_elements(self):
        try:
            elements = {}
            
            # Scenario: Selecting HTML elements
            while True:
                element_name = input("Enter the HTML element name (e.g., div, p): ")
                if not element_name:
                    break
                
                element_properties = input("Enter additional properties (e.g., class, id): ")
                element_properties = element_properties.split(",")
                
                element = {
                    "name": element_name,
                    "properties": element_properties
                }
                
                elements[element_name] = element

            return elements

        except Exception as e:
            raise Exception(f"Error selecting elements: {str(e)}")

    @handle_exception
    def is_valid_html(self, html_content):
        try:
            # Scenario: Validating HTML code
            soup = BeautifulSoup(html_content, "html.parser")
            return soup is not None

        except Exception as e:
            raise Exception(f"Error validating HTML: {str(e)}")

    @handle_exception
    def get_selected_elements(self, html_content, selector):
        try:
            # Scenario: Getting selected elements based on a selector
            soup = BeautifulSoup(html_content, "html.parser")
            selected_elements = soup.select(selector)
            
            return selected_elements

        except Exception as e:
            raise Exception(f"Error getting selected elements: {str(e)}")

# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import logging
from errorhandler import handle_exception


logging.basicConfig(filename="error.log", level=logging.ERROR)


class HTMLInspector:
    def __init__(self):
        self.selected_elements = []

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
            selected_elements = self.open_element_selection(html_content)

            return selected_elements

        except Exception as e:
            raise Exception(f"Error getting selected elements: {str(e)}")

    @handle_exception
    def open_element_selection(self, html_content):
        try:
            element_selection_window = tk.Toplevel()
            element_selection_window.title("Select HTML Elements")

            elements_frame = ttk.Frame(element_selection_window)
            elements_frame.pack(pady=10)

            elements_label = ttk.Label(elements_frame, text="Select HTML Elements:")
            elements_label.pack(side=tk.LEFT)

            elements_listbox = tk.Listbox(elements_frame, selectmode=tk.MULTIPLE, width=50, height=10)
            elements_listbox.pack(side=tk.LEFT)

            # Parse the HTML content and retrieve the elements
            soup = BeautifulSoup(html_content, "html.parser")
            elements = soup.find_all()
            for element in elements:
                tag = element.name
                attributes = [(attr, value) for attr, value in element.attrs.items()]
                tag_with_attributes = tag + " " + " ".join([f"{attr}={value}" for attr, value in attributes])
                elements_listbox.insert(tk.END, tag_with_attributes)

            def get_selected_elements():
                selected_indices = elements_listbox.curselection()
                self.selected_elements = [elements_listbox.get(idx) for idx in selected_indices]
                element_selection_window.destroy()

            select_button = ttk.Button(element_selection_window, text="Select", command=get_selected_elements)
            select_button.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening element selection: {str(e)}")
            logging.error(f"An exception occurred in open_element_selection: {str(e)}")

        return self.selected_elements


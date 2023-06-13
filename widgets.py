import tkinter as tk
from tkinter import ttk, scrolledtext
from bs4 import BeautifulSoup
import pandas as pd
from pandastable import Table
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox


class WidgetCreator:
    def __init__(self, root):
        self.root = root
        self.url_entry = None
        self.html_text = None
        self.elements_listbox = None
        self.html_elements = None
        self.selected_elements_text = None
        self.scrape_button = None
        self.back_button = None

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_url_input(self, callback):
        label = ttk.Label(self.root, text="Enter URL:")
        label.pack()

        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack()

        button = ttk.Button(self.root, text="Submit", command=callback)
        button.pack()

    def create_html_input(self, html_code, callback):
        label = ttk.Label(self.root, text="HTML Code:")
        label.pack()

        self.html_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10)
        self.html_text.insert(tk.END, html_code)
        self.html_text.pack()

        button = ttk.Button(self.root, text="Next", command=callback)
        button.pack()

    def open_element_selection(self, html_code):
        label = ttk.Label(self.root, text="HTML Elements:")
        label.pack()

        self.html_elements = self.get_html_elements(html_code)

        self.elements_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        for element in self.html_elements:
            self.elements_listbox.insert(tk.END, element)
        self.elements_listbox.pack()

    def get_html_elements(self, html_code):
        soup = BeautifulSoup(html_code, "html.parser")
        elements = []

        for tag in soup.find_all():
            elements.append(tag.name)

        return sorted(set(elements))

    def create_next_button(self, callback):
        button = ttk.Button(self.root, text="Next", command=callback)
        button.pack()

    def create_back_button(self, callback):
        button = ttk.Button(self.root, text="Back", command=callback)
        button.pack()

    def show_selected_elements(self, selected_elements):
        label = ttk.Label(self.root, text="Selected Elements:")
        label.pack()

        self.selected_elements_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=5)
        self.selected_elements_text.insert(tk.END, "\n".join(selected_elements))
        self.selected_elements_text.pack()

    def create_scrape_button(self, callback):
        self.scrape_button = ttk.Button(self.root, text="Scrape", command=callback)
        self.scrape_button.pack()

    def display_dataframe(self, data_frame):
        frame = tk.Frame(self.root)
        frame.pack()

        table = Table(frame, dataframe=data_frame, showtoolbar=True, showstatusbar=True)
        table.show()

    def create_back_button(self, callback):
        self.back_button = ttk.Button(self.root, text="Back", command=callback)
        self.back_button.pack()

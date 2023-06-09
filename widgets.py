# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, filedialog
from pandastable import Table


class PandasTable(Table):
    def __init__(self, parent=None, **kwargs):
        Table.__init__(self, parent, **kwargs)
        self.show()


class WidgetCreator:
    def __init__(self, root):
        self.root = root

    def create_url_input(self, get_html_code_callback):
        url_label = tk.Label(self.root, text="URL:")
        url_label.pack()

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()

        get_html_button = tk.Button(self.root, text="Get HTML", command=lambda: get_html_code_callback())
        get_html_button.pack()

    def create_html_input(self):
        html_label = tk.Label(self.root, text="HTML Code:")
        html_label.pack()

        self.html_entry = tk.Text(self.root, height=10, width=50)
        self.html_entry.pack()

    def create_selector_input(self):
        selector_label = tk.Label(self.root, text="CSS Selector:")
        selector_label.pack()

        self.selector_entry = tk.Entry(self.root)
        self.selector_entry.pack()

    def create_scrape_button(self, start_scraping_callback):
        scrape_button = tk.Button(self.root, text="Start Scraping", command=start_scraping_callback)
        scrape_button.pack()

    def create_clear_button(self, clear_html_code_callback):
        clear_button = tk.Button(self.root, text="Clear HTML", command=clear_html_code_callback)
        clear_button.pack()

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def show_info_message(self, message):
        messagebox.showinfo("Information", message)

    def show_warning_message(self, message):
        messagebox.showwarning("Warning", message)

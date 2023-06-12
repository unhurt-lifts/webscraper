import tkinter as tk
from tkinter import ttk
import pandas as pd
from bs4 import BeautifulSoup


class PandasTable(ttk.Frame):
    def __init__(self, parent, dataframe):
        ttk.Frame.__init__(self, parent)

        # Create a Treeview widget
        self.treeview = ttk.Treeview(self, columns=list(dataframe.columns), show="headings")
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure Treeview column headings
        for column in dataframe.columns:
            self.treeview.heading(column, text=column)

        # Add data rows to Treeview
        for row in dataframe.itertuples(index=False):
            self.treeview.insert("", tk.END, values=row)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


class WidgetCreator:
    def __init__(self, root):
        self.root = root
        self.url_entry = None
        self.html_entry = None
        self.next_button = None

    def create_url_input(self, get_html_code):
        label = ttk.Label(self.root, text="URL:")
        label.pack()

        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack()

        button = ttk.Button(self.root, text="Get Html", command=get_html_code)
        button.pack()

    def create_html_input(self, html_code):
        label = ttk.Label(self.root, text="HTML Code:")
        label.pack()

        self.html_entry = tk.Text(self.root, height=10)
        self.html_entry.pack()
        self.html_entry.insert(tk.END, html_code)

    def create_next_button(self, start_scraping):
        self.next_button = ttk.Button(self.root, text="Select", command=start_scraping)
        self.next_button.pack()

    def open_element_selection(self, html_content, get_selected_elements):
        element_selection_window = tk.Toplevel(self.root)
        element_selection_window.title("Select HTML Elements")
    
        elements_frame = ttk.Frame(element_selection_window)
        elements_frame.pack(pady=10)
    
        elements_label = ttk.Label(elements_frame, text="Select HTML Elements:")
        elements_label.pack(side=tk.LEFT)
    
        elements_listbox = tk.Listbox(elements_frame, selectmode=tk.MULTIPLE, width=50, height=50)
        elements_listbox.pack(side=tk.LEFT)
    
        # Parse the HTML content and retrieve the elements
        soup = BeautifulSoup(html_content, "html.parser")
        elements = soup.find_all()
        for element in elements:
            tag = element.name
            attributes = [(attr, value) for attr, value in element.attrs.items()]
            tag_with_attributes = tag + " " + " ".join([f"{attr}={value}" for attr, value in attributes])
            elements_listbox.insert(tk.END, tag_with_attributes)
    
        select_button = ttk.Button(element_selection_window, text="Select", command=lambda: get_selected_elements(elements_listbox))
        select_button.pack(pady=10)


    def display_dataframe(self, dataframe):
        table_window = tk.Toplevel(self.root)
        table_window.title("Scraped Data")

        table_frame = ttk.Frame(table_window)
        table_frame.pack(pady=10)

        table = PandasTable(table_frame, dataframe)
        table.pack()

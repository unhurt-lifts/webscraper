import tkinter as tk
from tkinter import ttk
from pandastable import Table
from bs4 import BeautifulSoup


class WidgetCreator:
    def __init__(self, root):
        self.root = root
        self.url_entry = None
        self.html_entry = None
        self.elements_listbox = None

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_url_input(self, get_html_code):
        self.clear_widgets()

        label = ttk.Label(self.root, text="URL:")
        label.pack()

        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack()

        button = ttk.Button(self.root, text="Get HTML", command=get_html_code)
        button.pack()

    def create_html_input(self, html_code):
        self.clear_widgets()

        label = ttk.Label(self.root, text="HTML Code:")
        label.pack()

        self.html_entry = tk.Text(self.root, height=10)
        self.html_entry.pack()
        self.html_entry.insert(tk.END, html_code)

    def open_element_selection(self, html_content, callback):
        self.clear_widgets()

        element_selection_window = tk.Toplevel(self.root)
        element_selection_window.title("Select HTML Elements")

        elements_frame = ttk.Frame(element_selection_window)
        elements_frame.pack(pady=10)

        elements_label = ttk.Label(elements_frame, text="Select HTML Elements:")
        elements_label.pack(side=tk.LEFT)

        self.elements_listbox = tk.Listbox(elements_frame, selectmode=tk.MULTIPLE, width=80, height=30)
        self.elements_listbox.pack(side=tk.LEFT)

        # Parse the HTML content and retrieve the elements
        soup = BeautifulSoup(html_content, "html.parser")
        elements = soup.find_all()
        for element in elements:
            tag = element.name
            attributes = [(attr, value) for attr, value in element.attrs.items()]
            tag_with_attributes = tag + " " + " ".join([f"{attr}={value}" for attr, value in attributes])
            self.elements_listbox.insert(tk.END, tag_with_attributes)

        select_button = ttk.Button(
            element_selection_window, text="Select", command=lambda: callback(self.elements_listbox)
        )
        select_button.pack(pady=10)

    def display_dataframe(self, dataframe):
        self.clear_widgets()

        table_window = tk.Toplevel(self.root)
        table_window.title("Scraped Data")

        table_frame = ttk.Frame(table_window)
        table_frame.pack(pady=10)

        table = Table(table_frame, dataframe=dataframe)
        table.show()

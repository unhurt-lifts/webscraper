# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, filedialog
from widgets import WidgetCreator, PandasTable
from html_inspector import HTMLInspector
from webscraper import WebScraper
from errorhandler import handle_exception
from get_html_request import get_html_code


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Scraper")
        self.widget_creator = WidgetCreator(self.root)
        self.urls = []
        self.html_code = ""

    def create_widgets(self):
        self.widget_creator.create_url_input(self.get_html_code)
        self.widget_creator.create_html_input()
        self.widget_creator.create_selector_input()
        self.widget_creator.create_scrape_button(self.start_scraping)

        self.root.mainloop()

    @handle_exception
    def get_html_code(self):
        # Get the URL from the entry
        url = self.widget_creator.url_entry.get().strip()

        # Validate the URL
        if not url:
            messagebox.showwarning("Empty URL", "Please enter a URL.")
            return

        try:
            self.html_code = get_html_code(url)
            self.widget_creator.html_entry.delete("1.0", tk.END)
            self.widget_creator.html_entry.insert(tk.END, self.html_code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get HTML code:\n{str(e)}")


    @handle_exception
    def start_scraping(self):
        # Get the URLs from the entry
        urls_text = self.widget_creator.url_entry.get().strip()
        self.urls = urls_text.splitlines()

        # Get the HTML code from the entry
        self.html_code = self.widget_creator.html_entry.get("1.0", tk.END)

        # Get the selector from the entry
        selector = self.widget_creator.selector_entry.get().strip()

        # Create an HTMLInspector object
        inspector = HTMLInspector()

        # Validate the HTML code
        if not inspector.is_valid_html(self.html_code):
            messagebox.showwarning("Invalid HTML", "The entered HTML code is invalid.")
            return

        # Create a WebScraper object
        scraper = WebScraper()

        # Scrape data from the URLs and HTML code
        for url in self.urls:
            if not scraper.is_valid_url(url):
                messagebox.showwarning("Invalid URL", f"The URL '{url}' is invalid.")
                return

        selected_elements = inspector.get_selected_elements(self.html_code, selector)
        scraper.scrape_data_from_elements(self.urls, selected_elements)

        # Create a DataFrame
        data_frame = scraper.create_dataframe()

        # Save the DataFrame to an Excel file
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel File", "*.xlsx")])
        if filename:
            scraper.save_to_excel(filename)

        # Show the DataFrame
        self.show_dataframe(data_frame)

    def show_dataframe(self, data_frame):
        # Create a new window to display the DataFrame
        window = tk.Toplevel(self.root)
        window.title("Scraped Data")

        # Create a PandasTable widget to show the DataFrame
        table = PandasTable(window, dataframe=data_frame)
        table.pack(fill=tk.BOTH, expand=True)

        # Add a close button
        close_button = tk.Button(window, text="Close", command=window.destroy)
        close_button.pack()

    def clear_html_code(self):
        self.widget_creator.html_entry.delete(1.0, tk.END)

    def run(self):
        self.create_widgets()


if __name__ == "__main__":
    app = App()
    app.run()


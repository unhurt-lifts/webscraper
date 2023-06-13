import tkinter as tk
from tkinter import messagebox
from webscraper import WebScraper
from widgets import WidgetCreator
from errorhandler import handle_exception


class App:
    def __init__(self, root):
        self.root = root
        self.scraper = WebScraper()
        self.widgets = WidgetCreator(self.root)
        self.html_code = ""
        self.selected_elements = []

        self.create_url_input()

    @handle_exception
    def create_url_input(self):
        self.widgets.clear_widgets()
        self.widgets.create_url_input(self.get_html_code)

    @handle_exception
    def get_html_code(self):
        url = self.widgets.url_entry.get()

        if not self.scraper.is_valid_url(url):
            messagebox.showerror("Error", "Invalid URL")
            return

        try:
            html_code = self.scraper.fetch_html(url)
            self.html_code = html_code
            self.widgets.create_html_input(html_code, self.open_html_selection)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @handle_exception
    def open_html_selection(self):
        self.widgets.clear_widgets()
        self.widgets.open_element_selection(self.html_code)
        self.widgets.create_next_button(self.get_selected_elements)
        self.widgets.create_back_button(self.create_url_input)

    @handle_exception
    def get_selected_elements(self):
        selected_indices = self.widgets.elements_listbox.curselection()
        self.selected_elements = [self.widgets.elements_listbox.get(index) for index in selected_indices]
        self.show_selected_elements()

    @handle_exception
    def show_selected_elements(self):
        self.widgets.clear_widgets()
        self.widgets.show_selected_elements(self.selected_elements)
        self.widgets.create_scrape_button(self.start_scraping)
        self.widgets.create_back_button(self.open_html_selection)

    @handle_exception
    def start_scraping(self):
        # Scrape data from selected elements
        self.scraper.scrape_data_from_elements(self.html_code, self.selected_elements)

        # Create a pandas DataFrame
        data_frame = self.scraper.create_dataframe()

        # Display the DataFrame in a table
        self.widgets.display_dataframe(data_frame)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Web Scraper")
    app = App(root)
    app.run()

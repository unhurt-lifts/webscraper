import tkinter as tk
from tkinter import messagebox
from webscraper import WebScraper
from widgets import WidgetCreator
from errorhandler import handle_exception


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Scraper")
        self.scraper = WebScraper()
        self.widget_creator = WidgetCreator(self.root)
        self.html_code = None

    @handle_exception
    def run(self):
        self.get_url_input()

    def get_url_input(self):
        self.widget_creator.clear_widgets()
        self.widget_creator.create_url_input(self.process_url_input)

    @handle_exception
    def process_url_input(self):
        url = self.widget_creator.url_entry.get()
        if self.scraper.is_valid_url(url):
            self.html_code = self.scraper.fetch_html(url)
            self.open_element_selection()
        else:
            messagebox.showerror("Invalid URL", "Please enter a valid URL.")

    def open_element_selection(self):
        self.widget_creator.clear_widgets()
        self.widget_creator.open_element_selection(self.html_code, self.get_selected_elements)

    def get_selected_elements(self, elements_listbox):
        selected_indices = elements_listbox.curselection()
        selected_elements = [elements_listbox.get(index) for index in selected_indices]

        self.scraper.scrape_data_from_elements(self.html_code, selected_elements)
        df = self.scraper.create_dataframe()

        # Display the scraped data in a new window
        self.widget_creator.display_dataframe(df)

        # Save the scraped data to Excel
        self.scraper.save_to_excel(df, "scraped_data.xlsx")

        messagebox.showinfo("Scraping", "Data scraping completed and saved to 'scraped_data.xlsx'!")


if __name__ == "__main__":
    app = App()
    app.run()
    app.root.mainloop()

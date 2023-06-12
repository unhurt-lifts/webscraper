import tkinter as tk
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
from webscraper import WebScraper
from widgets import WidgetCreator
from errorhandler import handle_exception


class App:
    def __init__(self, root):
        self.root = root
        self.scraper = WebScraper()
        self.widgets = WidgetCreator(self.root)
        self.html_code = ""

        self.create_url_input()

    @handle_exception
    def create_url_input(self):
        label = ttk.Label(self.root, text="URL:")
        label.pack()

        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack()

        button = ttk.Button(self.root, text="Get HTML", command=self.get_html_code)
        button.pack()

    @handle_exception
    def get_html_code(self):
        url = self.url_entry.get()

        if not self.scraper.is_valid_url(url):
            messagebox.showerror("Error", "Invalid URL")
            return

        self.url_entry.config(state="disabled")

        try:
            html_code = self.scraper.fetch_html(url)
            self.html_code = html_code
            self.open_html_selection()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @handle_exception
    def open_html_selection(self):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select HTML Elements")

        label = ttk.Label(selection_window, text="HTML Elements for your url:")
        label.pack()

        elements_listbox = tk.Listbox(selection_window, selectmode=tk.MULTIPLE, width=50, height=20)
        elements_listbox.pack()

        # Parse the HTML code and retrieve the elements
        soup = BeautifulSoup(self.html_code, "html.parser")
        elements = soup.find_all()
        for element in elements:
            tag = element.name
            attributes = [(attr, value) for attr, value in element.attrs.items()]
            tag_with_attributes = tag + " " + " ".join([f"{attr}={value}" for attr, value in attributes])
            elements_listbox.insert(tk.END, tag_with_attributes)

        next_button = ttk.Button(selection_window, text="Next", command=lambda: self.get_selected_elements(selection_window, elements_listbox))
        next_button.pack(pady=10)

    @handle_exception
    def get_selected_elements(self, selection_window, listbox):
        selected_indices = listbox.curselection()
        selected_elements = [listbox.get(index) for index in selected_indices]

        selection_window.destroy()
        self.show_selected_elements(selected_elements)

    @handle_exception
    def show_selected_elements(self, selected_elements):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Selected Items")

        label = ttk.Label(selection_window, text="Selected Elements:")
        label.pack()

        elements_listbox = tk.Listbox(selection_window, selectmode=tk.MULTIPLE, width=50, height=20)
        elements_listbox.pack()

        for element in selected_elements:
            elements_listbox.insert(tk.END, element)

        scrape_button = ttk.Button(selection_window, text="Scrape", command=lambda: self.start_scraping(selected_elements))
        scrape_button.pack(pady=10)

    @handle_exception
    def start_scraping(self, selected_elements):
        # Scrape data from selected elements
        self.scraper.scrape_data_from_elements(self.html_code, selected_elements)

        # Create a pandas DataFrame
        data_frame = self.scraper.create_dataframe()

        # Display the DataFrame in a table
        self.widgets.display_dataframe(data_frame)

    @handle_exception
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Web Scraper")
    app = App(root)
    app.run()

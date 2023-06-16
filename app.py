from tkinter import Tk, Button, Entry, messagebox, Toplevel, Listbox, Scrollbar, Label, END
from widgets import HTMLCodeScrolledText
from webscraper import Webscraper
from errorhandler import ErrorHandler
from errorhandler import log_uncaught_exceptions

import sys

class App:
    def __init__(self, root):
        self.root = root
        self.url_input = None
        self.process_button = None
        self.webscraper = Webscraper()
        self.error_handler = ErrorHandler()

    def create_widgets(self):
        self.root.title("Web Scraper")

        # URL Label and Input
        url_label = Label(self.root, text="URL:")
        url_label.pack(anchor='w', pady=5)

        self.url_input = Entry(self.root, width=50)
        self.url_input.pack(anchor='w')

        # Process Button
        self.process_button = Button(self.root, text="Process", command=self.process_url_input)
        self.process_button.pack(side='left', padx=10, pady=10)

        # Close Button
        close_button = Button(self.root, text="Close", command=self.root.quit)
        close_button.pack(side='right', padx=10, pady=10)

        # URL Format Label
        url_format_label = Label(self.root, text="URL Format: https://www.example.com")
        url_format_label.pack(anchor='w', pady=5)

    def process_url_input(self):
        url = self.url_input.get()
        try:
            if self.webscraper.validate_url(url):
                html_code = self.webscraper.get_html_code(url)
                self.show_html_code(html_code)
            else:
                messagebox.showerror("Invalid URL", "Please enter a valid URL.")
        except Exception as e:
            # Log uncaught exception
            self.error_handler.log_exception(*sys.exc_info())
            # Display error message to the user
            messagebox.showerror("Error", "An error occurred. Please check the log file for details.")

    def show_html_code(self, html_code):
        html_window = Toplevel(self.root)
        html_window.title("HTML Code")

        html_scrolled_text = HTMLCodeScrolledText(html_window)
        html_scrolled_text.pack(fill='both', expand=True)
        html_scrolled_text.show_html_code(html_code)

        # Select Button
        select_button = Button(html_window, text="Select", command=self.open_element_selection)
        select_button.pack(side='left', padx=10, pady=10)

        # Back Button
        back_button = Button(html_window, text="Back", command=self.root.deiconify)
        back_button.pack(side='right', padx=10, pady=10)

    def open_element_selection(self):
        elements_window = Toplevel(self.root)
        elements_window.title("Select Elements")

        elements_listbox = Listbox(elements_window, selectmode='multiple', width=80, height=20)
        elements_listbox.pack(side='left', padx=10, pady=10)

        scrollbar = Scrollbar(elements_window, command=elements_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        elements_listbox.config(yscrollcommand=scrollbar.set)

        # Add elements to the listbox
        elements = self.webscraper.get_elements()
        for element in elements:
            elements_listbox.insert(END, element)

        # Back Button
        back_button = Button(elements_window, text="Back", command=elements_window.destroy)
        back_button.pack(pady=10)

        # Select Button
        select_button = Button(elements_window, text="Select", command=self.process_selected_elements)
        select_button.pack(pady=10)

    def process_selected_elements(self):
        # Get the selected elements from the listbox
        elements_window = self.root.focus_get().master
        elements_listbox = elements_window.children['!listbox']
        selected_indices = elements_listbox.curselection()
        selected_elements = [elements_listbox.get(index) for index in selected_indices]
        
        import pdb; pdb.set_trace()
        # Pass the selected elements to the scraper for further processing
        scraped_data = self.webscraper.scrape_data(selected_elements)
    
        # Perform desired logic with the scraped data
        for data in scraped_data:
            tag = data["tag"]
            attributes = data.get("attributes", {})
            attribute_count = data.get("attribute_count", 0)
            element_data = f"Tag: {tag} | Attributes: {attributes} | Attribute Count: {attribute_count}"
            print(element_data)
    
        # Close the elements window
        elements_window.destroy()


if __name__ == "__main__":
    log_uncaught_exceptions()
    root = Tk()

    app = App(root)
    app.create_widgets()

    root.mainloop()

from tkinter import Tk, Button, Entry, messagebox, Toplevel, Listbox, Scrollbar, Label, END
from widgets import HTMLCodeScrolledText
from webscraper import Webscraper
from errorhandler import ErrorHandler
from errorhandler import log_uncaught_exceptions
from widgets import ScrapedDataWindow
import tkinter.filedialog as filedialog

import pandas as pd
from pandastable import Table
import tkinter.filedialog as tkFileDialog
from tkinter import Frame, Canvas, Scrollbar

import sys

class ScrolledTable(Frame):
    def __init__(self, parent, dataframe, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(self, borderwidth=0)
        self.table = Table(self.canvas, dataframe=dataframe)
        self.table.show()

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.table, anchor="nw")

        self.table.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.update_canvas)

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_canvas(self, event):
        self.canvas.itemconfigure(self.table, width=event.width)


class App:
    def __init__(self, root):
        self.root = root
        self.url_input = None
        self.process_button = None
        self.webscraper = Webscraper()
        self.error_handler = ErrorHandler()
        self.html_code = ""  # Add the 'html_code' attribute and initialize it to an empty string

    def create_widgets(self):
        self.root.title("Web Scraper")

        # URL Label and Input
        url_label = Label(self.root, text="URL:")
        url_label.pack(anchor='w', pady=5)

        self.url_input = Entry(self.root, width=50)
        self.url_input.pack(anchor='w')

        # Process Button
        self.process_button = Button(self.root, text="Process", command=self.process_url_input)
        self.process_button.pack(side='right', padx=10, pady=10)

        # Close Button
        close_button = Button(self.root, text="Close", command=self.root.quit)
        close_button.pack(side='left', padx=10, pady=10)

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
        except Exception:
            # Log uncaught exception
            self.error_handler.log_exception(*sys.exc_info())
            # Display error message to the user
            messagebox.showerror("Error", "An error occurred. Please check the log file for details.")

    def show_html_code(self, html_code):
        
        self.html_code = html_code  # Set the 'html_code' attribute
        html_window = Toplevel(self.root)
        html_window.title("HTML Code")

        html_scrolled_text = HTMLCodeScrolledText(html_window)
        html_scrolled_text.pack(fill='both', expand=True)
        html_scrolled_text.show_html_code(html_code)

        # Select Button
        select_button = Button(html_window, text="Select Elements", command=self.open_element_selection)
        select_button.pack(side='right', padx=10, pady=10)

        # Back Button
        back_button = Button(html_window, text="Back", command=self.root.deiconify)
        back_button.pack(side='left', padx=10, pady=10)

    


    def open_element_selection(self):
        elements_window = Toplevel(self.root)
        elements_window.title("Select HTML Elements to Scrape")
    
        elements_frame = Frame(elements_window)
        elements_frame.pack(fill='both', expand=True)
    
        # Label for search bar
        search_label = Label(elements_frame, text="Search Elements: Use Crtl key or Command key for multiple selection")
        search_label.pack(side='top', padx=10, pady=5)
    
        # Search Bar
        search_entry = Entry(elements_frame, width=30)
        search_entry.pack(side='top', padx=10, pady=5)
    
        elements_listbox = Listbox(elements_frame, selectmode='multiple', width=100, height=35)
        elements_listbox.pack(side='left', padx=10, pady=5)
    
        scrollbar = Scrollbar(elements_frame, command=elements_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        elements_listbox.config(yscrollcommand=scrollbar.set)
    
        # Add elements to the listbox
        elements = self.webscraper.get_elements()
    
        def filter_elements(event=None):
            search_text = search_entry.get()
            elements_listbox.delete(0, END)  # Clear previous elements
    
            filtered_elements = [element for element in elements if search_text.lower() in element.lower()]
    
            for element in filtered_elements:
                elements_listbox.insert(END, element)
    
        search_entry.bind("<KeyRelease>", filter_elements)
    
        filter_elements()
    
        # Select Button
        select_button = Button(elements_window, text="Scrape", command=lambda: self.process_selected_elements(elements_listbox))
        select_button.pack(side='right', padx=10, pady=10)
    
        # Back Button
        back_button = Button(elements_window, text="Back", command=elements_window.destroy)
        back_button.pack(side='left', padx=10, pady=10)




    def save_data(self, scraped_data_window): # This Method helps in the type of file to be saved
        scraped_data = scraped_data_window.scraped_data
        
    
        file_path = tkFileDialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")]
        )
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    data_frame = pd.DataFrame(scraped_data)
                    data_frame.to_csv(file_path, index=False)
                    messagebox.showinfo("Save Successful", "Data saved as CSV.")
                elif file_path.endswith(".xlsx"):
                    data_frame = pd.DataFrame(scraped_data)
                    data_frame.to_excel(file_path, index=False)
                    messagebox.showinfo("Save Successful", "Data saved as Excel.")
                    
                else:
                    messagebox.showerror("Invalid File Format", "Please save the data in CSV or Excel format.")
            
            # Close all windows and start at the first window
                self.root.quit()
                self.root.destroy()
                run_app()
            
            except Exception as e:
                messagebox.showerror("Save Error", str(e))


    
    
    def process_selected_elements(self, elements_listbox):
        # Check if elements are selected
        if elements_listbox.curselection():
            selected_indices = elements_listbox.curselection()
            selected_elements = [elements_listbox.get(index) for index in selected_indices]
    
            # Pass the selected elements to the scraper for further processing
            scraped_data = self.webscraper.scrape_data(selected_elements)

    
            # Create an instance of the ScrapedDataWindow to display and save the scraped data
            scraped_data_window = ScrapedDataWindow(self.root, scraped_data)
            scraped_data_window.display_scraped_data()  # Display the scraped data window
            scraped_data_window.save_button.config(command=lambda: self.save_data(scraped_data_window))  # Attach the save command
    
            self.root.withdraw()  # Hide the main window







def run_app():
    root = Tk()
    app = App(root)
    app.create_widgets()
    root.mainloop()


if __name__ == "__main__":
    error_handler = ErrorHandler()
    log_uncaught_exceptions(error_handler)
    run_app()

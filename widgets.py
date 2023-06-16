import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class HTMLCodeScrolledText(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.scrolled_text = ScrolledText(self)
        self.scrolled_text.pack(fill=tk.BOTH, expand=True)

    def show_html_code(self, html_code):
        self.scrolled_text.delete("1.0", tk.END)  # Clear previous content
        self.scrolled_text.insert(tk.END, html_code,"html")


class ElementsListbox(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.listbox = tk.Listbox(self)
        self.scrollbar = tk.Scrollbar(self, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def insert_elements(self, elements):
        self.listbox.delete(0, tk.END)  # Clear previous elements

        for element in elements:
            self.listbox.insert(tk.END, element)

    def get_selected_element(self):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_element = self.listbox.get(selected_index)
            return selected_element

    def clear_selection(self):
        self.listbox.selection_clear(0, tk.END)

    def get_all_elements(self):
        return self.listbox.get(0, tk.END)


class ScrapedDataWindow(tk.Toplevel):
    def __init__(self, parent, scraped_data):
        super().__init__(parent)
        self.title("Scraped Data")

        self.data_listbox = tk.Listbox(self)
        self.data_listbox.pack(fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(self, text="Save", command=self.save_data)
        self.save_button.pack(side=tk.LEFT)

        self.done_button = tk.Button(self, text="Done", command=self.close_window)
        self.done_button.pack(side=tk.LEFT)

        self.data_listbox.delete(0, tk.END)  # Clear previous data
        for data in scraped_data:
            tag = data["tag"]
            attributes = data["attributes"]
            element_data = f"Tag: {tag}  |  Attributes: {attributes}"
            self.data_listbox.insert(tk.END, element_data)

    def save_data(self):
        selected_indices = self.data_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_data = self.data_listbox.get(selected_index)
            # Logic to save the selected data to a file (Excel or CSV)
            # You can implement the save functionality according to your requirements
            print(f"Save data: {selected_data}")

    def close_window(self):
        self.destroy()

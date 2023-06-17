import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from tkinter import Toplevel, ttk, filedialog, messagebox
import pandas as pd

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






class ScrapedDataWindow:
    def __init__(self, parent, scraped_data):
        self.parent = parent
        self.scraped_data = scraped_data

        self.window = Toplevel(self.parent)
        self.window.title("Scraped Data")

        # Create a Treeview widget to display the scraped data
        self.treeview = ttk.Treeview(self.window)
        self.treeview.pack(fill="both", expand=True)

        # Display the scraped data in the Treeview widget
        self.display_scraped_data()

        # Save Button
        self.save_button = ttk.Button(self.window, text="Save", command=self.save_data)
        self.save_button.pack()

    # def display_scraped_data(self):
    #     # Clear existing data in the treeview
    #     self.treeview.delete(*self.treeview.get_children())
    
    #     self.treeview["columns"] = ("tag", "attributes", "attribute_count", "data")
    #     self.treeview.heading("tag", text="Tag")
    #     self.treeview.heading("attributes", text="Attributes")
    #     self.treeview.heading("attribute_count", text="Attribute Count")
    #     self.treeview.heading("data", text="Data")
    
    #     for data in self.scraped_data:
    #         tag = data["tag"]
    #         attributes = data.get("attributes", {})
    #         attribute_count = data.get("attribute_count", 0)
    #         data_text = data.get("data", "")
    
    #         self.treeview.insert("", "end", values=(tag, attributes, attribute_count, data_text))

    
    def display_scraped_data(self):
        # Clear existing data in the treeview
        self.treeview.delete(*self.treeview.get_children())
    
        self.treeview["columns"] = ("sr_no", "tag", "attributes", "attribute_count", "data")
        self.treeview.heading("sr_no", text="Sr. No")
        self.treeview.heading("tag", text="Tag")
        self.treeview.heading("attributes", text="Attributes")
        self.treeview.heading("attribute_count", text="Attribute Count")
        self.treeview.heading("data", text="Data")
    
        for i, data in enumerate(self.scraped_data, start=1):
            tag = data["tag"]
            attributes = data.get("attributes", {})
            attribute_count = data.get("attribute_count", 0)
            data_text = data.get("data", "")
    
            self.treeview.insert("", "end", values=(i, tag, attributes, attribute_count, data_text))


    # def save_data(self):
    #     # Use self.scraped_data instead of self
    #     data_frame = pd.DataFrame(self.scraped_data)
    #     selected_item = self.treeview.focus()
    #     values = self.treeview.item(selected_item)["values"]
    #     import pdb; pdb.set_trace()
    #     # Save the selected data to a file (you can modify this as per your requirements)
    #     filename = filedialog.asksaveasfilename(defaultextension=".csv")
    #     if filename:
    #         try:
    #             with open(filename, "w") as file:
    #                 file.write(f"Tag: {values[0]}\n")
    #                 file.write(f"Attributes: {values[1]}\n")
    #                 file.write(f"Data: {values[2]}\n")
    #             messagebox.showinfo("Save", "Scraped data saved successfully.")
    #         except Exception as e:
    #             messagebox.showerror("Error", f"An error occurred while saving the data:\n{str(e)}")


    def save_data(self): # This method configures what needs to be saved 
        # Use self.scraped_data instead of self
        data_frame = pd.DataFrame(self.scraped_data)
        selected_item = self.treeview.focus()
        values = self.treeview.item(selected_item)["values"]
        import pdb; pdb.set_trace()
        # Save the selected data to a file (you can modify this as per your requirements)
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            try:
                with open(filename, "w") as file:
                    file.write(f"Sr. No: {values[0]}\n")
                    file.write(f"Tag: {values[1]}\n")
                    file.write(f"Attributes: {values[2]}\n")
                    file.write(f"Attribute Count: {values[3]}\n")
                    file.write(f"Data: {values[4]}\n")
                messagebox.showinfo("Save", "Scraped data saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the data:\n{str(e)}")
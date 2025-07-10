# frames/apartments_frame.py
import customtkinter as ctk
from tkinter import ttk
import db

class ApartmentsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.load_table()

    def load_table(self):
        for widget in self.winfo_children():
            widget.destroy()

        table = ttk.Treeview(self, columns=("apartment_id", "tariff_group_id", "group_apartment"),
                             show="headings", height=15)
        table.heading("apartment_id", text="מספר דירה")
        table.heading("tariff_group_id", text="קבוצת תעריף")
        table.heading("group_apartment", text="קבוצת דירות")

        table.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)

        for i, row in enumerate(db.fetch_apartments()):
            tag = "even" if i % 2 == 0 else "odd"
            table.insert("", "end", values=row, tags=(tag,))
        table.tag_configure("even", background="white")
        table.tag_configure("odd", background="#cccccc")

# tariff_frame.py
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import db

class TariffFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.mode = "table"
        self.load_table()

    def load_table(self):
        self.mode = "table"
        for widget in self.winfo_children():
            widget.destroy()

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(btn_frame, text="חדש", command=self.add_tariff).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="עדכון", command=self.update_tariff).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="מחק", command=self.delete_tariff).grid(row=0, column=2, padx=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview.Heading",
                        font=("Arial", 16, "bold"),
                        foreground="white",
                        background="#333333")
        style.configure("Custom.Treeview",
                        font=("Arial", 16),
                        rowheight=30,
                        background="white",
                        fieldbackground="white",
                        borderwidth=1,
                        relief="flat")
        style.map("Custom.Treeview", background=[("selected", "#2a6f97")])

        self.table = ttk.Treeview(self,
                                  columns=("group_id", "start_date", "vat", "price_per_kwh", "fixed", "cubic"),
                                  show="headings", height=15, style="Custom.Treeview")

        headings = {
            "group_id": "קבוצת תעריפים",
            "start_date": "תאריך התחלה",
            "vat": "מע\"מ",
            "price_per_kwh": "מחיר לקוט\"ש",
            "fixed": "חשמל יומי",
            "cubic": "מחיר למ\"ק"
        }
        for col, text in headings.items():
            self.table.heading(col, text=text)
            self.table.column(col, anchor="center", stretch=True)

        self.table.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)

        for i, row in enumerate(db.fetch_tariffs()):
            tag = "even" if i % 2 == 0 else "odd"
            self.table.insert("", "end", values=row, tags=(tag,))
        self.table.tag_configure("even", background="white")
        self.table.tag_configure("odd", background="#cccccc")

    def add_tariff(self):
        self.mode = "form"
        self.clear_widgets()

        self.entries = {}
        labels = {
            "group_id": "קבוצת תעריפים",
            "start_date": "תאריך התחלה (YY-MM-DD)",
            "vat": "מע\"מ",
            "price_per_kwh": "מחיר לקוט\"ש",
            "fixed_electricity_daily": "תשלום יומי לחשמל",
            "price_per_cubic_meter": "מחיר למ\"ק מים"
        }

        form = ctk.CTkFrame(self)
        form.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        for i, (field, label) in enumerate(labels.items()):
            ctk.CTkLabel(form, text=label, font=("Arial", 16, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form, font=("Arial", 16))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[field] = entry

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="שמור", command=self.save_tariff).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="ביטול", command=self.load_table).grid(row=0, column=1, padx=10)

    def save_tariff(self):
        try:
            group_id = self.entries["group_id"].get().strip()
            start_date = self.entries["start_date"].get().strip()
            vat = float(self.entries["vat"].get().strip())
            price_per_kwh = float(self.entries["price_per_kwh"].get().strip())
            fixed = float(self.entries["fixed_electricity_daily"].get().strip())
            cubic = float(self.entries["price_per_cubic_meter"].get().strip())

            if not group_id:
                raise ValueError("חובה למלא קבוצת תעריפים")

            # בדיקת תאריך תקני
            try:
                datetime.strptime(start_date, "%y-%m-%d")
            except ValueError:
                raise ValueError("תאריך לא תקין. השתמש בפורמט YY-MM-DD")

            db.insert_tariff((group_id, start_date, vat, price_per_kwh, fixed, cubic))
            messagebox.showinfo("הצלחה", "התעריף נשמר בהצלחה")
            self.load_table()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    def update_tariff(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("שגיאה", "יש לבחור תעריף לעדכון")
            return

        values = self.table.item(selected[0])["values"]
        self.mode = "update"
        self.selected_tariff = values
        self.clear_widgets()

        self.entries = {}
        labels = {
            "group_id": "קבוצת תעריפים",
            "start_date": "תאריך התחלה (YY-MM-DD)",
            "vat": "מע\"מ",
            "price_per_kwh": "מחיר לקוט\"ש",
            "fixed_electricity_daily": "תשלום יומי לחשמל",
            "price_per_cubic_meter": "מחיר למ\"ק מים"
        }

        form = ctk.CTkFrame(self)
        form.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        for i, (field, label) in enumerate(labels.items()):
            ctk.CTkLabel(form, text=label, font=("Arial", 16, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form, font=("Arial", 16))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entry.insert(0, values[i])
            if field in ["group_id", "start_date"]:
                entry.configure(state="disabled")
            self.entries[field] = entry

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="שמור", command=self.save_update).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="ביטול", command=self.load_table).grid(row=0, column=1, padx=10)

    def save_update(self):
        try:
            group_id = self.selected_tariff[0]
            start_date = self.selected_tariff[1]
            vat = float(self.entries["vat"].get().strip())
            price_per_kwh = float(self.entries["price_per_kwh"].get().strip())
            fixed = float(self.entries["fixed_electricity_daily"].get().strip())
            cubic = float(self.entries["price_per_cubic_meter"].get().strip())

            db.update_tariff((vat, price_per_kwh, fixed, cubic, group_id, start_date))
            messagebox.showinfo("הצלחה", "התעריף עודכן בהצלחה")
            self.load_table()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    def delete_tariff(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("שגיאה", "יש לבחור תעריף למחיקה")
            return
        values = self.table.item(selected[0])["values"]
        try:
            db.delete_tariff(values[0], values[1])
            self.load_table()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

# ui.py
import customtkinter as ctk
from tkinter import messagebox
from tariff_frame import TariffFrame
from apartments_frame import ApartmentsFrame


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ניהול שכירויות")
        self.geometry("800x600")
        self.minsize(700, 500)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # תפריט צד ימין
        self.menu_frame = ctk.CTkFrame(self, width=200)
        self.menu_frame.grid(row=0, column=0, sticky="ns")
        self.menu_frame.grid_propagate(False)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.buttons = {
            "ניהול תעריפים": self.load_tariff_frame,
            "ניהול דירות": self.load_apartments_frame,
        }

        for i, (text, command) in enumerate(self.buttons.items()):
            btn = ctk.CTkButton(
                self.menu_frame, text=text, font=("Arial", 16, "bold"),
                command=command
            )
            btn.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            self.menu_frame.grid_rowconfigure(i, weight=0)

        self.current_frame = None
        self.load_tariff_frame()

    def clear_content(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def load_tariff_frame(self):
        self.clear_content()
        self.current_frame = TariffFrame(self.content_frame)
        self.current_frame.pack(fill="both", expand=True)

    def load_apartments_frame(self):
        self.clear_content()
        self.current_frame = ApartmentsFrame(self.content_frame)
        self.current_frame.pack(fill="both", expand=True)

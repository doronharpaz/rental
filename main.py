# main.py
import customtkinter as ctk
from ui import MainApp

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()

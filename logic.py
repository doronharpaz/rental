from datetime import datetime
from tkinter import messagebox

def validate_tariff_inputs(values):
    try:
        datetime.strptime(values["start_date"], "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("שגיאה", "יש להזין תאריך בפורמט YYYY-MM-DD")
        return False

    numeric_fields = ["vat", "price_per_kwh", "fixed_electricity_daily", "price_per_cubic_meter"]
    for field in numeric_fields:
        try:
            float(values[field])
        except ValueError:
            messagebox.showerror("שגיאה", f"השדה {field} חייב להיות מספר")
            return False

    if not values["group_id"]:
        messagebox.showerror("שגיאה", "יש להזין מזהה קבוצה")
        return False

    return True

import tkinter as tk
from tkinter import ttk
from SRC.ViewLayer.Theme.ModernUI import ModernUI

class PreferencesMenu(tk.Frame):
    def __init__(self, parent, on_select, default_label="Display by"):
        super().__init__(parent, bg=ModernUI.COLORS["light"])

        self.on_select = on_select

        # תיבות בחירה
        self.display_options = {
            "Active Days": "active_days",
            "Free Windows": "free_windows_number",
            "Total Free Windows": "free_windows_sum",
            "Avg Start": "average_start_time",
            "Avg End": "average_end_time"
        }
        self.sort_options = ["Ascending", "Descending"]

        # משתנים
        self.display_var = tk.StringVar()
        self.sort_var = tk.StringVar(value="Ascending")  # ברירת מחדל

        # תיבת בחירה להעדפה
        tk.Label(self, text="Display by:", bg=ModernUI.COLORS["light"]).pack(side=tk.LEFT, padx=5)
        self.display_box = ttk.Combobox(self, textvariable=self.display_var, state="readonly")
        self.display_box["values"] = list(self.display_options.keys())
        self.display_box.pack(side=tk.LEFT, padx=5)
        self.display_box.bind("<<ComboboxSelected>>", self._update_selection)

        # תיבת בחירה לסדר
        tk.Label(self, text="Sort:", bg=ModernUI.COLORS["light"]).pack(side=tk.LEFT, padx=5)
        self.sort_box = ttk.Combobox(self, textvariable=self.sort_var, state="readonly")
        self.sort_box["values"] = self.sort_options
        self.sort_box.pack(side=tk.LEFT, padx=5)
        self.sort_box.bind("<<ComboboxSelected>>", self._update_selection)

    def _update_selection(self, event=None):
        display_label = self.display_var.get()
        order = self.sort_var.get()

        if not display_label:
            print("Please select a display option.")
            return

        display = self.display_options.get(display_label)
        print(f"Selected display: {display}, order: {order}")

        self.on_select(display, order)

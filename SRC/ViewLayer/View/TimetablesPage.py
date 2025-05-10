# view/TimetablesPage.py

import tkinter as tk
from tkinter import messagebox
from SRC.ViewLayer.Theme.ModernUI import ModernUI
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots
from SRC.ViewLayer.Layout.TimeTable import draw_timetable_grid

class TimetableApp:
    def __init__(self, root, timetable_options):
        self.root = root
        self.options = timetable_options
        self.current_index = 0

        self.header = tk.Label(root, text="", font=("Arial", 14))
        self.header.pack(pady=10)
       
        # # non scrollable frame
        # self.frame = tk.Frame(root)
        # self.frame.pack()
        
        # Create a scrollable canvas
        canvas = tk.Canvas(root, borderwidth=10, background=ModernUI.COLORS["light"])
        scroll_frame = tk.Frame(canvas, background=ModernUI.COLORS["white"])
        # scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Scrollbar
        vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Put the timetable frame inside the canvas
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Set scrolling region
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_frame_configure)

        # Store the frame reference
        self.frame = scroll_frame

        # Create the timetable grid
        self.navbar = tk.Frame(root)
        self.navbar.pack(pady=10)

        # 'Prev' button
        self.prev_button = ModernUI.create_rounded_button(
            self.navbar, "Previous", self.show_prev, 
            bg_color=ModernUI.COLORS["dark"], width=100)
        self.prev_button.pack(side="left", pady=10)

        # 'Next' button
        self.next_button = ModernUI.create_rounded_button(
            self.navbar, "Next", self.show_next, 
            bg_color=ModernUI.COLORS["dark"], width=100)
        self.next_button.pack(side="right", pady=10)
       

        self.update_view()

    # This method updates the timetable view based on the current index.
    def update_view(self):
        """Update the timetable view based on the current option."""
        # If there are no options, show a message and destroy the frame.
        if len(self.options) == 0:
            messagebox.showinfo("No Timetable Options", "No timetable options available.")
            self.root.destroy() # Close the application TODO: change it to stay? empry grid? go back?
            return
        # If there are options, clear the frame and draw the new timetable.
        courses = self.options[self.current_index] # Each option is a list of courses (List<Course>)
        slot_map = map_courses_to_slots(courses) # Maps the courses to their respective time slots. func from logic.
        draw_timetable_grid(self.frame, slot_map) # Draws the timetable grid based on the slot_map. func from layout.
        self.header.config(text=f"Timetable Option {self.current_index + 1} of {len(self.options)}")

    
    def show_prev(self):
        """Show the previous timetable option."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_view()

    def show_next(self):
        """Show the next timetable option."""
        if self.current_index < len(self.options) - 1:
            self.current_index += 1
            self.update_view()
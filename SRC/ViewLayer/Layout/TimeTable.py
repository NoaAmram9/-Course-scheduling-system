# # layout_timetable.py

# import tkinter as tk
# from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS

# def draw_timetable_grid(frame, slot_map):
#     """Draws the timetable grid into the given frame based on the slot_map."""
#     for widget in frame.winfo_children():
#         widget.destroy()

#     # Header row: day labels
#     tk.Label(frame, text="").grid(row=0, column=0)
#     for col, day in enumerate(DAYS, start=1):
#         tk.Label(frame, text=day, borderwidth=1, relief="solid", width=15).grid(row=0, column=col)

#     # Time rows + course cells
#     for row, hour in enumerate(HOURS, start=1):
#         # Time label
#         tk.Label(frame, text=f"{hour}:00", borderwidth=1, relief="solid", width=10).grid(row=row, column=0)
#         # Course cells
#         for col, day in enumerate(DAYS, start=1):
#             course = slot_map.get((day, hour))
#             if course:
#                 name = course["name"]
#                 code = course["code"]
#                 course_type = course["type"]
#                 instructor = course["instructor"]
#                 location = course["location"]
#                 course_info = f"{name} ({code}) \n {course_type} \n {instructor} \n {location}"
#             else:
#                 course_info = ""  # If there's no course at this day+hour, just return an empty string.
            
#             tk.Label(frame, text=course_info, borderwidth=1, relief="solid", width=15, height=2, bg="white").grid(row=row, column=col) # Creates a visible label and puts it in the grid.


# layout_timetable.py

import tkinter as tk
from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS
from SRC.ViewLayer.Theme.ModernUI import ModernUI


def draw_timetable_grid(frame, slot_map):
    """Draws the timetable grid into the given frame based on the slot_map."""

    # Clear previous content
    for widget in frame.winfo_children():
        widget.destroy()

    # Configure grid to expand
    for r in range(len(HOURS) + 1):
        frame.grid_rowconfigure(r, weight=1)
    for c in range(len(DAYS) + 1):
        frame.grid_columnconfigure(c, weight=1)

    # Header row (Days)
    tk.Label(frame, text="", bg=ModernUI.COLORS["light"]).grid(row=0, column=0, sticky="nsew")
    for col, day in enumerate(DAYS, start=1):
        tk.Label(
            frame, text=day, bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"],
            borderwidth=1, relief="solid", width=15, height=4,
            font=("Calibri", 12, "bold")
        ).grid(row=0, column=col, sticky="nsew")

    # Time + cells
    for row, hour in enumerate(HOURS, start=1):
        # Time label column
        tk.Label(
            frame, text=f"{hour}:00", bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"],
            borderwidth=1, relief="solid", width=12, height=3,
            font=("Calibri", 11, "bold")
        ).grid(row=row, column=0, sticky="nsew")

        # Time slot cells
        for col, day in enumerate(DAYS, start=1):
            course = slot_map.get((day, hour))
            if course:
                # Course styling
                name = course["name"]
                code = course["code"]
                course_type = course["type"]
                instructor = course["instructor"]
                location = course["location"]

                # Choose background color by course type
                type_colors = {
                    "Lecture": ModernUI.COLORS["lecture"],
                    "Lab": ModernUI.COLORS["lab"],
                    "Exercise": ModernUI.COLORS["exercise"],
                }
                bg_color = type_colors.get(course_type, ModernUI.COLORS["gray"])

                # Use a Text widget (instead of Label) for better formatting
                text_widget = tk.Text(
                    frame,
                    bg=bg_color, fg=ModernUI.COLORS["black"],
                    font=("Calibri", 10),  # base font
                    width=22, height=8,
                    wrap="word", borderwidth=1, relief="solid"
                )

                # Insert formatted text with different fonts/sizes
                text_widget.insert("end", f"{name} ", ("name",))
                text_widget.insert("end", f"({code})\n", ("code",))
                text_widget.insert("end", f"{course_type}\n", ("type",))
                text_widget.insert("end", f"{instructor}\n", ("instructor",))
                text_widget.insert("end", f"{location}", ("location",))

                # Define tag styles
                text_widget.tag_configure("name", font=("Calibri", 9, "bold"))
                text_widget.tag_configure("code", font=("Calibri", 8, "italic"))
                text_widget.tag_configure("type", font=("Calibri", 7))
                text_widget.tag_configure("instructor", font=("Calibri", 7))
                text_widget.tag_configure("location", font=("Calibri", 7, "italic"))

                text_widget.config(state="disabled")  # Make it read-only
                text_widget.grid(row=row, column=col, sticky="nsew")
            else:
                # Empty cell
                tk.Label(
                    frame,
                    text="", bg=ModernUI.COLORS["white"],
                    borderwidth=1, relief="solid", width=20, height=8
                ).grid(row=row, column=col, sticky="nsew")

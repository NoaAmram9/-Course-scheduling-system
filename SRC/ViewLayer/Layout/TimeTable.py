# layout_timetable.py

import tkinter as tk
from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS
from SRC.ViewLayer.Theme.ModernUI import ModernUI


# def draw_timetable_grid(frame, slot_map):
#     """Draws the timetable grid into the given frame based on the slot_map."""

#     # Clear previous content
#     for widget in frame.winfo_children():
#         widget.destroy()

#     # Configure grid to expand
#     for r in range(len(HOURS) + 1):
#         frame.grid_rowconfigure(r, weight=1)
#     for c in range(len(DAYS) + 1):
#         frame.grid_columnconfigure(c, weight=1)
        

#     # # Header row (Days) 
#     # In comment because the days should be fixed when scrolling, in contrast to the rest of the timetable.
#     # tk.Label(frame, text="", bg=ModernUI.COLORS["light"]).grid(row=0, column=0, sticky="nsew")
#     # for col, day in enumerate(DAYS, start=1):
#     #     tk.Label(
#     #         frame, text=day, bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"],
#     #         borderwidth=1, relief="solid", width=15, height=4,
#     #         font=("Helvetica", 12, "bold")
#     #     ).grid(row=0, column=col, sticky="nsew")

#     # Time + cells
#     for row, hour in enumerate(HOURS, start=1):
#         # Time label column
#         tk.Label(
#             frame, text=f"{hour}:00", bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"],
#             borderwidth=1, relief="solid", width=12, height=3,
#             font=("Helvetica", 11, "bold")
#         ).grid(row=row, column=0, sticky="nsew")

#         # Time slot cells
#         for col, day in enumerate(DAYS, start=1):
#             course = slot_map.get((day, hour))
#             if course:
#                 # Course styling
#                 name = course["name"]
#                 code = course["code"]
#                 course_type = course["type"]
#                 instructor = course["instructor"]
#                 location = course["location"]

#                 # Choose background color by course type
#                 type_colors = {
#                     "Lecture": ModernUI.COLORS["lecture"],
#                     "Lab": ModernUI.COLORS["lab"],
#                     "Exercise": ModernUI.COLORS["exercise"],
#                 }
#                 bg_color = type_colors.get(course_type, ModernUI.COLORS["gray"])
#                 # Create a text widget for the course info
#                 text_widget = tk.Text(
#                     frame,
#                     bg=bg_color, fg=ModernUI.COLORS["black"],
#                     font=("Helvetica", 10),  # base font
#                     width=22, height=8,
#                     wrap="word", borderwidth=1, relief="solid"
#                 )

#                 # Insert formatted text with different fonts/sizes
#                 text_widget.insert("end", f"{name} ", ("name",))
#                 text_widget.insert("end", f"({code})\n", ("code",))
#                 text_widget.insert("end", f"{course_type}\n", ("type",))
#                 text_widget.insert("end", f"{instructor}\n", ("instructor",))
#                 text_widget.insert("end", f"{location}", ("location",))

#                 # Define tag styles
#                 text_widget.tag_configure("name", font=("Helvetica", 11, "bold"))
#                 text_widget.tag_configure("code", font=("Helvetica", 9, "italic"))
#                 text_widget.tag_configure("type", font=("Helvetica", 8))
#                 text_widget.tag_configure("instructor", font=("Helvetica", 8))
#                 text_widget.tag_configure("location", font=("Helvetica", 8, "italic"))

#                 text_widget.config(state="disabled")  # Make it read-only
#                 text_widget.grid(row=row, column=col, sticky="nsew")
#             else:
#                 # Empty cell
#                 tk.Label(
#                     frame,
#                     text="", bg=ModernUI.COLORS["white"],
#                     borderwidth=1, relief="solid", width=20, height=8
#                 ).grid(row=row, column=col, sticky="nsew")


def draw_timetable_grid(frame, slot_map):
    from tkinter import Canvas

    def draw_rounded_cell(canvas, x1, y1, x2, y2, radius, fill, text="", font=("Helvetica", 10), bold_top=False):
        shadow_offset = 3
        # Shadow
        canvas.create_rectangle(
            x1 + shadow_offset, y1 + shadow_offset,
            x2 + shadow_offset, y2 + shadow_offset,
            fill="#d0d0d0", outline="", width=0
        )

        # Rounded rectangle (approximate using polygon)
        canvas.create_polygon(
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
            smooth=True,
            fill=fill, outline=ModernUI.COLORS["gray"]
        )

        if bold_top:
            canvas.create_line(x1, y1, x2, y1, fill="#555555", width=2)

        canvas.create_text(
            (x1 + x2) // 2,
            (y1 + y2) // 2,
            text=text,
            font=font,
            fill=ModernUI.COLORS["black"],
            justify="center"
        )

    # Clear previous content
    for widget in frame.winfo_children():
        widget.destroy()

    cell_width = 200
    cell_height = 100
    radius = 12

    # Grid config to stretch
    for r in range(len(HOURS) + 1):
        frame.grid_rowconfigure(r, weight=1)
    for c in range(len(DAYS) + 1):
        frame.grid_columnconfigure(c, weight=1)

    # Header: Day names
    for col, day in enumerate([""] + DAYS):
        canvas = Canvas(frame, width=cell_width, height=cell_height, bg=ModernUI.COLORS["light"], highlightthickness=0)
        canvas.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)

        if day:
            draw_rounded_cell(
                canvas, 5, 5, cell_width - 5, cell_height - 5, radius,
                fill=ModernUI.COLORS["light"],
                text=day,
                font=("Helvetica", 12, "bold")
            )

    # Time + timetable
    for row, hour in enumerate(HOURS, start=1):
        # Time column
        canvas = Canvas(frame, width=cell_width, height=cell_height, bg=ModernUI.COLORS["light"], highlightthickness=0)
        canvas.grid(row=row, column=0, sticky="nsew", padx=2, pady=2)

        draw_rounded_cell(
            canvas, 5, 5, cell_width - 5, cell_height - 5, radius,
            fill=ModernUI.COLORS["light"],
            text=f"{hour}:00",
            font=("Helvetica", 11, "bold")
        )

        # Content cells
        for col, day in enumerate(DAYS, start=1):
            course = slot_map.get((day, hour))
            canvas = Canvas(frame, width=cell_width, height=cell_height, bg=ModernUI.COLORS["white"], highlightthickness=0)
            canvas.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

            if course:
                name = course["name"]
                code = course["code"]
                course_type = course["type"]
                instructor = course["instructor"]
                location = course["location"]

                type_colors = {
                    "Lecture": ModernUI.COLORS["lecture"],
                    "Lab": ModernUI.COLORS["lab"],
                    "Exercise": ModernUI.COLORS["exercise"],
                }
                bg_color = type_colors.get(course_type, ModernUI.COLORS["gray"])

                text = f"{name} ({code})\n{course_type}\n{instructor}\n{location}"

                draw_rounded_cell(
                    canvas, 5, 5, cell_width - 5, cell_height - 5, radius,
                    fill=bg_color,
                    text=text,
                    font=("Helvetica", 9),
                    bold_top=True
                )
            else:
                draw_rounded_cell(
                    canvas, 5, 5, cell_width - 5, cell_height - 5, radius,
                    fill=ModernUI.COLORS["white"]
                )
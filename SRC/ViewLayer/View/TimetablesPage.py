# # view/TimetablesPage.py

# import tkinter as tk
# from tkinter import messagebox
# from SRC.ViewLayer.Theme.ModernUI import ModernUI
# from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots
# from SRC.ViewLayer.Layout.TimeTable import draw_timetable_grid

# class TimetableApp:
#     def __init__(self, root, timetable_options):
#         self.root = root
#         self.options = timetable_options
#         self.current_index = 0

#         self.header = tk.Label(root, text="", font=("Arial", 14))
#         self.header.pack(pady=10)
       
#         # # non scrollable frame
#         # self.frame = tk.Frame(root)
#         # self.frame.pack()
        
#         # Create a scrollable canvas
#         canvas = tk.Canvas(root, borderwidth=10, background=ModernUI.COLORS["light"])
#         scroll_frame = tk.Frame(canvas, background=ModernUI.COLORS["white"])
#         # scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#         # Scrollbar
#         vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
#         canvas.configure(yscrollcommand=vsb.set)

#         vsb.pack(side="right", fill="y")
#         canvas.pack(side="left", fill="both", expand=True)

#         # Put the timetable frame inside the canvas
#         canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

#         # Set scrolling region
#         def on_frame_configure(event):
#             canvas.configure(scrollregion=canvas.bbox("all"))

#         scroll_frame.bind("<Configure>", on_frame_configure)

#         # Store the frame reference
#         self.frame = scroll_frame

#         # Create the timetable grid
#         self.navbar = tk.Frame(root)
#         self.navbar.pack(pady=10)

#         # 'Prev' button
#         self.prev_button = ModernUI.create_rounded_button(
#             self.navbar, "Previous", self.show_prev, 
#             bg_color=ModernUI.COLORS["dark"], width=100)
#         self.prev_button.pack(side="left", pady=10)

#         # 'Next' button
#         self.next_button = ModernUI.create_rounded_button(
#             self.navbar, "Next", self.show_next, 
#             bg_color=ModernUI.COLORS["dark"], width=100)
#         self.next_button.pack(side="right", pady=10)
       

#         self.update_view()

#     # This method updates the timetable view based on the current index.
#     def update_view(self):
#         """Update the timetable view based on the current option."""
#         # If there are no options, show a message and destroy the frame.
#         if len(self.options) == 0:
#             messagebox.showinfo("No Timetable Options", "No timetable options available.")
#             self.root.destroy() # Close the application TODO: change it to stay? empry grid? go back?
#             return
#         # If there are options, clear the frame and draw the new timetable.
#         courses = self.options[self.current_index] # Each option is a list of courses (List<Course>)
#         slot_map = map_courses_to_slots(courses) # Maps the courses to their respective time slots. func from logic.
#         draw_timetable_grid(self.frame, slot_map) # Draws the timetable grid based on the slot_map. func from layout.
#         self.header.config(text=f"Timetable Option {self.current_index + 1} of {len(self.options)}")

    
#     def show_prev(self):
#         """Show the previous timetable option."""
#         if self.current_index > 0:
#             self.current_index -= 1
#             self.update_view()

#     def show_next(self):
#         """Show the next timetable option."""
#         if self.current_index < len(self.options) - 1:
#             self.current_index += 1
#             self.update_view()
            
            
            
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from SRC.ViewLayer.Theme.ModernUI import ModernUI
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots, DAYS, HOURS
from SRC.ViewLayer.Layout.TimeTable import draw_timetable_grid

class TimetablesPage:
    def __init__(self, root, timetable_options):
        self.root = root
        self.options = timetable_options
        self.current_index = 0
        
        # Configure the window to be responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create a navigation bar at the top
        self.create_nav_bar()
        
        # Create the timetable container
        self.create_timetable_container()
        
        # Initial view update
        self.update_view()
    
    def create_nav_bar(self):
        """Create the navigation bar with prev/next buttons and title"""
        nav_frame = tk.Frame(self.root, bg=ModernUI.COLORS["light"])
        nav_frame.grid(row=0, column=0, sticky="n", padx=10, pady=20)
        
        # Configure the nav frame to be responsive
        nav_frame.grid_columnconfigure(1, weight=1)
        
        # Previous button
        self.prev_button = ModernUI.create_rounded_button(
            nav_frame, "Prev", self.show_prev,
            bg_color=ModernUI.COLORS["dark"], width=50)
        self.prev_button.grid(row=0, column=0, padx=10)
        
        # Title label (timetable option x of y)
        self.title_label = tk.Label(
            nav_frame, text="",
            font=("Helvetica", 12, "bold"), bg=ModernUI.COLORS["light"])
        self.title_label.grid(row=0, column=1)
        
        # Next button
        self.next_button = ModernUI.create_rounded_button(
            nav_frame, "Next", self.show_next,
            bg_color=ModernUI.COLORS["dark"], width=50)
        self.next_button.grid(row=0, column=2, padx=10)
    
    def create_timetable_container(self):
        """Create a container for the timetable with a fixed header row"""
        # Main container
        self.timetable_container = tk.Frame(self.root, bg=ModernUI.COLORS["light"])
        self.timetable_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.timetable_container.grid_columnconfigure(0, weight=1)
        self.timetable_container.grid_rowconfigure(1, weight=1)
        
        # Days header (fixed while scrolling)
        self.days_header = tk.Frame(self.timetable_container, bg=ModernUI.COLORS["dark"])
        self.days_header.grid(row=0, column=0, sticky="ew")
        
        # Draw fixed day headers
        self.draw_days_header()
        
        # Scrollable timetable area
        self.canvas = tk.Canvas(self.timetable_container, borderwidth=0, highlightthickness=0, 
                              bg=ModernUI.COLORS["white"])
        self.scrollbar = ttk.Scrollbar(self.timetable_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid the canvas and scrollbar
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Frame inside canvas for the timetable content
        self.timetable_frame = tk.Frame(self.canvas, bg=ModernUI.COLORS["white"])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.timetable_frame, anchor="nw")
        
        # Configure scrolling and resizing behavior
        self.timetable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
    
    def on_frame_configure(self, event):
        """Update the scrollregion to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """When the canvas resizes, resize the inner frame to match"""
        # Update the width of the inner frame to match the canvas
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def draw_days_header(self):
        """Draw the fixed days header"""
        # Clear existing header
        for widget in self.days_header.winfo_children():
            widget.destroy()
            
        # Configure columns to be responsive
        for i in range(len(DAYS) + 1):  # +1 for the time column
            self.days_header.grid_columnconfigure(i, weight=1)
        
        # Empty cell in the top-left corner
        empty_cell = tk.Label(self.days_header, text="", width=12, height=3, 
                             bg=ModernUI.COLORS["light"], borderwidth=1, relief="solid")
        empty_cell.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        # Day headers
        for i, day in enumerate(DAYS):
            day_label = tk.Label(self.days_header, text=day, width=15, height=4,
                               font=("Helvetica", 12, "bold"), 
                               bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"],
                               borderwidth=1, relief="solid")
            day_label.grid(row=0, column=i+1, sticky="nsew")
    
    def update_view(self):
        """Update the view to display the current timetable option"""
        if not self.options:
            messagebox.showinfo("No Timetable Options", "No timetable options available.")
            return
        
        # Update the title
        self.title_label.config(text=f"Timetable Option {self.current_index + 1} of {len(self.options)}")
        
        # Get timetable for this option
        current_timetable = self.options[self.current_index]
        
        # Map courses to slots
        slot_map = map_courses_to_slots(current_timetable)
        
        # Clear previous content in the scroll frame
        for widget in self.timetable_frame.winfo_children():
            widget.destroy()
            
        # Draw the timetable using the imported function
        draw_timetable_grid(self.timetable_frame, slot_map)
        
        # Update buttons state based on current index
        # For prev button
        if self.current_index > 0:
            self.prev_button.config(bg=ModernUI.COLORS["dark"])
            self.prev_button.bind("<Button-1>", lambda e: self.show_prev())
        else:
            self.prev_button.config(bg=ModernUI.COLORS["gray"])  # Use gray color for disabled
            self.prev_button.unbind("<Button-1>")
        
        # For next button
        if self.current_index < len(self.options) - 1:
            self.next_button.config(bg=ModernUI.COLORS["dark"])
            self.next_button.bind("<Button-1>", lambda e: self.show_next())
        else:
            self.next_button.config(bg=ModernUI.COLORS["gray"])  # Use gray color for disabled
            self.next_button.unbind("<Button-1>")
    
    def show_prev(self):
        """Show the previous timetable option"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_view()
    
    def show_next(self):
        """Show the next timetable option"""
        if self.current_index < len(self.options) - 1:
            self.current_index += 1
            self.update_view()
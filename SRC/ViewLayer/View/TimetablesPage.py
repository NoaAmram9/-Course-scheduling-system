# timetables page
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tempfile
import os

from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.pagesizes import landscape, A4
from SRC.ViewLayer.Theme.ModernUI import ModernUI
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots, DAYS, HOURS
from SRC.ViewLayer.Layout.TimeTable import draw_timetable_grid
from SRC.ViewLayer.Logic.Pdf_Exporter import generate_pdf_from_data


class TimetablesPage:
    def __init__(self, root, controller, go_back_callback=None):
        self.root = root
        self.controller = controller
        self.options = controller.get_all_options("Data/courses.txt","Data/selected_courses.txt")
        self.current_index = 0
        self.go_back_callback = go_back_callback

        root.state("zoomed")  # מסך מלא
        # Configure the window to be responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.title("Timetables")
        
        # Create a navigation bar at the top
        self.create_nav_bar()
        
        # Create the timetable container
        self.create_timetable_container()
        
        # Initial view update
        self.update_view()
    
    def create_nav_bar(self):
        """Create the navigation bar with prev/next buttons and title"""
        nav_frame = tk.Frame(self.root, bg=ModernUI.COLORS["light"])
        nav_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=20)
        
        # Configure the nav frame to be responsive
        for i in range(7):  # 0 to 5
            weight = 1 if i in [1, 5] else 0  # Expand only side spacers
            nav_frame.grid_columnconfigure(i, weight=weight)
        
        # Back button on the far left
        self.back_button = ModernUI.create_rounded_button(
            nav_frame, "<", self.go_back,
            fg_color=ModernUI.COLORS["dark"],  # Dark color for text
            bg_color=ModernUI.COLORS["light"], width=50)
        self.back_button.grid(row=0, column=0, padx=10)
        
        # Previous button
        self.prev_button = ModernUI.create_rounded_button(
            nav_frame, "Prev", self.show_prev,
            bg_color=ModernUI.COLORS["dark"], width=50)
        self.prev_button.grid(row=0, column=2, padx=10)
        
        # Title label (timetable option x of y)
        self.title_label = tk.Label(
            nav_frame, text="",
            font=("Helvetica", 12, "bold"), bg=ModernUI.COLORS["light"])
        self.title_label.grid(row=0, column=3)
        
        # Next button
        self.next_button = ModernUI.create_rounded_button(
            nav_frame, "Next", self.show_next,
            bg_color=ModernUI.COLORS["dark"], width=50)
        self.next_button.grid(row=0, column=4, padx=10)
        
        # Export button (for printing)
        self.export_button = ModernUI.create_rounded_button(
            nav_frame, "Export PDF", self.export_pdf_dialog,
            bg_color=ModernUI.COLORS["dark"], width=100)
        self.export_button.grid(row=0, column=6, padx=10)
    
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
        # self.draw_days_header()
        
        # Scrollable timetable area
        self.canvas = tk.Canvas(self.timetable_container, borderwidth=0, highlightthickness=0, 
                              bg=ModernUI.COLORS["white"])
        self.scrollbar = ttk.Scrollbar(self.timetable_container, orient="vertical", command=self.canvas.yview)
        # def on_mouse_wheel(event):
        #     if str(self.canvas) in self.canvas.tk.call('winfo', 'children', '.'):
        #         self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # self.canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        def on_mouse_wheel(event):
            try:
                if self.canvas.winfo_exists():
                    self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass  # Avoid crash if the canvas is destroyed during the event
        self.canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        self.canvas.bind("<Destroy>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        # Bind the mouse wheel event to scroll the canvas
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
        empty_cell = tk.Label(self.days_header, text="", width=15, height=4, 
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
            # Hide unnecessary UI elements
            self.prev_button.grid_remove()
            self.next_button.grid_remove()
            self.title_label.grid_remove()
            self.days_header.grid_remove()
            self.canvas.grid_remove()
            self.scrollbar.grid_remove()

            # Show a "No timetable available" label
            if not hasattr(self, "no_data_label"):
                self.no_data_label = tk.Label(
                    self.root,
                    text="No timetable available.",
                    font=("Helvetica", 14),
                    bg=ModernUI.COLORS["light"],
                    fg=ModernUI.COLORS["dark"]
                )
                self.no_data_label.grid(row=1, column=0, pady=50)
            else:
                self.no_data_label.grid()
            return

        # If previously shown, hide the no-data label
        if hasattr(self, "no_data_label"):
            self.no_data_label.grid_remove()

        # Show the UI again if it was hidden before
        self.prev_button.grid()
        self.next_button.grid()
        self.title_label.grid()
        self.days_header.grid()
        self.canvas.grid()
        self.scrollbar.grid()
        
        # Update the title
        self.title_label.config(text=f"Timetable Option {self.current_index + 1} of {len(self.options)}")
        
        # Get timetable for this option
        current_timetable = self.options[self.current_index]
        
        # Reset the canvas view to the top
        self.canvas.yview_moveto(0)
        
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

    def save_canvas_as_image(self):
        self.root.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        bbox = (x, y, x + w, y + h)
        temp_image_path = os.path.join(tempfile.gettempdir(), "timetable_capture.png")
        image = ImageGrab.grab(bbox)
        image.save(temp_image_path)

        return temp_image_path
    
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
    
    def go_back(self):
     """Return to the previous page if callback is provided"""
     if self.go_back_callback:
        self.go_back_callback()
 
    # def export_current_timetable_pdf(self):
    #     file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    #     if not file_path:
    #         return

    #     current_timetable = self.options[self.current_index]
    #     slot_map = map_courses_to_slots(current_timetable)

    #     try:
    #         generate_pdf_from_data(file_path, slot_map, title=f"Timetable Option {self.current_index + 1}")
    #         # messagebox.showinfo("Success", f"Timetable exported to {file_path}")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Failed to export PDF: {e}")

    def export_pdf_dialog(self):
        choice = messagebox.askquestion("Export PDF", "Do you want to export all timetable options?\nChoose Yes for all, No for current.")
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        try:
            # export all timetable options to pdf file
            if choice == 'yes':
                doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
                all_elements = []

                for idx, timetable in enumerate(self.options):
                    slot_map = map_courses_to_slots(timetable)
                    title = f"{idx + 1}"
                    # Calling a function that returns elements of a time table
                    elements = generate_pdf_from_data(None, slot_map, title, return_elements=True)
                    all_elements.extend(elements)
                    all_elements.append(PageBreak())

                doc.build(all_elements)
            # export only the current timetable to pdf file
            else:
                current_timetable = self.options[self.current_index]
                slot_map = map_courses_to_slots(current_timetable)
                generate_pdf_from_data(file_path, slot_map, self.current_index + 1)

            os.startfile(file_path) # open the file when done create it

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {e}")


import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import tkinter.scrolledtext as scrolledtext

class ModernUI:
    """Class with modern UI elements and styling"""
    
    # Color palette
    COLORS = {
        "primary": "#3499FF",     # Blue
        "secondary": "#36F6A9",   # Green
        "accent": "#FF1313",      # Red
        "light": "#ecf0f1",       # Light Gray
        "dark": "#2c3e50",        # Dark Blue/Gray
        "white": "#ffffff",       # White
        "gray": "#95a5a6",        # Medium Gray
        "selected": "#d5f5e3"     # Light Green for selected items
    }
    
    @staticmethod
    def create_rounded_button(parent, text, command, bg_color=None, fg_color=None, width=120, height=30):
        """Creates a custom canvas button with rounded corners"""
        if not bg_color:
            bg_color = ModernUI.COLORS["primary"]
        if not fg_color:
            fg_color = ModernUI.COLORS["white"]
            
        frame = tk.Frame(parent, bg=parent["bg"])
        canvas = tk.Canvas(frame, width=width, height=height, bg=parent["bg"], 
                         highlightthickness=0)
        canvas.pack()
        
        # Draw rounded rectangle
        canvas.create_rounded_rectangle = lambda x1, y1, x2, y2, radius, **kwargs: canvas.create_polygon(
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
            smooth=True, **kwargs)
            
        button_shape = canvas.create_rounded_rectangle(0, 0, width, height, 15, 
                                                    fill=bg_color, outline="")
        button_text = canvas.create_text(width//2, height//2, text=text, 
                                       fill=fg_color, font=("Calibri", 10, "bold"))
        
        # Hover effects
        def on_enter(e):
            # Darken the button slightly on hover
            canvas.itemconfig(button_shape, fill=ModernUI.adjust_color(bg_color, -20))
            
        def on_leave(e):
            canvas.itemconfig(button_shape, fill=bg_color)
            
        def on_click(e):
            # Flash effect and execute command
            canvas.itemconfig(button_shape, fill=ModernUI.adjust_color(bg_color, -40))
            parent.after(100, lambda: canvas.itemconfig(button_shape, fill=bg_color))
            command()
            
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<ButtonRelease-1>", on_leave)
        
        return frame
    
    @staticmethod
    def adjust_color(hex_color, amount):
        """Adjusts a hex color by the given amount (positive = lighter, negative = darker)"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def configure_treeview_style():
        """Configures a custom style for treeview"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure the Treeview colors
        style.configure("Treeview", 
                      background=ModernUI.COLORS["white"],
                      foreground=ModernUI.COLORS["dark"],
                      rowheight=25,
                      fieldbackground=ModernUI.COLORS["white"])
        
        # Change selected color
        style.map('Treeview', 
                background=[('selected', ModernUI.COLORS["primary"])],
                foreground=[('selected', ModernUI.COLORS["white"])])
        
        # Configure the header
        style.configure("Treeview.Heading",
                      background=ModernUI.COLORS["light"],
                      foreground=ModernUI.COLORS["dark"],
                      relief="flat",
                      font=('Calibri', 10, 'bold'))
        
        style.map("Treeview.Heading",
                background=[('active', ModernUI.COLORS["gray"])])

class CourseDetailsPanel(tk.Frame):
    """Panel to display detailed course information"""
    
    def __init__(self, parent, bg_color):
        super().__init__(parent, bg=bg_color, padx=10, pady=10)
        
        # Title
        self.title_label = tk.Label(self, text="Course Details", 
                                  font=("Calibri", 14, "bold"),
                                  bg=bg_color, fg=ModernUI.COLORS["dark"])
        self.title_label.pack(anchor="w", pady=(0, 10))
        
        # Content Frame with border
        content_frame = tk.Frame(self, bg=ModernUI.COLORS["white"],
                               highlightbackground=ModernUI.COLORS["gray"],
                               highlightthickness=1, bd=0)
        content_frame.pack(fill="both", expand=True)
        
        # Course details
        self.code_label = tk.Label(content_frame, text="Code: ", font=("Calibri", 10, "bold"),
                                 bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                 anchor="w")
        self.code_label.pack(fill="x", padx=10, pady=(10, 5))
        
        self.name_label = tk.Label(content_frame, text="Name: ", font=("Calibri", 10),
                                 bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                 anchor="w", wraplength=250)
        self.name_label.pack(fill="x", padx=10, pady=2)
        
        self.instructor_label = tk.Label(content_frame, text="Instructor: ", font=("Calibri", 10),
                                       bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                       anchor="w")
        self.instructor_label.pack(fill="x", padx=10, pady=2)
        
        # Schedule details frame
        schedule_frame = tk.Frame(content_frame, bg=ModernUI.COLORS["white"])
        schedule_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(schedule_frame, text="Schedule:", font=("Calibri", 10, "bold"),
               bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"]).pack(anchor="w")
        
        self.lectures_label = tk.Label(schedule_frame, text="• Lectures: ", font=("Calibri", 9),
                                     bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                     anchor="w")
        self.lectures_label.pack(fill="x", padx=(10, 0), pady=1)
        
        self.exercises_label = tk.Label(schedule_frame, text="• Exercises: ", font=("Calibri", 9),
                                      bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                      anchor="w")
        self.exercises_label.pack(fill="x", padx=(10, 0), pady=1)
        
        self.labs_label = tk.Label(schedule_frame, text="• Labs: ", font=("Calibri", 9),
                                 bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                 anchor="w")
        self.labs_label.pack(fill="x", padx=(10, 0), pady=1)
        
        # Action button
        self.add_button_frame = ModernUI.create_rounded_button(
            self, "Add Course", self.add_course, 
            bg_color=ModernUI.COLORS["secondary"], width=200)
        self.add_button_frame.pack(pady=10)
        
        # Reference to the selected course
        self.current_course = None
        
    def update_details(self, course):
        """Update the panel with course details"""
        self.current_course = course
        
        if course:
            self.code_label.config(text=f"Code: {course._code}")
            self.name_label.config(text=f"Name: {course._name}")
            self.instructor_label.config(text=f"Instructor: {course._instructor}")
            
            self.lectures_label.config(text=f"• Lectures: {len(course._lectures)}")
            self.exercises_label.config(text=f"• Exercises: {len(course._exercises)}")
            self.labs_label.config(text=f"• Labs: {len(course._labs)}")
        else:
            self.code_label.config(text="Code: ")
            self.name_label.config(text="Name: ")
            self.instructor_label.config(text="Instructor: ")
            self.lectures_label.config(text="• Lectures: ")
            self.exercises_label.config(text="• Exercises: ")
            self.labs_label.config(text="• Labs: ")
    
    def set_add_callback(self, callback):
        """Set the callback function for the add button"""
        self.add_callback = callback
        
    def add_course(self):
        """Add the current course to selected courses"""
        if self.current_course and hasattr(self, 'add_callback'):
            self.add_callback(self.current_course._code)

class MainPage:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Course Selector")
        self.window.geometry("1200x650")
        self.window.config(bg=ModernUI.COLORS["light"])
        
        # Apply modern styling
        ModernUI.configure_treeview_style()
        
        self.max_courses = 7
        self.selected_course_ids = set()
        self.course_map = {}  # code -> Course object
        
        # Main container with padding
        main_container = tk.Frame(self.window, bg=ModernUI.COLORS["light"], padx=15, pady=15)
        main_container.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg=ModernUI.COLORS["light"])
        header_frame.pack(fill="x", pady=(0, 15))
        
        header_label = tk.Label(header_frame, text="Course Selector", 
                              font=("Calibri", 18, "bold"),
                              bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"])
        header_label.pack(side="left")
        
        # Main content area - with 3 panels
        content_frame = tk.Frame(main_container, bg=ModernUI.COLORS["light"])
        content_frame.pack(fill="both", expand=True)
        
        # Left panel - Course codes list
        left_panel = tk.Frame(content_frame, bg=ModernUI.COLORS["light"], padx=5, pady=5)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Label for courses list
        tk.Label(left_panel, text="Available Courses", 
               font=("Calibri", 12, "bold"),
               bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"]).pack(anchor="w", pady=(0, 5))
        
       
        self.tree_codes = ttk.Treeview(left_panel, columns=("Code"), 
                                    show="headings", selectmode="browse")
        self.tree_codes.heading("Code", text="Course Code")
        self.tree_codes.column("Code", width=150, anchor="center")
        self.tree_codes.pack(fill="both", expand=True)
        
        # Add scrollbar to course codes
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree_codes.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_codes.configure(yscrollcommand=scrollbar.set)
        
        # Middle panel - Course details
        middle_panel = tk.Frame(content_frame, bg=ModernUI.COLORS["light"], width=300)
        middle_panel.pack(side="left", fill="both", padx=5)
        middle_panel.pack_propagate(False)  # Prevent shrinking
        
        self.details_panel = CourseDetailsPanel(middle_panel, ModernUI.COLORS["light"])
        self.details_panel.pack(fill="both", expand=True)
        self.details_panel.set_add_callback(self.add_course_by_code)
        
        # Right panel - Selected courses
        right_panel = tk.Frame(content_frame, bg=ModernUI.COLORS["light"], padx=5, pady=5)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Header for selected courses with counter
        selected_header_frame = tk.Frame(right_panel, bg=ModernUI.COLORS["light"])
        selected_header_frame.pack(fill="x", pady=(0, 5))
        
        self.selected_count_var = tk.StringVar()
        self.selected_count_var.set("Selected Courses (0/7)")
        
        tk.Label(selected_header_frame, textvariable=self.selected_count_var, 
               font=("Calibri", 12, "bold"),
               bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"]).pack(side="left")
        
        # Selected courses treeview
        columns = ("Code", "Name", "Instructor", "Lectures", "Exercises", "Labs")
        self.tree_selected = ttk.Treeview(right_panel, columns=columns, 
                                       show="headings", selectmode="browse")
        for col in columns:
            self.tree_selected.heading(col, text=col)
            if col == "Name":
                self.tree_selected.column(col, width=200, anchor="w")
            else:
                self.tree_selected.column(col, width=80, anchor="center")
        self.tree_selected.pack(fill="both", expand=True)
        
        # Add scrollbar to selected courses
        scrollbar_selected = ttk.Scrollbar(right_panel, orient="vertical", command=self.tree_selected.yview)
        scrollbar_selected.pack(side="right", fill="y")
        self.tree_selected.configure(yscrollcommand=scrollbar_selected.set)
        
        # Footer with buttons
        footer_frame = tk.Frame(main_container, bg=ModernUI.COLORS["light"], pady=10)
        footer_frame.pack(fill="x")
        
        # Create buttons using the custom rounded style
        load_button_frame = ModernUI.create_rounded_button(
            footer_frame, "Load Courses", self.load_courses)
        load_button_frame.pack(side="left", padx=5)
        
        remove_button_frame = ModernUI.create_rounded_button(
            footer_frame, "Remove Selected", self.remove_selected_course,
            bg_color=ModernUI.COLORS["accent"])
        remove_button_frame.pack(side="left", padx=5)
        
        save_button_frame = ModernUI.create_rounded_button(
            footer_frame, "Save Selection", self.save_selection,
            bg_color=ModernUI.COLORS["secondary"])
        save_button_frame.pack(side="right", padx=5)
        
        # === Bindings ===
        self.tree_codes.bind("<ButtonRelease-1>", self.show_course_details)
        self.tree_codes.bind("<Double-1>", self.add_course_from_double_click)
        self.tree_selected.bind("<Double-1>", self.remove_course)
        
        # === Initial load of courses ===
        self.load_courses()

    def load_courses(self):
        courses = self.controller.get_courses()  # מחזיר רשימת Course
        self.course_map = {course._code: course for course in courses}

        for row in self.tree_codes.get_children():
            self.tree_codes.delete(row)

        for course in courses:
            self.tree_codes.insert(
                "", tk.END,
                iid=course._code,
                values=(course._code,)
            )
        
        self.update_selected_count()

    def show_course_details(self, event):
        """Show details of the selected course in the middle panel"""
        item = self.tree_codes.focus()
        if item:
            course = self.course_map.get(item)
            if course:
                self.details_panel.update_details(course)

    def add_course_from_double_click(self, event):
        """Add course to selected list on double-click"""
        item = self.tree_codes.identify_row(event.y)
        if item:
            self.add_course_by_code(item)

    def add_course_by_code(self, course_code):
        """Add a course to the selected courses using its code"""
        if course_code in self.selected_course_ids:
            messagebox.showinfo("Already Selected", "This course is already in your selection.")
            return
            
        if len(self.selected_course_ids) >= self.max_courses:
            messagebox.showwarning("Limit Reached", f"You can select up to {self.max_courses} courses only.")
            return

        if course_code in self.course_map:
            course = self.course_map[course_code]
            self.selected_course_ids.add(course_code)
            
            # Add to selected courses treeview
            lectures = len(course._lectures)
            exercises = len(course._exercises)
            labs = len(course._labs)
            
            self.tree_selected.insert(
                "", tk.END,
                iid=course_code,
                values=(course._code, course._name, course._instructor, lectures, exercises, labs)
            )
            
            # Mark as selected in codes list
            self.tree_codes.item(course_code, tags=("selected",))
            self.tree_codes.tag_configure("selected", background=ModernUI.COLORS["selected"])
            
            # Update counter
            self.update_selected_count()

    def remove_course(self, event):
        """Remove course from selected list on double-click"""
        item = self.tree_selected.focus()
        if item:
            self.remove_course_by_code(item)

    def remove_selected_course(self):
        """Remove the currently selected course from the selected list"""
        item = self.tree_selected.focus()
        if item:
            self.remove_course_by_code(item)
        else:
            messagebox.showinfo("No Selection", "Please select a course to remove.")

    def remove_course_by_code(self, course_code):
        """Remove a course from the selected courses using its code"""
        if course_code in self.selected_course_ids:
            self.tree_selected.delete(course_code)
            self.selected_course_ids.remove(course_code)
            
            # Remove selected tag in codes list
            self.tree_codes.item(course_code, tags=())
            
            # Update counter
            self.update_selected_count()

    def update_selected_count(self):
        """Update the counter showing how many courses are selected"""
        count = len(self.selected_course_ids)
        self.selected_count_var.set(f"Selected Courses ({count}/{self.max_courses})")

    def filter_courses(self, *args):
        """Filter the courses list based on search input"""
        search_text = self.search_var.get().lower()
        
        # Clear the treeview
        for row in self.tree_codes.get_children():
            self.tree_codes.delete(row)
        
        # Add matching courses
        for code, course in self.course_map.items():
            if (search_text in code.lower() or 
                search_text in course._name.lower() or 
                search_text in course._instructor.lower()):
                
                self.tree_codes.insert(
                    "", tk.END,
                    iid=code,
                    values=(code,)
                )
                
                # Re-apply selected tag if needed
                if code in self.selected_course_ids:
                    self.tree_codes.item(code, tags=("selected",))
                    self.tree_codes.tag_configure("selected", background=ModernUI.COLORS["selected"])

    def save_selection(self):
        """Save the current course selection"""
        selected_courses = self.get_selected_courses()
        if not selected_courses:
            messagebox.showinfo("No Courses", "You haven't selected any courses yet.")
            return
            
        # This is a placeholder - you would implement your actual save functionality here
        course_names = [course._name for course in selected_courses]
        message = f"You have selected {len(course_names)} courses:\n\n"
        message += "\n".join([f"- {name}" for name in course_names])
        
        messagebox.showinfo("Selection Saved", message)

    def get_selected_courses(self):
        selected_courses = []
        for item in self.tree_selected.get_children():
            course_code = item  # The iid is the course code
            if course_code in self.course_map:
                selected_courses.append(self.course_map[course_code])
        return selected_courses

    def run(self):
        self.window.mainloop()
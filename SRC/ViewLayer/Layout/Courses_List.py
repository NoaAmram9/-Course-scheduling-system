import tkinter as tk
from tkinter import ttk
from SRC.ViewLayer.Theme.ModernUI import ModernUI

class CourseListPanel(tk.Frame):
    """Panel to display all available courses"""

    def __init__(self, parent, bg_color):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.all_courses = []  # Full unfiltered list
        # Label for courses list
        tk.Label(self, text="Available Courses", 
                 font=("Calibri", 12, "bold"),
                 bg=bg_color, fg=ModernUI.COLORS["dark"]).pack(anchor="w", pady=(0, 5))
    # # Search box
    #     search_frame = tk.Frame(self, bg=bg_color)
    #     search_frame.pack(fill="x", pady=(0, 5))

    #     tk.Label(search_frame, text="Search:", bg=bg_color, fg=ModernUI.COLORS["dark"]).pack(side="left")

    #     self.search_var = tk.StringVar()
    #     search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25)
    #     search_entry.pack(side="left", padx=(5, 0))
    #     self.search_var.trace_add("write", lambda *args: self.filter_courses())
        # Create a frame to hold both Treeview and Scrollbar side by side
        tree_frame = tk.Frame(self, bg=bg_color)
        tree_frame.pack(fill="both", expand=True)
        
          

       

        # Create Treeview for courses
        self.tree_codes = ttk.Treeview(tree_frame, columns=("Code",), 
                                       show="headings", selectmode="browse")
        self.tree_codes.heading("Code", text="Course Code")
        self.tree_codes.column("Code", width=150, anchor="center")
        self.tree_codes.pack(side="left", fill="both", expand=True)

        # Add scrollbar to Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_codes.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_codes.configure(yscrollcommand=scrollbar.set)

        # Course mapping and callbacks
        self.course_map = {}
        self.details_callback = None
        self.add_course_callback = None

        # Bindings
        self.tree_codes.bind("<ButtonRelease-1>", self.on_course_select)
        self.tree_codes.bind("<Double-1>", self.on_course_double_click)

    
    def load_courses(self, courses):
        
        """Load courses into the treeview"""
        # Clear existing items
        for row in self.tree_codes.get_children():
            self.tree_codes.delete(row)
            
        # Store courses in the map
        self.course_map = {course._code: course for course in courses}
        
        # Add courses to the treeview
        for course in courses:
            self.tree_codes.insert(
                "", tk.END,
                iid=course._code,
                values=(course._code,)
            )
        self.all_courses = courses  # Store the full list
        print(f"[DEBUG] Loaded {len(courses)} valid courses.")
    def set_details_callback(self, callback):
        """Set callback function for showing course details"""
        self.details_callback = callback
    
    def set_add_course_callback(self, callback):
        """Set callback function for adding a course"""
        self.add_course_callback = callback
    
    def on_course_select(self, event):
        """Handle course selection event"""
        item = self.tree_codes.focus()
        if item and self.details_callback:
            course = self.course_map.get(item)
            if course:
                self.details_callback(course)
    
    def on_course_double_click(self, event):
        """Handle course double-click event"""
        item = self.tree_codes.identify_row(event.y)
        if item and self.add_course_callback:
            self.add_course_callback(item)
    
    def mark_course_as_selected(self, course_code):
        """Mark a course as selected in the UI"""
        self.tree_codes.item(course_code, tags=("selected",))
        self.tree_codes.tag_configure("selected", background=ModernUI.COLORS["selected"])
    
    def unmark_course_as_selected(self, course_code):
        """Remove selected marking from a course"""
        self.tree_codes.item(course_code, tags=())
    
    def filter_courses(self, *args):
        search_text = self.search_var.get().lower().strip()
        print(f"[DEBUG] Filtering for: '{search_text}'")

        # Clear Treeview
        for row in self.tree_codes.get_children():
            self.tree_codes.delete(row)

        # Filter logic
        if not search_text:
            filtered_courses = self.all_courses
        else:
            filtered_courses = [
                course for course in self.all_courses
                if search_text in course._code.lower()
                or search_text in course._name.lower()
            ]

        # Insert filtered results
        for course in filtered_courses:
            if not self.tree_codes.exists(course._code):  # avoid duplicates
                self.tree_codes.insert(
                    "", tk.END,
                    iid=course._code,
                    values=(course._code,)
                )


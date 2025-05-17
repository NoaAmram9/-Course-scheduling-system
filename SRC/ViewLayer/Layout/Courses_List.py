import tkinter as tk
from tkinter import ttk
from SRC.ViewLayer.Theme.ModernUI import ModernUI

class CourseListPanel(tk.Frame):
    """Panel to display all available courses"""

    def __init__(self, parent, bg_color):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)

        # This will hold all courses for filtering
        self.all_courses = []

        # Simple label at the top of the list
        tk.Label(self, text="Available Courses", 
                 font=("Calibri", 12, "bold"),
                 bg=bg_color, fg=ModernUI.COLORS["dark"]).pack(anchor="w", pady=(0, 5))

        # === Treeview section starts here ===

        # A frame to contain the list and its scrollbar side by side
        tree_frame = tk.Frame(self, bg=bg_color)
        tree_frame.pack(fill="both", expand=True)

        # Treeview showing course codes 
        self.tree_codes = ttk.Treeview(tree_frame, columns=("Code",), 
                                       show="headings", selectmode="browse")
        self.tree_codes.heading("Code", text="Course Code")
        self.tree_codes.column("Code", width=150, anchor="center")
        self.tree_codes.pack(side="left", fill="both", expand=True)

        # Vertical scrollbar 
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_codes.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_codes.configure(yscrollcommand=scrollbar.set)

        # Mapping course codes to actual course objects 
        self.course_map = {}

        # Callback functions to be set externally
        self.details_callback = None
        self.add_course_callback = None

        # Handle single and double clicks
        self.tree_codes.bind("<ButtonRelease-1>", self.on_course_select)
        self.tree_codes.bind("<Double-1>", self.on_course_double_click)

    def load_courses(self, courses):
        """Load courses into the treeview"""

        # Clear anything that was already in there
        for row in self.tree_codes.get_children():
            self.tree_codes.delete(row)

        # Map codes to objects
        self.course_map = {course._code: course for course in courses}

        # Add each course to the list view
        for course in courses:
            self.tree_codes.insert(
                "", tk.END,
                iid=course._code,
                values=(course._code,)
            )

        # Keep the full list for filtering/searching later
        self.all_courses = courses

    def set_details_callback(self, callback):
        """Sets the function to call when a course is selected """
        self.details_callback = callback

    def set_add_course_callback(self, callback):
        """Sets the function to call when a course is double-clicked """
        self.add_course_callback = callback

    def on_course_select(self, event):
        """When a course is selected, call the details function """
        item = self.tree_codes.focus()
        if item and self.details_callback:
            course = self.course_map.get(item)
            if course:
                self.details_callback(course)

    def on_course_double_click(self, event):
        """Double-click = probably wants to add it to schedule"""
        item = self.tree_codes.identify_row(event.y)
        if item and self.add_course_callback:
            self.add_course_callback(item)

    def mark_course_as_selected(self, course_code):
        """Visually mark a course as selected (change background color)"""
        self.tree_codes.item(course_code, tags=("selected",))
        self.tree_codes.tag_configure("selected", background=ModernUI.COLORS["selected"])

    def unmark_course_as_selected(self, course_code):
        """Remove any visual selection on a course"""
        self.tree_codes.item(course_code, tags=())

    def filter_courses(self, *args):
        """Filter the course list based on text input"""
        search_text = self.search_var.get().lower().strip()
        print(f"[DEBUG] Filtering for: '{search_text}'")

        # Start fresh
        for row in self.tree_codes.get_children():
            self.tree_codes.delete(row)

        # If nothing was typed, just show everything
        if not search_text:
            filtered_courses = self.all_courses
        else:
            # Match by code or name 
            filtered_courses = [
                course for course in self.all_courses
                if search_text in course._code.lower()
                or search_text in course._name.lower()
            ]

        # Add only the matching courses
        for course in filtered_courses:
            if not self.tree_codes.exists(course._code):
                self.tree_codes.insert(
                    "", tk.END,
                    iid=course._code,
                    values=(course._code,)
                )

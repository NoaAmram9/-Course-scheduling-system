import tkinter as tk
from tkinter import ttk, messagebox
from SRC.ViewLayer.Theme.ModernUI import ModernUI

class SelectedCoursesPanel(tk.Frame):
    """Panel to display selected/traded courses"""
    def __init__(self, parent, bg_color, max_courses=7):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        
        self.max_courses = max_courses
        self.selected_course_ids = set()
        self.course_map = {}
        self.remove_callback = None
        
        # Header with course count
        selected_header_frame = tk.Frame(self, bg=bg_color)
        selected_header_frame.pack(fill="x", pady=(0, 5))
        
        self.selected_count_var = tk.StringVar()
        self.selected_count_var.set(f"Selected Courses (0/{self.max_courses})")
         # Label for courses list
        tk.Label(self, text="Available Courses", 
                 font=("Calibri", 12, "bold"),
                 bg=bg_color, fg=ModernUI.COLORS["dark"]).pack(anchor="w", pady=(0, 5))
        # tk.Label(selected_header_frame, textvariable=self.selected_count_var, 
        #          font=("Calibri", 12, "bold"),
        #          bg=bg_color, fg=ModernUI.COLORS["dark"]).pack(side="left")
        
        # Frame to contain both the Treeview and its scrollbar
        tree_frame = tk.Frame(self, bg=bg_color)
        tree_frame.pack(fill="both", expand=True)
        
        # Treeview setup
        columns = ("Code", "Name", "Instructor", "Lectures", "Exercises", "Labs")
        self.tree_selected = ttk.Treeview(tree_frame, columns=columns, 
                                          show="headings", selectmode="browse")
        
        for col in columns:
            self.tree_selected.heading(col, text=col)
            if col == "Name":
                self.tree_selected.column(col, width=200, anchor="w")
            else:
                self.tree_selected.column(col, width=80, anchor="center")
        
        self.tree_selected.pack(side="left", fill="both", expand=True)
        
        # Scrollbar placement (to the right of the treeview)
        scrollbar_selected = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_selected.yview)
        scrollbar_selected.pack(side="right", fill="y")
        self.tree_selected.configure(yscrollcommand=scrollbar_selected.set)
        
        # Event binding
        self.tree_selected.bind("<Double-1>", self.on_course_double_click)
    
    def set_course_map(self, course_map):
        """Set the course map reference"""
        self.course_map = course_map
    
    def set_remove_callback(self, callback):
        """Set callback for when a course is removed"""
        self.remove_callback = callback
    
    def add_course(self, course_code):
        """Add a course to the selected courses panel"""
        if course_code in self.selected_course_ids:
            messagebox.showinfo("Already Selected", "This course is already in your selection.")
            return False
            
        if len(self.selected_course_ids) >= self.max_courses:
            messagebox.showwarning("Limit Reached", f"You can select up to {self.max_courses} courses only.")
            return False

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
            
            # Update counter
            self.update_selected_count()
            return True
        
        return False
    
    def on_course_double_click(self, event):
        """Handle double-click on a selected course (to remove it)"""
        item = self.tree_selected.focus()
        if item:
            self.remove_course(item)
    
    def remove_course(self, course_code):
        """Remove a course from the selected courses"""
        if course_code in self.selected_course_ids:
            self.tree_selected.delete(course_code)
            self.selected_course_ids.remove(course_code)
            
            # Update counter
            self.update_selected_count()
            
            # Call the remove callback if set
            if self.remove_callback:
                self.remove_callback(course_code)
            
            return True
        
        return False
    
    def remove_selected_course(self):
        """Remove the currently selected course"""
        item = self.tree_selected.focus()
        if item:
            return self.remove_course(item)
        else:
            messagebox.showinfo("No Selection", "Please select a course to remove.")
            return False
    
    def update_selected_count(self):
        """Update the counter showing how many courses are selected"""
        count = len(self.selected_course_ids)
        self.selected_count_var.set(f"Selected Courses ({count}/{self.max_courses})")
    
    def get_selected_courses(self):
        """Get a list of all selected course objects"""
        selected_courses = []
        for item in self.tree_selected.get_children():
            course_code = item  # The iid is the course code
            if course_code in self.course_map:
                selected_courses.append(self.course_map[course_code])
        return selected_courses
    
    def clear_selection(self):
        """Clear all selected courses"""
        for item in list(self.tree_selected.get_children()):
            self.remove_course(item)
# main_page.py
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from Theme.ModernUI import ModernUI
from Layout.SelectionPage import SelectionPage
class SelectionPage:
    
    def __init__(self, controller):
        self.controller = controller
        self._setup_window()
        self._build_layout()
        self._load_courses()
        
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
import tkinter as tk
from tkinter import messagebox

class CourseManager:
    """
    Logic class that handles interaction between the controller and UI components
    """
    
    def __init__(self, controller, course_list_panel, course_details_panel, selected_courses_panel):
        """
        Initialize with references to controller and UI components
        """
        self.controller = controller
        self.course_list_panel = course_list_panel
        self.course_details_panel = course_details_panel
        self.selected_courses_panel = selected_courses_panel
        
        # Set up component callbacks
        self.course_list_panel.set_details_callback(self.show_course_details)
        self.course_list_panel.set_add_course_callback(self.add_course)
        self.course_details_panel.set_add_callback(self.add_course)
        self.selected_courses_panel.set_remove_callback(self.on_course_removed)
        
        # Load initial courses
        self.load_courses()
    
    def load_courses(self):
        
        
        """Load courses from the controller"""
        courses = self.controller.process_repository_file("Data/courses.txt")
        
        # Create course map
        course_map = {course.code: course for course in courses}
        
        # Update components
        self.course_list_panel.load_courses(courses)
        self.selected_courses_panel.set_course_map(course_map)
    
    def show_course_details(self, course):
        """Show details of a course in the details panel"""
        self.course_details_panel.update_details(course)
    
    def add_course(self, course_code):
        """Add a course to selected courses"""
        success = self.selected_courses_panel.add_course(course_code)
        if success:
            self.course_list_panel.mark_course_as_selected(course_code)
    
    def on_course_removed(self, course_code):
        """Handle when a course is removed from selected courses"""
        self.course_list_panel.unmark_course_as_selected(course_code)
    
    def remove_selected_course(self):
        """Remove the currently selected course"""
        self.selected_courses_panel.remove_selected_course()
    
    def save_selection(self):
        """Save the current course selection"""
        selected_courses = self.selected_courses_panel.get_selected_courses()
        if not selected_courses:
            messagebox.showinfo("No Courses", "You haven't selected any courses yet.")
            return
            
        # This is a placeholder - you would implement your actual save functionality here
        course_names = [course._name for course in selected_courses]
        message = f"You have selected {len(course_names)} courses:\n\n"
        message += "\n".join([f"- {name}" for name in course_names])
        
        # messagebox.showinfo("Selection Saved", message)
        course_code = [course._code for course in selected_courses]
        self.controller.create_selected_courses_file(course_code, "Data/selected_courses.txt")

        
        
    def get_selected_courses(self):
        """Get the list of selected courses"""
        return self.selected_courses_panel.get_selected_courses()
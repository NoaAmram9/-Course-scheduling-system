import tkinter as tk
from tkinter import messagebox

class CourseManager:
    """
    Logic class that handles interaction between the controller and UI components.
    This acts as the middleman that connects user actions with underlying logic.
    """
    
    def __init__(self, controller, course_list_panel, course_details_panel, selected_courses_panel):
        # Initialize with references to the controller and all UI panels
        self.controller = controller
        self.course_list_panel = course_list_panel
        self.course_details_panel = course_details_panel
        self.selected_courses_panel = selected_courses_panel
        
        # Set up callbacks for UI components
        self.course_list_panel.set_details_callback(self.show_course_details)
        self.course_list_panel.set_add_course_callback(self.add_course)
        self.course_details_panel.set_add_callback(self.add_course)
        self.selected_courses_panel.set_remove_callback(self.on_course_removed)
        
        # Load the courses from the file
        self.load_courses()
    
    def load_courses(self):
    
        # Load courses from the repository file using the controller
        courses = self.controller.process_repository_file("Data/courses.txt")
        
        # Build a quick-access dictionary by course code
        course_map = {course.code: course for course in courses}
        
        # Send the full list to the list panel
        self.course_list_panel.load_courses(courses)
        
        # Also send the map to the selected panel 
        self.selected_courses_panel.set_course_map(course_map)
    
    def show_course_details(self, course):
        """Display full details of a given course in the details panel"""
        self.course_details_panel.update_details(course)
    
    def add_course(self, course_code):
        """
        Try to add a course to the selection list.
        If it works, mark it visually as selected in the list.
        """
        success = self.selected_courses_panel.add_course(course_code)
        if success:
            self.course_list_panel.mark_course_as_selected(course_code)
    
    def on_course_removed(self, course_code):
        """Callback from selected panel: course was removed, so unmark it in the list"""
        self.course_list_panel.unmark_course_as_selected(course_code)
    
    def remove_selected_course(self):
        """Manually remove whichever course is selected in the 'selected' panel"""
        self.selected_courses_panel.remove_selected_course()
    
    def save_selection(self):
        """
        Save the user's selected courses to a file.
        If none were selected, show a message box instead.
        """
        selected_courses = self.selected_courses_panel.get_selected_courses()
        
        # Show a friendly reminder if the user hasn't picked anything
        if not selected_courses:
            messagebox.showinfo("No Courses", "You haven't selected any courses yet.")
            return False
        
        # Optional: build a string for logging or feedback
        course_names = [course._name for course in selected_courses]
        message = f"You have selected {len(course_names)} courses:\n\n"
        message += "\n".join([f"- {name}" for name in course_names])
        
        # Save the selected course codes to a file using the controller
        course_codes = [course._code for course in selected_courses]
        self.controller.create_selected_courses_file(course_codes, "Data/selected_courses.txt")
        return True
        
    def get_selected_courses(self):
        """Return the full list of selected Course objects"""
        return self.selected_courses_panel.get_selected_courses()

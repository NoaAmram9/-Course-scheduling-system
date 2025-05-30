from PyQt5.QtWidgets import QMessageBox

class CourseManagerQt5:
    """Logic class that handles interaction between the controller and UI components."""
    
    def __init__(self, controller, course_list_panel, course_details_panel, selected_courses_panel):
        self.controller = controller
        self.course_list_panel = course_list_panel
        self.course_details_panel = course_details_panel  
        self.selected_courses_panel = selected_courses_panel
        
        # Connect signals -
        self.course_list_panel.course_selected.connect(self.show_course_details)
        self.course_list_panel.course_double_clicked.connect(self.add_course)
        self.course_details_panel.add_course_requested.connect(self.add_course) 
        self.selected_courses_panel.course_removed.connect(self.on_course_removed)
        
        # Load courses
        self.load_courses()
    
    def load_courses(self):
        """Load courses from the repository file using the controller"""
        courses = self.controller.process_repository_file("Data/courses.txt")
        course_map = {course.code: course for course in courses}
        
        self.course_list_panel.load_courses(courses)
        self.selected_courses_panel.set_course_map(course_map)
    
    def show_course_details(self, course):
        """Display full details of a given course in the details panel"""
        self.course_details_panel.update_details(course)
    
    def add_course(self, course_code):
        """Try to add a course to the selection list"""
        success = self.selected_courses_panel.add_course(course_code)
        if success:
            self.course_list_panel.mark_course_as_selected(course_code)
    
    def on_course_removed(self, course_code):
        """Callback from selected panel: course was removed"""
        self.course_list_panel.unmark_course_as_selected(course_code)
    
    def remove_selected_course(self):
        """Manually remove whichever course is selected in the 'selected' panel"""
        self.selected_courses_panel.remove_selected_course()
    
    def save_selection(self):
        """Save the user's selected courses to a file"""
        selected_courses = self.selected_courses_panel.get_selected_courses()
        
        if not selected_courses:
            QMessageBox.information(None, "No Courses", "You haven't selected any courses yet.")
            return False
        
        course_names = [course._name for course in selected_courses]
        message = f"You have selected {len(course_names)} courses:\n\n"
        message += "\n".join([f"- {name}" for name in course_names])
        
        course_codes = [course._code for course in selected_courses]
        self.controller.create_selected_courses_file(course_codes, "Data/selected_courses.txt")
        return True
    
    def get_selected_courses(self):
        """Return the full list of selected Course objects"""
        return self.selected_courses_panel.get_selected_courses()
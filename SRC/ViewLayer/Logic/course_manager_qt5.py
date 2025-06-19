from PyQt5.QtWidgets import QMessageBox

from SRC.Models import Course
from SRC.ViewLayer.Layout.MainPage.AddCourseDialog import AddCourseDialog

from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class CourseManagerQt5:
    """Logic class that handles interaction between the controller and UI components."""

    def __init__(self, controller,Data, course_list_panel, course_details_panel, selected_courses_panel):
        self.controller = controller
        self.course_list_panel = course_list_panel
        self.course_details_panel = course_details_panel  
        self.selected_courses_panel = selected_courses_panel
        self.Data = Data
        # Connect signals -
        self.course_list_panel.course_selected.connect(self.show_course_details)
        self.course_list_panel.course_double_clicked.connect(self.add_course)
        self.course_details_panel.add_course_requested.connect(self.add_course) 
        self.selected_courses_panel.course_removed.connect(self.on_course_removed)
        self.add_course_button = ModernUIQt5.create_button("Add Course")
        self.add_course_button.setObjectName("UploadButton")
        self.add_course_button.clicked.connect(self.show_add_course_dialog)
        self.delete_course_button = ModernUIQt5.create_button("Delete Course")
        self.delete_course_button.setObjectName("DeleteButton")
        self.delete_course_button.clicked.connect(self.delete_selected_course)

        buttons_layout = self.course_details_panel.layout().itemAt(
            self.course_details_panel.layout().count() - 1
        ).layout()

        buttons_layout.addWidget(self.add_course_button)
        buttons_layout.addWidget(self.delete_course_button)

        # Load courses
        self.load_courses()
    
    def load_courses(self):
        """Load courses from the repository file using the controller"""
        courses = self.Data
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
        
        course_codes = [course._code for course in selected_courses]
        self.controller.create_selected_courses_file(course_codes, "Data/selected_courses.txt")
        return True
    
    def get_selected_courses(self):
        """Return the full list of selected Course objects"""
        return self.selected_courses_panel.get_selected_courses()
    
    def show_add_course_dialog(self):
        if not hasattr(self, "add_course_dialog"):
            self.add_course_dialog = AddCourseDialog(self.course_details_panel)  # Use parent window
            self.add_course_dialog.course_added.connect(self.on_new_course_added)

        self.add_course_dialog.clear_form()
        self.add_course_dialog.exec_()

    def on_new_course_added(self, course: Course):
        if not course or not course.code or not course.name:
            print("No valid course received. Skipping.")
            return
        # Add course to internal list
        self.Data.append(course)
        # Reload the course list panel with updated data
        self.course_list_panel.load_courses(self.Data)
        # Update selected_courses_panel map if needed
        self.selected_courses_panel.set_course_map({c.code: c for c in self.Data})
        # Log
        print(f"New course added: {course.code} - {course.name}")
        
    def delete_selected_course(self):
        course = self.course_details_panel.get_current_course()  # You must implement this method if it doesn't exist

        if not course:
            QMessageBox.warning(None, "No Selection", "Please select a course to delete.")
            return

        confirm = QMessageBox.question(
            None,
            "Confirm Deletion",
            f"Are you sure you want to delete the course '{course.name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            # Remove from internal data
            self.Data = [c for c in self.Data if c.code != course.code]

            # Reload UI
            self.course_list_panel.load_courses(self.Data)
            self.selected_courses_panel.set_course_map({c.code: c for c in self.Data})
            

            print(f"Deleted course: {course.code} - {course.name}")


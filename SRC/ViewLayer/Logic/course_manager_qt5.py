# from PyQt5.QtWidgets import QMessageBox

# from SRC.Models import Course
# from SRC.ViewLayer.Layout.MainPage.AddCourseDialog import AddCourseDialog

# from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

# class CourseManagerQt5:
#     """Logic class that handles interaction between the controller and UI components."""

#     def __init__(self, controller,Data, course_list_panel, course_details_panel, selected_courses_panel):
#         self.controller = controller
#         self.course_list_panel = course_list_panel
#         self.course_details_panel = course_details_panel  
#         self.selected_courses_panel = selected_courses_panel
#         self.Data = Data
#         # Connect signals -
#         self.course_list_panel.course_selected.connect(self.show_course_details)
#         self.course_list_panel.course_double_clicked.connect(self.add_course)
#         self.course_details_panel.add_course_requested.connect(self.add_course) 
#         self.selected_courses_panel.course_removed.connect(self.on_course_removed)
#         self.add_course_button = ModernUIQt5.create_button("Add Course")
#         self.add_course_button.setObjectName("UploadButton")
#         self.add_course_button.clicked.connect(self.show_add_course_dialog)
#         self.delete_course_button = ModernUIQt5.create_button("Delete Course")
#         self.delete_course_button.setObjectName("DeleteButton")
#         self.delete_course_button.clicked.connect(self.delete_selected_course)

#         buttons_layout = self.course_details_panel.layout().itemAt(
#             self.course_details_panel.layout().count() - 1
#         ).layout()

#         buttons_layout.addWidget(self.add_course_button)
#         buttons_layout.addWidget(self.delete_course_button)

#         # Load courses
#         self.load_courses()
    
#     def load_courses(self):
#         """Load courses from the repository file using the controller"""
#         courses = self.Data
#         course_map = {course.code: course for course in courses}
        
#         self.course_list_panel.load_courses(courses)
#         self.selected_courses_panel.set_course_map(course_map)
    
#     def show_course_details(self, course):
#         """Display full details of a given course in the details panel"""
#         self.course_details_panel.update_details(course)
    
#     def add_course(self, course_code):
#         """Try to add a course to the selection list"""
#         success = self.selected_courses_panel.add_course(course_code)
#         if success:
#             self.course_list_panel.mark_course_as_selected(course_code)
    
#     def on_course_removed(self, course_code):
#         """Callback from selected panel: course was removed"""
#         self.course_list_panel.unmark_course_as_selected(course_code)
    
#     def remove_selected_course(self):
#         """Manually remove whichever course is selected in the 'selected' panel"""
#         self.selected_courses_panel.remove_selected_course()
    
#     def save_selection(self):
#         """Save the user's selected courses to a file"""
#         selected_courses = self.selected_courses_panel.get_selected_courses()
        
#         if not selected_courses:
#             QMessageBox.information(None, "No Courses", "You haven't selected any courses yet.")
#             return False
        
#         course_codes = [course._code for course in selected_courses]
#         self.controller.create_selected_courses_file(course_codes, "Data/selected_courses.txt")
#         return True
    
#     def get_selected_courses(self):
#         """Return the full list of selected Course objects"""
#         return self.selected_courses_panel.get_selected_courses()
    
#     def show_add_course_dialog(self):
#         if not hasattr(self, "add_course_dialog"):
#             self.add_course_dialog = AddCourseDialog(self.course_details_panel)  # Use parent window
#             self.add_course_dialog.course_added.connect(self.on_new_course_added)

#         self.add_course_dialog.clear_form()
#         self.add_course_dialog.exec_()

#     def on_new_course_added(self, course: Course):
#         if not course or not course.code or not course.name:
#             print("No valid course received. Skipping.")
#             return
#         # Add course to internal list
#         self.Data.append(course)
#         # Reload the course list panel with updated data
#         self.course_list_panel.load_courses(self.Data)
#         # Update selected_courses_panel map if needed
#         self.selected_courses_panel.set_course_map({c.code: c for c in self.Data})
#         # Log
#         print(f"New course added: {course.code} - {course.name}")
        
    
        
#     def delete_selected_course(self):
#         course = self.course_details_panel.get_current_course()  # make sure this returns the selected course

#         if not course:
#             QMessageBox.warning(None, "No Selection", "Please select a course to delete.")
#             return

#         confirm = QMessageBox.question(
#             None,
#             "Confirm Deletion",
#             f"Are you sure you want to delete the course '{course.name}'?",
#             QMessageBox.Yes | QMessageBox.No,
#         )

#         if confirm == QMessageBox.Yes:
#             # Modify the existing list in place
#             self.Data[:] = [c for c in self.Data if c.code != course.code]

#             # Reload UI components
#             self.course_list_panel.load_courses(self.Data)
#             self.selected_courses_panel.set_course_map({c.code: c for c in self.Data})

#             print(f"Deleted course: {course.code} - {course.name}")

from PyQt5.QtWidgets import QMessageBox

from SRC.Models import Course
from SRC.ViewLayer.Layout.MainPage.AddCourseDialog import AddCourseDialog
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class CourseManagerQt5:
    """Logic class that handles interaction between the controller and UI components."""

    def __init__(self, controller, Data, course_list_panel, course_details_panel, selected_courses_panel):
        self.controller = controller
        self.course_list_panel = course_list_panel
        self.course_details_panel = course_details_panel  
        self.selected_courses_panel = selected_courses_panel
        self.Data = Data
        
        # Connect signals
        self.course_list_panel.course_selected.connect(self.show_course_details)
        self.course_list_panel.course_double_clicked.connect(self.add_course)
        self.course_details_panel.add_course_requested.connect(self.add_course) 
        self.selected_courses_panel.course_removed.connect(self.on_course_removed)
        
        # Create buttons
        self.add_course_button = ModernUIQt5.create_button("Add Course")
        self.add_course_button.setObjectName("UploadButton")
        self.add_course_button.clicked.connect(self.show_add_course_dialog)
        
        self.delete_course_button = ModernUIQt5.create_button("Delete Course")
        self.delete_course_button.setObjectName("DeleteButton")
        self.delete_course_button.clicked.connect(self.delete_selected_course)
        
        # # Database management buttons
        # self.refresh_from_db_button = ModernUIQt5.create_button("Refresh from DB")
        # self.refresh_from_db_button.setObjectName("RefreshButton")
        # self.refresh_from_db_button.clicked.connect(self.refresh_from_database)
        
        # self.sync_to_db_button = ModernUIQt5.create_button("Sync to DB")
        # self.sync_to_db_button.setObjectName("SyncButton")
        # self.sync_to_db_button.clicked.connect(self.sync_to_database)

        # Add buttons to layout
        buttons_layout = self.course_details_panel.layout().itemAt(
            self.course_details_panel.layout().count() - 1
        ).layout()

        buttons_layout.addWidget(self.add_course_button)
        buttons_layout.addWidget(self.delete_course_button)
        
        # # Add database buttons only if database is enabled
        # if self.controller.use_database:
        #     buttons_layout.addWidget(self.refresh_from_db_button)
        #     buttons_layout.addWidget(self.sync_to_db_button)

        # Load courses
        self.load_courses()
    
    def load_courses(self):
        """Load courses from the repository file using the controller"""
        courses = self.Data
        course_map = {course.code: course for course in courses}
        
        self.course_list_panel.load_courses(courses)
        self.selected_courses_panel.set_course_map(course_map)
    
    def refresh_from_database(self):
        """Refresh courses from database"""
        if not self.controller.use_database:
            QMessageBox.warning(None, "Database Disabled", "Database is not enabled for this session.")
            return
        
        try:
            # Get courses from database
            db_courses = self.controller.get_courses_from_database()
            
            if not db_courses:
                QMessageBox.information(None, "No Data", "No courses found in database.")
                return
            
            # Update internal data
            self.Data.clear()
            self.Data.extend(db_courses)
            
            # Reload UI
            self.load_courses()
            
         
            
        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Failed to load from database:\n{str(e)}")
    
    def sync_to_database(self):
        """Sync current courses to database"""
        if not self.controller.use_database:
            
            return
        
        try:
            # Clear database and import current courses
            self.controller.clear_database()
            imported_count, errors = self.controller.db_manager.import_courses_from_list(self.Data)
            
            if errors:
                error_msg = f"Synced {imported_count} courses but encountered {len(errors)} errors:\n"
                error_msg += "\n".join(str(error) for error in errors[:5])  # Show first 5 errors
                if len(errors) > 5:
                    error_msg += f"\n... and {len(errors) - 5} more errors"
                
            
                
        except Exception as e:
            QMessageBox.critical(None, "Sync Error", f"Failed to sync to database:\n{str(e)}")

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
        self.refresh_from_database()
        # self.sync_to_database()
        return True
    
    def get_selected_courses(self):
        """Return the full list of selected Course objects"""
        return self.selected_courses_panel.get_selected_courses()
    
    def show_add_course_dialog(self):
        if not hasattr(self, "add_course_dialog"):
            self.add_course_dialog = AddCourseDialog(self.course_details_panel)
            self.add_course_dialog.course_added.connect(self.on_new_course_added)

        self.sync_to_database()
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
        
        # Save to database if enabled
        if self.controller.use_database:
            try:
                imported_count, errors = self.controller.db_manager.import_courses_from_list([course])
                if errors:
                    print(f"Warning: Errors saving new course to database: {errors}")
                else:
                    print(f"New course saved to database: {course.code} - {course.name}")
            except Exception as e:
                print(f"Error saving new course to database: {e}")
        
        print(f"New course added: {course.code} - {course.name}")
        
    def delete_selected_course(self):
        course = self.course_details_panel.get_current_course()

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
            # Delete from database first if enabled
            if self.controller.use_database:
                try:
                    success = self.controller.delete_course_from_database(course.code, course.name)
                    if success:
                        print(f"Course deleted from database: {course.code}")
                    else:
                        print(f"Course not found in database: {course.code}")
                except Exception as e:
                    QMessageBox.warning(None, "Database Warning", 
                                      f"Course deleted from local data but failed to delete from database:\n{str(e)}")
            
            # Modify the existing list in place
            self.Data[:] = [c for c in self.Data if c.code != course.code]

            # Reload UI components
            self.course_list_panel.load_courses(self.Data)
            self.selected_courses_panel.set_course_map({c.code: c for c in self.Data})

            print(f"Deleted course: {course.code} - {course.name}")

    def get_database_info(self):
        """Get and display database information"""
        if not self.controller.use_database:
            QMessageBox.information(None, "Database Disabled", "Database is not enabled for this session.")
            return
        
        try:
            stats = self.controller.get_database_stats()
            info_msg = f"Database Statistics:\n\n"
            info_msg += f"Total courses: {stats.get('total_courses', 0)}\n"
            info_msg += f"Total lessons: {stats.get('total_lessons', 0)}\n"
            
            semester_counts = stats.get('courses_by_semester', {})
            if semester_counts:
                info_msg += "\nCourses by semester:\n"
                for semester, count in sorted(semester_counts.items()):
                    info_msg += f"  Semester {semester}: {count} courses\n"
            
            QMessageBox.information(None, "Database Info", info_msg)
            
        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Failed to get database info:\n{str(e)}")

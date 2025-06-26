from PyQt5.QtWidgets import QMessageBox

from SRC.Models import Course
from SRC.ViewLayer.Layout.MainPage.AddCourseDialog import AddCourseDialog
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class MainPageLogic:
    """LOGIC Layer - Handles business logic and coordinates between VIEW and CONTROLLER"""

    def __init__(self, controller, Data, course_list_panel, details_panel, selected_courses_panel, main_view=None):
        self.controller = controller
        self.course_list_panel = course_list_panel
        self.details_panel = details_panel  
        self.selected_courses_panel = selected_courses_panel
        self.Data = Data
        self.main_view = main_view  # Reference to VIEW layer
        
        # Business logic state
        self.max_courses = 7
        self.selected_course_ids = set()
        self.course_map = {}
        self.previous_constraints = []
        
        self._connect_signals()
        self._setup_ui_buttons()
        
    def _connect_signals(self):
        """Connect UI signals to logic handlers"""
        self.course_list_panel.course_selected.connect(self.show_course_details)
        self.course_list_panel.course_double_clicked.connect(self.add_course)
        self.details_panel.add_course_requested.connect(self.add_course) 
        self.selected_courses_panel.course_removed.connect(self.on_course_removed)
        
    def _setup_ui_buttons(self):
        """Setup additional UI buttons in the details panel"""
        # Create buttons
        self.add_course_button = ModernUIQt5.create_button("Add Course")
        self.add_course_button.setObjectName("UploadButton")
        self.add_course_button.clicked.connect(self.show_add_course_dialog)
        
        self.delete_course_button = ModernUIQt5.create_button("Delete Course")
        self.delete_course_button.setObjectName("DeleteButton")
        self.delete_course_button.clicked.connect(self.delete_selected_course)

        # Add buttons to details panel layout
        buttons_layout = self.details_panel.layout().itemAt(
            self.details_panel.layout().count() - 1
        ).layout()

        buttons_layout.addWidget(self.add_course_button)
        buttons_layout.addWidget(self.delete_course_button)

    # ===========================
    # MAIN BUSINESS LOGIC METHODS
    # ===========================
    
    def load_courses(self):
        """Load courses from data source - Business Logic"""
        courses = self.Data
        self.course_map = {course.code: course for course in courses}
        
        # Update UI components
        self.course_list_panel.load_courses(courses)
        self.selected_courses_panel.set_course_map(self.course_map)
    
    def show_course_details(self, course):
        """Display course details - Business Logic"""
        self.details_panel.update_details(course)
    
    def add_course(self, course_code):
        """Add course to selection - Business Logic"""
        success = self.selected_courses_panel.add_course(course_code)
        if success:
            self.course_list_panel.mark_course_as_selected(course_code)
            self.selected_course_ids.add(course_code)
    
    def on_course_removed(self, course_code):
        """Handle course removal - Business Logic"""
        self.course_list_panel.unmark_course_as_selected(course_code)
        self.selected_course_ids.discard(course_code)
    
    def save_selection(self):
        """Save selected courses - Business Logic"""
        selected_courses = self.selected_courses_panel.get_selected_courses()
        
        if not selected_courses:
            if self.main_view:
                self.main_view.show_info_dialog("No Courses", "You haven't selected any courses yet.")
            return False
        
        course_codes = [course._code for course in selected_courses]
        self.controller.create_selected_courses_file(course_codes, "Data/selected_courses.txt")
        return True
    
    def get_selected_courses(self):
        """Get selected courses - Business Logic"""
        return self.selected_courses_panel.get_selected_courses()

    # ===========================
    # ACTION HANDLERS - Called by VIEW layer
    # ===========================
    
    def handle_back(self):
        """Handle back action - Business Logic"""
        try:
            if hasattr(self, 'parent_controller') and self.parent_controller:
                self.main_view.hide()
                self.parent_controller.show_start_page()
            else:
                # Fallback: create new start page
                self.main_view.close()
                from SRC.ViewLayer.View.StartPage import StartPageView
                from SRC.ViewLayer.Logic.StartPageController import StartPageController
                
                start_view = StartPageView()
                start_controller = StartPageController(start_view)
                start_view.show()
                
        except Exception as e:
            print(f"Error going back to start: {e}")
    
    def handle_time_constraints(self):
        """Handle time constraints action - Business Logic"""
        if self.main_view:
            self.main_view.show_time_constraints_dialog(self.previous_constraints)
    
    def apply_time_constraints(self, constraints, dialog=None):
        """Apply time constraints - Business Logic"""
        self.previous_constraints = constraints
        self.controller.apply_time_constraints(self.previous_constraints)
        if dialog:
            dialog.close()
    
    def handle_auto_generate(self):
        """Handle auto-generate schedules - Business Logic"""
        if self.save_selection():
            # Save courses to file
            self.controller.save_courses_to_file("Data/All_Courses.xlsx", self.Data)
            
            # Show timetables page
            if self.main_view:
                self.main_view.show_timetables_page()
    
    def handle_manual_schedule(self):
        """Handle manual schedule creation - Business Logic"""
        if self.save_selection():
            if self.main_view:
                self.main_view.show_manual_schedule_page()
    
    def handle_close_event(self):
        """Handle application close - Business Logic"""
        if self.main_view:
            if self.main_view.show_confirmation_dialog('Exit', 'Are you sure you want to exit?'):
                # Save data before closing
                self.controller.save_courses_to_file("Data/All_Courses.xlsx", self.Data)
                self.controller.handle_exit()
                return True
        return False

    # ===========================
    # COURSE MANAGEMENT LOGIC
    # ===========================
    
    def show_add_course_dialog(self):
        """Show add course dialog - Business Logic"""
        if not hasattr(self, "add_course_dialog"):
            self.add_course_dialog = AddCourseDialog(self.details_panel)
            self.add_course_dialog.course_added.connect(self.on_new_course_added)

        self.sync_to_database()
        self.add_course_dialog.clear_form()
        self.add_course_dialog.exec_()

    def on_new_course_added(self, course: Course):
        """Handle new course addition - Business Logic"""
        if not course or not course.code or not course.name:
            print("No valid course received. Skipping.")
            return
        
        # Add course to internal list
        self.Data.append(course)
        
        # Reload the course list panel with updated data
        self.course_list_panel.load_courses(self.Data)
        
        # Update course map and selected courses panel
        self.course_map = {c.code: c for c in self.Data}
        self.selected_courses_panel.set_course_map(self.course_map)
        
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
        """Delete selected course - Business Logic"""
        course = self.details_panel.get_current_course()

        if not course:
            if self.main_view:
                self.main_view.show_info_dialog("No Selection", "Please select a course to delete.")
            return

        if self.main_view:
            if not self.main_view.show_confirmation_dialog(
                "Confirm Deletion", 
                f"Are you sure you want to delete the course '{course.name}'?"
            ):
                return

        # Delete from database first if enabled
        if self.controller.use_database:
            try:
                success = self.controller.delete_course_from_database(course.code, course.name)
                if success:
                    print(f"Course deleted from database: {course.code}")
                else:
                    print(f"Course not found in database: {course.code}")
            except Exception as e:
                if self.main_view:
                    self.main_view.show_info_dialog("Database Warning", 
                                  f"Course deleted from local data but failed to delete from database:\n{str(e)}")
        
        # Remove from internal data
        self.Data[:] = [c for c in self.Data if c.code != course.code]

        # Update UI components
        self.course_list_panel.load_courses(self.Data)
        self.course_map = {c.code: c for c in self.Data}
        self.selected_courses_panel.set_course_map(self.course_map)
        
        # Remove from selected courses if it was selected
        self.selected_course_ids.discard(course.code)

        print(f"Deleted course: {course.code} - {course.name}")

    # ===========================
    # DATABASE OPERATIONS
    # ===========================
    
    def refresh_from_database(self):
        """Refresh courses from database - Business Logic"""
        if not self.controller.use_database:
            if self.main_view:
                self.main_view.show_info_dialog("Database Disabled", "Database is not enabled for this session.")
            return
        
        try:
            # Get courses from database
            db_courses = self.controller.get_courses_from_database()
            
            if not db_courses:
                if self.main_view:
                    self.main_view.show_info_dialog("No Data", "No courses found in database.")
                return
            
            # Update internal data
            self.Data.clear()
            self.Data.extend(db_courses)
            
            # Reload UI
            self.load_courses()
            
        except Exception as e:
            if self.main_view:
                self.main_view.show_info_dialog("Database Error", f"Failed to load from database:\n{str(e)}")
    
    def sync_to_database(self):
        """Sync current courses to database - Business Logic"""
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
                
                if self.main_view:
                    self.main_view.show_info_dialog("Sync Warning", error_msg)
                
        except Exception as e:
            if self.main_view:
                self.main_view.show_info_dialog("Sync Error", f"Failed to sync to database:\n{str(e)}")

    def get_database_info(self):
        """Get and display database information - Business Logic"""
        if not self.controller.use_database:
            if self.main_view:
                self.main_view.show_info_dialog("Database Disabled", "Database is not enabled for this session.")
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
            
            if self.main_view:
                self.main_view.show_info_dialog("Database Info", info_msg)
            
        except Exception as e:
            if self.main_view:
                self.main_view.show_info_dialog("Database Error", f"Failed to get database info:\n{str(e)}")

    # ===========================
    # DEPRECATED/LEGACY METHODS - For backwards compatibility
    # ===========================
    
    def remove_selected_course(self):
        """Legacy method - remove selected course"""
        self.selected_courses_panel.remove_selected_course()
        
    def go_back_to_start(self):
        """Legacy method - redirect to handle_back"""
        return self.handle_back()
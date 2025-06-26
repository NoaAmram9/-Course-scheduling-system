from PyQt5.QtWidgets import QMessageBox
from SRC.ViewLayer.View.MainPage import MainPageView as MainPageQt5
from SRC.ViewLayer.View.LandPageView import LandPageView
from SRC.ViewLayer.Logic.LandPageController import LandPageController
from SRC.Controller.FileController import FileController
import os

class StartPageController:
    def __init__(self, view):
        self.view = view
        self.file_controller = None
        self.upload_view = None
        self.upload_logic = None
        self.main_page = None
        
        # Keep a list of all windows to prevent garbage collection
        self.windows = []
        
        # Connect signals
        self.view.upload_new_file.connect(self.handle_upload_new_file)
        self.view.continue_existing.connect(self.handle_continue_existing)
    
    def handle_upload_new_file(self):
        """Handle uploading a new file - open the original upload page"""
        try:
            # Create and show the original upload page
            self.upload_view = LandPageView()
            self.upload_logic = LandPageController(self.upload_view, parent_controller=self)
            
            # Add to windows list to prevent garbage collection
            self.windows.append(self.upload_view)
            self.windows.append(self.upload_logic)
            
            # Set window properties
            self.upload_view.setWindowTitle("Upload File")
            self.upload_view.resize(600, 400)
            self.upload_view.show()
            
            # Hide the current view after the new one is shown
            self.view.hide()
            
            print("Upload page opened successfully!")
            
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to open upload page:\n{str(e)}")
            print(f"Debug - Error details: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_continue_existing(self):
        """Handle continuing with existing database"""
        try:
            # Check if database exists and has data
            if not self.check_database_exists():
                QMessageBox.warning(
                    self.view, 
                    "No Database Found", 
                    "No existing database found. Please upload a file first."
                )
                return
            
            # Create file controller for database access
            db_path = "Data/courses.db"  # התאם לפי המיקום שלך
            self.file_controller = FileController(
                file_type=".xlsx", 
                filePath=db_path, 
                use_database=True
            )
            
            # Get courses from database
            courses = self.get_courses_from_database()
            
            if not courses:
                QMessageBox.information(
                    self.view, 
                    "Empty Database", 
                    "The database is empty. Please upload a file first."
                )
                return
            
            # Create callback function for returning to start page
            def return_to_start():
                """Callback function to return to start page"""
                if self.main_page:
                    self.main_page.hide()
                self.show_start_page()
            
            # Open main page with existing data and callback
            self.main_page = MainPageQt5(
                Data=courses, 
                controller=self.file_controller, 
                filePath=db_path,
                go_back_callback=return_to_start  # Pass the callback function
            )
            
            # Add to windows list to prevent garbage collection
            self.windows.append(self.main_page)
            
            # Set up the course manager with parent controller reference
            if hasattr(self.main_page, 'course_manager'):
                self.main_page.course_manager.parent_controller = self
            
            self.main_page.show()
            self.main_page.setWindowTitle("Main Page")
            self.main_page.resize(1200, 650)  # Match the original size
            
            # Hide the current view
            self.view.hide()
            
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Failed to load existing database:\n{str(e)}")
            print(f"Debug - Error details: {e}")
            import traceback
            traceback.print_exc()
    
    def check_database_exists(self):
        """Check if database file exists"""
        try:
            # חפש את המסד נתונים במיקומים אפשריים
            possible_paths = [
                "Data/courses.db",
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Data', 'courses.db'),
                "courses.db"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return True
            return False
            
        except Exception:
            return False
    
    def show_start_page(self):
        """Show the start page again"""
        self.view.show()
        
        # Hide other windows
        if self.upload_view:
            self.upload_view.hide()
        if self.main_page:
            self.main_page.hide()
    
    def get_courses_from_database(self):
        """Get courses from database"""
        try:
            if self.file_controller:
                # נניח שיש לך פונקציה בFileController לקבל את כל הקורסים מהמסד נתונים
                courses = self.file_controller.get_courses_from_database()
                return courses
            return []
            
        except Exception as e:
            print(f"Error getting courses from database: {e}")
            return []
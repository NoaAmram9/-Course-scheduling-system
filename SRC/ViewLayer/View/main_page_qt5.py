import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Logic.course_manager_qt5 import CourseManagerQt5
from SRC.ViewLayer.Layout.course_list_panel_qt5 import CourseListPanelQt5
from SRC.ViewLayer.Layout.course_details_panel_qt5 import CourseDetailsPanelQt5
from SRC.ViewLayer.Layout.selected_courses_panel_qt5 import SelectedCoursesPanelQt5
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class MainPageQt5(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.max_courses = 7
        self.selected_course_ids = set()
        self.course_map = {}
        
        self.init_ui()
        self.setup_course_manager()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Course Selector")
        self.setGeometry(100, 100, 1200, 650)
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header
        self.create_header(main_layout)
        
        # Content area with 3 panels
        self.create_content_area(main_layout)
        
        # Footer with buttons
        self.create_footer(main_layout)
        
    def create_header(self, parent_layout):
        """Create the header section"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header_label = QLabel("Course Selector")
        header_label.setObjectName("headerLabel")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        parent_layout.addWidget(header_widget)
        
    def create_content_area(self, parent_layout):
        """Create the main content area with 3 panels"""
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel - Course List (30% width)
        self.course_list_panel = CourseListPanelQt5()
        self.course_list_panel.setMinimumWidth(300)
        content_layout.addWidget(self.course_list_panel, 1)
        
        # Middle panel - Course Details (40% width)
        self.details_panel = CourseDetailsPanelQt5()
        self.details_panel.setMinimumWidth(350)
        self.details_panel.setMaximumWidth(400)
        content_layout.addWidget(self.details_panel, 0)
        
        # Right panel - Selected Courses (30% width)
        self.selected_courses_panel = SelectedCoursesPanelQt5(self.max_courses)
        self.selected_courses_panel.setMinimumWidth(400)
        content_layout.addWidget(self.selected_courses_panel, 1)
        
        parent_layout.addWidget(content_widget)
        
    def create_footer(self, parent_layout):
        """Create the footer with action buttons"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        footer_layout.addStretch()
        
        # Save Selection button
        save_button = ModernUIQt5.create_button("Save Selection", "primary")
        save_button.clicked.connect(self.save_selection)
        footer_layout.addWidget(save_button)
        
        parent_layout.addWidget(footer_widget)
        
    def setup_course_manager(self):
        """Set up the course manager to handle logic"""
        self.course_manager = CourseManagerQt5(
            self.controller,
            self.course_list_panel,
            self.details_panel,
            self.selected_courses_panel
        )
        
    def load_courses(self):
        """Load courses from the controller"""
        self.course_manager.load_courses()
        
    # def save_selection(self):
    #     """Save the current course selection and go to timetable page"""
    #     if self.course_manager.save_selection():
            
    #         # Create timetable window - Fix: pass self.controller instead of self
    #         from SRC.ViewLayer.View.TimetablesPage import TimetablesPage
            
    #         self.timetable_window = TimetablesPage(self.controller, self)  
    #         self.timetable_window.show()
    def save_selection(self):
        """Save the current course selection and go to timetable page"""
        if self.course_manager.save_selection():
            self.show_timetables()    
    def show_timetables(self):
        """Show the timetables page"""
        # Import the PyQt5 timetables page
        from SRC.ViewLayer.View.Timetables_qt5 import TimetablesPageQt5
        
        # Create callback function to return to course selection
        def go_back_to_selection():
            if self.timetables_window:
                self.timetables_window.close()
                self.timetables_window = None
            self.show()  # Show the course selection window again
        
        # Hide the current window
        self.hide()
        
        # Create the timetables window
        self.timetables_window = TimetablesPageQt5(
            controller=self.controller,
            go_back_callback=go_back_to_selection
        )
        
        # Show the timetables window
        self.timetables_window.show()       
    def get_selected_courses(self):
        """Get the list of selected courses"""
        return self.course_manager.get_selected_courses()
        
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.controller.handle_exit()
            event.accept()
        else:
            event.ignore()
            
    def run(self):
        """Run the application"""
        self.load_courses()
        self.show()

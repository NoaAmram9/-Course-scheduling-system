import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Layout.TimeConstraintsSelector import TimeConstraintsSelector
from SRC.ViewLayer.Logic.course_manager_qt5 import CourseManagerQt5
from SRC.ViewLayer.Layout.course_list_panel_qt5 import CourseListPanelQt5
from SRC.ViewLayer.Layout.MainPage.CourseDetailsPanelQt5 import CourseDetailsPanelQt5
from SRC.ViewLayer.Layout.selected_courses_panel_qt5 import SelectedCoursesPanelQt5
from SRC.ViewLayer.View.ManualSchedulePage import ManualSchedulePage
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5


class MainPageQt5(QMainWindow):
    def __init__(self, Data ,controller, filePath):
        super().__init__()
        self.controller = controller
        self.max_courses = 7
        self.selected_course_ids = set()
        self.course_map = {}
        self.previous_constraints = []
        self.Data = Data
        self.dark_mode = False  
        self.init_ui()
        self.setup_course_manager()
        self.filePath = filePath
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Course Selector")
        self.setGeometry(100, 100, 1200, 650)
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet(dark=self.dark_mode))

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
        
        # כפתור מצב לילה
        self.dark_mode_btn = QPushButton()
        self.dark_mode_btn.setCheckable(True)
        self.dark_mode_btn.setChecked(self.dark_mode)
        self.update_dark_mode_button_text()
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        header_layout.addWidget(self.dark_mode_btn, alignment=Qt.AlignRight)
            
        parent_layout.addWidget(header_widget)
        
    def update_dark_mode_button_text(self):
        if self.dark_mode:
            self.dark_mode_btn.setText("מצב רגיל")
        else:
            self.dark_mode_btn.setText("מצב לילה")
            
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet(dark=self.dark_mode))
        self.style().polish(self)
        for widget in self.findChildren(QWidget):
            widget.style().polish(widget)
        self.update_dark_mode_button_text()
        self.dark_mode_btn.setChecked(self.dark_mode)

        
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

        # # Add Time Constraints Button (styled like Save Selection)
        # self.toggle_constraints_button = ModernUIQt5.create_button("Add Time Constraints", "primary")
        # self.toggle_constraints_button.setFixedHeight(36)
        # #self.toggle_constraints_button.clicked.connect(self.open_time_constraints_dialog)
        # self.toggle_constraints_button.clicked.connect(self.show_time_constraints_selector)


        # # Add it to content_layout with alignment below the course list
        # content_layout.addWidget(self.toggle_constraints_button, 1, Qt.AlignTop)

        
        # Middle panel - Course Details (40% width)
        self.details_panel = CourseDetailsPanelQt5()
        self.details_panel.setMinimumWidth(400)
        self.details_panel.setMaximumWidth(600)
        self.details_panel.setMinimumHeight(500)
        self.details_panel.setMaximumHeight(600)
        content_layout.addWidget(self.details_panel, 0)
        
        # Right panel - Selected Courses (30% width)
        self.selected_courses_panel = SelectedCoursesPanelQt5(self.max_courses)
        self.selected_courses_panel.setMinimumWidth(300)
        content_layout.addWidget(self.selected_courses_panel, 1)
        
        parent_layout.addWidget(content_widget)

    def create_footer(self, parent_layout):
        """Unified footer with both buttons on the same row"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)
    
        # Add Time Constraints button (left-aligned)
        self.toggle_constraints_button = ModernUIQt5.create_button("Add Time Constraints", "primary")
        self.toggle_constraints_button.setFixedHeight(36)
        self.toggle_constraints_button.clicked.connect(self.show_time_constraints_selector)
        footer_layout.addWidget(self.toggle_constraints_button, alignment=Qt.AlignLeft)
    
        # Spacer in the middle
        footer_layout.addStretch()
    
        # Save Selection button (right-aligned)
        auto_ganerate_button = ModernUIQt5.create_button("Auto-Generate Schedules", "primary")
        auto_ganerate_button.clicked.connect(self.auto_ganerate_schedules)
        auto_ganerate_button.setFixedHeight(36)
        footer_layout.addWidget(auto_ganerate_button, alignment=Qt.AlignRight)
        
        # Save Selection button (right-aligned)
        manual_button = ModernUIQt5.create_button("Create Manually", "primary")
        manual_button.clicked.connect(self.manual_schedule)
        manual_button.setFixedHeight(36)
        footer_layout.addWidget(manual_button, alignment=Qt.AlignRight)
    
        parent_layout.addWidget(footer_widget)


        
    def setup_course_manager(self):
        """Set up the course manager to handle logic"""
        self.course_manager = CourseManagerQt5(
            self.controller,
            self.Data,
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
    def auto_ganerate_schedules(self):
        """Save the current course selection and go to timetable page"""
        if self.course_manager.save_selection():
            self.controller.save_courses_to_file("Data/All_Courses.xlsx", self.Data)
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
            go_back_callback=go_back_to_selection,
            filePath= self.filePath
        )
        
        # Show the timetables window
        self.timetables_window.show()  
        
             
    def get_selected_courses(self):
        """Get the list of selected courses"""
        return self.course_manager.get_selected_courses()


    def show_time_constraints_selector(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Select Time Constraints")
        layout = QVBoxLayout(self.dialog)

        # Convert stored constraints into (day, hour) tuples
        preselected = set()
        for c in self.previous_constraints:
            for h in range(c["start"], c["end"]):
                preselected.add((c["day"], h))

        self.selector = TimeConstraintsSelector(preselected_slots=preselected)
        layout.addWidget(self.selector)

        confirm_btn = QPushButton("Apply")
        confirm_btn.clicked.connect(self.apply_constraints_from_selector)
        layout.addWidget(confirm_btn)

        self.dialog.exec_()


    def apply_constraints_from_selector(self):
        self.previous_constraints = self.selector.get_constraints()  # Save them
        self.controller.apply_time_constraints(self.previous_constraints)
        self.dialog.close()

    def manual_schedule(self):
        if self.course_manager.save_selection():
            selected_courses = self.get_selected_courses()
            self.manual_schedule_page = ManualSchedulePage(self.controller, self.filePath)
            self.manual_schedule_page.show()

        
    #closeEvent method to handle window close event
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.controller.save_courses_to_file( "Data/All_Courses.xlsx", self.Data)
            self.controller.handle_exit()
            event.accept()
        else:
            event.ignore()
            
    def run(self):
        """Run the application"""
        self.load_courses()
        self.show()
        
        
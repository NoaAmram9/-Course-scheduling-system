import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Layout.TimeConstraintsSelector import TimeConstraintsSelector
from SRC.ViewLayer.Logic.MainPage import MainPageLogic
from SRC.ViewLayer.Layout.course_list_panel_qt5 import CourseListPanelQt5
from SRC.ViewLayer.Layout.MainPage.CourseDetailsPanelQt5 import CourseDetailsPanelQt5
from SRC.ViewLayer.Layout.selected_courses_panel_qt5 import SelectedCoursesPanelQt5
from SRC.ViewLayer.View.ManualSchedulePage import ManualSchedulePage
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from SRC.ViewLayer.View.Timetables_qt5 import TimetablesPageQt5

class MainPageView(QMainWindow):
    """VIEW Layer - Pure UI component for main page display"""
    
    def __init__(self, Data, controller, filePath, go_back_callback=None):
        super().__init__()
        self.controller = controller
        self.Data = Data
        self.filePath = filePath
        self.go_back_callback = go_back_callback 
        self.dark_mode = False
        
        # Initialize UI components
        self.init_ui()
        
        # Initialize course manager (LOGIC layer)
        self.course_manager = MainPageLogic(
            self.controller,
            self.Data,
            self.course_list_panel,
            self.details_panel,
            self.selected_courses_panel,
            main_view=self  # Pass reference to view for callbacks
        )
        
    def init_ui(self):
        """Initialize the user interface - Pure UI setup"""
        """Initialize the user interface - Pure UI setup"""
        self.setWindowTitle("Course Selector")
       
        # Set window icon
        icon_path = "Data/Logo.png"
        self.setWindowIcon(QIcon(icon_path))

        self.setGeometry(100, 100, 1200, 650)
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet(dark=self.dark_mode))

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Create UI sections
        self.create_header(main_layout)
        self.create_content_area(main_layout)
        self.create_footer(main_layout)
        
    def create_header(self, parent_layout):
        """Create the header section - Pure UI"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header_label = QLabel("Course Selector")
        header_label.setObjectName("headerLabel")

      
        font = QFont("Segoe UI")
        
        font.setBold(True)
        header_label.setFont(font)

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        # Dark mode toggle button
        self.dark_mode_btn = QPushButton()
        self.dark_mode_btn.setCheckable(True)
        self.dark_mode_btn.setChecked(self.dark_mode)
        self.update_dark_mode_button_text()
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        header_layout.addWidget(self.dark_mode_btn, alignment=Qt.AlignRight)
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("Data/Logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(logo_pixmap)
        else:
            self.logo_label.setText("LOGO")
            self.logo_label.setStyleSheet("color: gray; font-size: 16px;")

        self.logo_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.logo_label.setObjectName("logoLabel")
        header_layout.addWidget(self.logo_label, alignment=Qt.AlignRight)
       
            
        parent_layout.addWidget(header_widget)
        
    def create_content_area(self, parent_layout):
        """Create the main content area with 3 panels - Pure UI Layout"""
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
        self.details_panel.setMinimumWidth(400)
        self.details_panel.setMaximumWidth(600)
        self.details_panel.setMinimumHeight(500)
        self.details_panel.setMaximumHeight(600)
        content_layout.addWidget(self.details_panel, 0)
        
        # Right panel - Selected Courses (30% width)
        self.selected_courses_panel = SelectedCoursesPanelQt5(max_courses=7)
        self.selected_courses_panel.setMinimumWidth(300)
        content_layout.addWidget(self.selected_courses_panel, 1)
        
        parent_layout.addWidget(content_widget)

    def create_footer(self, parent_layout):
        """Create footer with action buttons - Pure UI"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)
        
        # # Left-aligned buttons
        # self.back_button = ModernUIQt5.create_button("Back", "primary")
        # self.back_button.setFixedHeight(36)
        # self.back_button.clicked.connect(self.on_back_clicked)
        # footer_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        
        self.toggle_constraints_button = ModernUIQt5.create_button("Add Time Constraints", "primary")
        self.toggle_constraints_button.setFixedHeight(36)
        self.toggle_constraints_button.clicked.connect(self.on_time_constraints_clicked)
        footer_layout.addWidget(self.toggle_constraints_button, alignment=Qt.AlignLeft)
        
        # Spacer
        footer_layout.addStretch()
    
        # Right-aligned buttons
        auto_generate_button = ModernUIQt5.create_button("Auto-Generate Schedules", "primary")
        auto_generate_button.clicked.connect(self.on_auto_generate_clicked)
        auto_generate_button.setFixedHeight(36)
        footer_layout.addWidget(auto_generate_button, alignment=Qt.AlignRight)
        
        manual_button = ModernUIQt5.create_button("Create Manually", "primary")
        manual_button.clicked.connect(self.on_manual_schedule_clicked)
        manual_button.setFixedHeight(36)
        footer_layout.addWidget(manual_button, alignment=Qt.AlignRight)
    
        parent_layout.addWidget(footer_widget)

    # ======================
    # UI EVENT HANDLERS - Delegate to LOGIC layer
    # ======================
    
    def on_back_clicked(self):
        """Handle back button click - Delegate to LOGIC"""
        self.course_manager.handle_back()
        
    def on_time_constraints_clicked(self):
        """Handle time constraints button click - Delegate to LOGIC"""
        self.course_manager.handle_time_constraints()
        
    def on_auto_generate_clicked(self):
        """Handle auto-generate button click - Delegate to LOGIC"""
        self.course_manager.handle_auto_generate()
        
    def on_manual_schedule_clicked(self):
        """Handle manual schedule button click - Delegate to LOGIC"""
        self.course_manager.handle_manual_schedule()

    # ======================
    # UI STATE MANAGEMENT
    # ======================
    
    def update_dark_mode_button_text(self):
        """Update dark mode button text"""
        if self.dark_mode:
            self.dark_mode_btn.setText("מצב רגיל")
        else:
            self.dark_mode_btn.setText("מצב לילה")
            
    def toggle_dark_mode(self):
        """Toggle dark mode - Pure UI state change"""
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet(dark=self.dark_mode))
        self.style().polish(self)
        for widget in self.findChildren(QWidget):
            widget.style().polish(widget)
        self.update_dark_mode_button_text()
        self.dark_mode_btn.setChecked(self.dark_mode)

    # ======================
    # VIEW INTERFACE METHODS - Called by LOGIC layer
    # ======================
    
    def show_time_constraints_dialog(self, previous_constraints):
        """Show time constraints dialog - Called by LOGIC layer"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Time Constraints")
        layout = QVBoxLayout(dialog)

        # Convert stored constraints into (day, hour) tuples
        preselected = set()
        for c in previous_constraints:
            for h in range(c["start"], c["end"]):
                preselected.add((c["day"], h))

        selector = TimeConstraintsSelector(preselected_slots=preselected)
        layout.addWidget(selector)

        confirm_btn = QPushButton("Apply")
        confirm_btn.clicked.connect(lambda: self.course_manager.apply_time_constraints(selector.get_constraints(), dialog))
        layout.addWidget(confirm_btn)

        dialog.exec_()
        
    def show_timetables_page(self):
        def return_to_main_page():
            if hasattr(self, 'timetables_window') and self.timetables_window:
                self.timetables_window.close()
                self.timetables_window = None
            self.show()

        self.hide()
        self.timetables_window = TimetablesPageQt5(
            controller=self.controller,
            go_back_callback=return_to_main_page,
            filePath=self.filePath
        )
        self.timetables_window.show()
        
    def show_manual_schedule_page(self):
        """Show manual schedule page - Called by LOGIC layer"""
        # print("filePath =", self.filePath)
        # self.manual_schedule_page = ManualSchedulePage(self.controller, self.filePath, courses_data = self.Data)
        # self.manual_schedule_page.show()
        self.show_manual_page()
    
    def manual_schedule(self):
        if self.course_manager.save_selection():
            # selected_courses = self.get_selected_courses()
            self.controller.save_courses_to_file("Data/All_Courses.xlsx", self.Data)
            self.show_manual_page()
            
    def show_manual_page(self):
        
        # Create callback function to return to course selection
        def go_back():
            if self.manual_schedule_page:
                self.manual_schedule_page.close()
                self.manual_schedule_page = None
            self.show()  # Show the course selection window again
        
        # Hide the current window
        self.hide()
            
        self.manual_schedule_page = ManualSchedulePage(
            controller = self.controller,
            file_path = self.filePath,
            courses_data = self.Data,
            go_back_callback=go_back,
        )
        self.manual_schedule_page.show()
        
    def show_confirmation_dialog(self, title, message):
        """Show confirmation dialog - Returns True/False"""
        reply = QMessageBox.question(self, title, message,
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        return reply == QMessageBox.Yes
        
    def show_info_dialog(self, title, message):
        """Show information dialog"""
        QMessageBox.information(self, title, message)

    # ======================
    # WINDOW LIFECYCLE
    # ======================
        
    def closeEvent(self, event):
        """Handle window close event - Delegate to LOGIC"""
        if self.course_manager.handle_close_event():
            event.accept()
        else:
            event.ignore()
            
    def load_courses(self):
        """Load courses - Delegate to LOGIC layer"""
        self.course_manager.load_courses()
            
    def run(self):
        """Run the application"""
        self.load_courses()
        self.show()
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.modern_ui_qt5 import ModernUIQt5

class CourseDetailsPanelQt5(QWidget):
    # Signal
    add_course_requested = pyqtSignal(str)  # Emits course code
    
    def __init__(self):
        super().__init__()
        self.current_course = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Course Details")
        title_label.setObjectName("panelTitle")
        layout.addWidget(title_label)
        
        # Content frame
        content_frame = QFrame()
        content_frame.setObjectName("detailsFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(10)
        
        # Course details labels
        self.code_label = QLabel("Code: ")
        self.code_label.setObjectName("detailLabel")
        content_layout.addWidget(self.code_label)
        
        self.name_label = QLabel("Name: ")
        self.name_label.setObjectName("detailLabel")
        self.name_label.setWordWrap(True)
        content_layout.addWidget(self.name_label)
        
        self.instructor_label = QLabel("Prof.: ")
        self.instructor_label.setObjectName("detailLabel")
        content_layout.addWidget(self.instructor_label)
        
        content_layout.addStretch()
        layout.addWidget(content_frame)
        
        # Add button
        self.add_button = ModernUIQt5.create_button("Add Course", "accent")
        self.add_button.clicked.connect(self.add_course)
        layout.addWidget(self.add_button)
        
        # Apply styling
        self.setStyleSheet(ModernUIQt5.get_details_panel_stylesheet())
        
    def update_details(self, course):
        """Update the panel with course details"""
        self.current_course = course
        
        if course:
            self.code_label.setText(f"Code: {course._code}")
            self.name_label.setText(f"Name: {course._name}")
            #self.instructor_label.setText(f"Prof.: {course._instructor}")
        else:
            self.code_label.setText("Code: ")
            self.name_label.setText("Name: ")
            self.instructor_label.setText("Prof.: ")
            
    def add_course(self):
        """Add the current course to selected courses"""
        if self.current_course:
            self.add_course_requested.emit(self.current_course._code)

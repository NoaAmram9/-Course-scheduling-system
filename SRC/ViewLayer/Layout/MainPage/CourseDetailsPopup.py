from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from .LessonSectionWidget import LessonSectionWidget

class CourseDetailsPopup(QDialog):
    """Popup dialog for displaying detailed course information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.popup_main_layout = None
        self.popup_content_widget = None
        self.init_ui()

    def init_ui(self):
        """Initialize the popup dialog"""
        self.setWindowTitle("Course Details")
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setModal(False)
        self.resize(650, 550)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        self._create_title(layout)
        
        # Scrollable content area
        self._create_scroll_area(layout)
        
        # Close button
        self._create_close_button(layout)
        
        # Apply styling
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet())

    def _create_title(self, parent_layout):
        """Create the popup title"""
        title = QLabel("Detailed Course Information")
       
        parent_layout.addWidget(title)

    def _create_scroll_area(self, parent_layout):
        """Create the scrollable content area"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.popup_content_widget = QWidget()
        self.popup_main_layout = QVBoxLayout(self.popup_content_widget)
        self.popup_main_layout.setSpacing(15)

        scroll_area.setWidget(self.popup_content_widget)
        parent_layout.addWidget(scroll_area)

    def _create_close_button(self, parent_layout):
        """Create the close button"""
        close_layout = QHBoxLayout()
        close_layout.addStretch()

        close_btn = ModernUIQt5.create_button("✖ Close")
       
        close_btn.clicked.connect(self.close)
        close_layout.addWidget(close_btn)
        close_layout.addStretch()

        parent_layout.addLayout(close_layout)

    def update_course_details(self, course):
        """Update the popup with detailed course information"""
        self._clear_content()
        
        if not course:
            return

        # Add notes section if available
        self._add_notes_section(course)
        
        # Add lesson sections
        self._add_lesson_sections(course)

    def _clear_content(self):
        """Clear existing content from the popup"""
        while self.popup_main_layout.count():
            child = self.popup_main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _add_notes_section(self, course):
        """Add notes section if course has notes"""
        if not (hasattr(course, 'notes') and course.notes):
            return

        notes_frame = QFrame()
        notes_frame.setObjectName("detailsFrame")
        notes_layout = QVBoxLayout(notes_frame)
        notes_layout.setContentsMargins(15, 15, 15, 15)

        # Notes title
        notes_title = QLabel("Notes")
        
        notes_layout.addWidget(notes_title)

        # Notes content
        notes_text = QLabel(course.notes)
        notes_text.setWordWrap(True)
      
        notes_layout.addWidget(notes_text)

        self.popup_main_layout.addWidget(notes_frame)

    def _add_lesson_sections(self, course):
        """Add all lesson type sections"""
        lesson_types = [
            ('lectures', 'Lectures'),
            ('exercises', 'Exercises'),
            ('labs', 'Labs'),
            ('departmentHours', 'Department Hours'),
            ('reinforcement', 'Reinforcement'),
            ('training', 'Training')
        ]

        for attr_name, display_name in lesson_types:
            lessons = getattr(course, attr_name, [])
            if lessons:  # Only add section if it has lessons
                section_widget = LessonSectionWidget(attr_name, display_name, lessons)
                self.popup_main_layout.addWidget(section_widget)
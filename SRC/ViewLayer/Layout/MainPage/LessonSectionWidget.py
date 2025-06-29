from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .LessonWidget import LessonWidget

class LessonSectionWidget(QFrame):
    """Widget for displaying a section of lessons (e.g., lectures, exercises)"""
    
    def __init__(self, attr_name, display_name, lessons):
        super().__init__()
        self.attr_name = attr_name
        self.display_name = display_name
        self.lessons = lessons
        self.init_ui()

    def init_ui(self):
        """Initialize the lesson section widget"""
        self.setObjectName("detailsFrame")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Create header
        self._create_header(layout)
        
        # Add separator
        self._add_separator(layout)
        
        # Add lesson widgets
        self._add_lesson_widgets(layout)

    def _create_header(self, parent_layout):
        """Create the section header"""
        header_layout = QHBoxLayout()
        
        title_label = QLabel(f" {self.display_name}")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #3E5879;")
        
        count_label = QLabel(f"({len(self.lessons)} sessions)")
        count_label.setStyleSheet("color: #3E5879; font-size: 12px;")

        header_layout.addWidget(title_label)
        header_layout.addWidget(count_label)
        header_layout.addStretch()
        
        parent_layout.addLayout(header_layout)

    def _add_separator(self, parent_layout):
        """Add horizontal separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        separator.setStyleSheet("color: #ffffff; background-color: #3E5879;")
        parent_layout.addWidget(separator)

    def _add_lesson_widgets(self, parent_layout):
        """Add individual lesson widgets"""
        for i, lesson in enumerate(self.lessons):
            lesson_widget = LessonWidget(lesson, i + 1)
            parent_layout.addWidget(lesson_widget)
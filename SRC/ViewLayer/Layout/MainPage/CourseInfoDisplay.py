from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CourseInfoDisplay(QWidget):
    """Component responsible for displaying basic course information"""
    
    def __init__(self):
        super().__init__()
        self.labels = {}
        self.init_ui()

    def init_ui(self):
        """Initialize the info display layout"""
        # Main content frame
        content_frame = QFrame()
        content_frame.setObjectName("detailsFrame")
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(8)
        content_layout.setAlignment(Qt.AlignTop)

        # Create info fields
        self._create_info_fields(content_layout)
        
        # Push content to top
        content_layout.addStretch()
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_frame)

    def _create_info_fields(self, parent_layout):
        """Create all the information display fields"""
        fields = [
            ('code_label', "Code: "),
            ('name_label', "Name: "),
            ('semester_label', "Semester: "),
            ('total_credits_label', "Total Credits: "),
            ('total_groups_label', "Groups: ")
        ]

        for field_name, label_text in fields:
            self._create_detail_row(parent_layout, field_name, label_text)

    def _create_detail_row(self, parent_layout, attr_name, label_text):
        """Create a styled row for a single piece of course info"""
        label = QLabel(label_text)
        label.setObjectName("detailLabel")
        label.setWordWrap(True)

        # Wrap in a frame for styling
        wrapper = QFrame()
        wrapper.setObjectName("detailRowFrame")
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 8, 0, 8)
        wrapper_layout.addWidget(label)

        # Store label reference
        self.labels[attr_name] = label
        
        parent_layout.addWidget(wrapper)
        self._add_separator(parent_layout)

    def _add_separator(self, layout):
        """Add a horizontal line separator between info rows"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #FFA500; background-color: #3E5879; max-height: 1px;")
        layout.addWidget(line)

    def update_course_info(self, course, calculator):
        """Update the display with course information"""
        if course:
            self._update_with_course_data(course, calculator)
        else:
            self._clear_all_fields()

    def _update_with_course_data(self, course, calculator):
        """Update labels with actual course data"""
        self.labels['code_label'].setText(f"Code: {course._code}")
        self.labels['name_label'].setText(f"Name: {course._name}")
        self.labels['semester_label'].setText(f"Semester: {course._semester}")
        
        total_credits = calculator.calculate_total_credits(course)
        self.labels['total_credits_label'].setText(f"Total Credits: {total_credits}")
        
        total_groups = calculator.count_total_groups(course)
        self.labels['total_groups_label'].setText(f"Groups: {total_groups}")

    def _clear_all_fields(self):
        """Clear all display fields"""
        default_texts = {
            'code_label': "Code: ",
            'name_label': "Name: ",
            'semester_label': "Semester: ",
            'total_credits_label': "Total Credits: ",
            'total_groups_label': "Groups: "
        }
        
        for field, text in default_texts.items():
            if field in self.labels:
                self.labels[field].setText(text)
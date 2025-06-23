from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class LessonWidget(QFrame):
    """Widget for displaying details of a single lesson"""
    
    def __init__(self, lesson, lesson_number):
        super().__init__()
        self.lesson = lesson
        self.lesson_number = lesson_number
        self.init_ui()

    def init_ui(self):
        """Initialize the lesson widget"""
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 3px 0px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Create header
        self._create_header(layout)
        
        # Create details grid
        self._create_details_grid(layout)

    def _create_header(self, parent_layout):
        """Create the lesson header"""
        header_text = f"Session {self.lesson_number} - Group {getattr(self.lesson, 'groupCode', 'N/A')}"
        
        if hasattr(self.lesson, 'lesson_type') and self.lesson.lesson_type:
            header_text += f" ({self.lesson.lesson_type})"

        header_label = QLabel(header_text)
        header_label.setStyleSheet("font-weight: bold; color: #333; font-size: 12px;")
        parent_layout.addWidget(header_label)

    def _create_details_grid(self, parent_layout):
        """Create the details grid for lesson attributes"""
        details_widget = QWidget()
        details_layout = QGridLayout(details_widget)
        details_layout.setSpacing(8)
        details_layout.setContentsMargins(5, 5, 5, 5)

        row = 0
        row = self._add_time_info(details_layout, row)
        row = self._add_location_info(details_layout, row)
        row = self._add_instructors_info(details_layout, row)
        row = self._add_credits_info(details_layout, row)
        row = self._add_hours_info(details_layout, row)

        parent_layout.addWidget(details_widget)

    def _add_time_info(self, layout, row):
        """Add time information to the grid"""
        if not (hasattr(self.lesson, 'time') and self.lesson.time):
            return row

        time_label = QLabel("Time:")
        time_label.setStyleSheet("font-weight: bold; color: #555;")
        
        start_time = f"{self.lesson.time.start_hour:02d}:00"
        end_time = f"{self.lesson.time.end_hour:02d}:00"
        
        # Hebrew day names
        days = {
            1: "ראשון", 2: "שני", 3: "שלישי",
            4: "רביעי", 5: "חמישי", 6: "שישי", 7: "שבת"
        }
        day_name = days.get(self.lesson.time.day, f"יום {self.lesson.time.day}")
        time_display = f"{day_name}: {start_time} - {end_time}"
        
        time_value = QLabel(time_display)
        
        layout.addWidget(time_label, row, 0)
        layout.addWidget(time_value, row, 1)
        return row + 1

    def _add_location_info(self, layout, row):
        """Add location information to the grid"""
        if not (hasattr(self.lesson, 'building') and hasattr(self.lesson, 'room') 
                and self.lesson.building and self.lesson.room):
            return row

        location_label = QLabel("Location:")
        location_label.setStyleSheet("font-weight: bold; color: #555;")
        
        location_value = QLabel(f"בניין: {self.lesson.building}, חדר: {self.lesson.room}")
        
        layout.addWidget(location_label, row, 0)
        layout.addWidget(location_value, row, 1)
        return row + 1

    def _add_instructors_info(self, layout, row):
        """Add instructors information to the grid"""
        if not (hasattr(self.lesson, 'instructors') and self.lesson.instructors):
            return row

        instructors_label = QLabel("Instructors:")
        instructors_label.setStyleSheet("font-weight: bold; color: #555;")
        
        instructors_value = QLabel(", ".join(self.lesson.instructors))
        instructors_value.setWordWrap(True)
        
        layout.addWidget(instructors_label, row, 0)
        layout.addWidget(instructors_value, row, 1)
        return row + 1

    def _add_credits_info(self, layout, row):
        """Add credit points information to the grid"""
        if not (hasattr(self.lesson, 'creditPoints') and self.lesson.creditPoints):
            return row

        credits_label = QLabel("Credits:")
        credits_label.setStyleSheet("font-weight: bold; color: #555;")
        
        credits_value = QLabel(str(self.lesson.creditPoints))
        
        layout.addWidget(credits_label, row, 0)
        layout.addWidget(credits_value, row, 1)
        return row + 1

    def _add_hours_info(self, layout, row):
        """Add weekly hours information to the grid"""
        if not (hasattr(self.lesson, 'weeklyHours') and self.lesson.weeklyHours):
            return row

        hours_label = QLabel("Weekly Hours:")
        hours_label.setStyleSheet("font-weight: bold; color: #555;")
        
        hours_value = QLabel(str(self.lesson.weeklyHours))
        
        layout.addWidget(hours_label, row, 0)
        layout.addWidget(hours_value, row, 1)
        return row + 1
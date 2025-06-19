
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from .CourseFormValidator import CourseFormValidator
from SRC.Models.Course import Course
from SRC.Models.Lesson import Lesson
from SRC.Models.LessonTimes import LessonTimes

class LessonDialog(QDialog):
    """Dialog for adding individual lessons"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lesson = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize lesson dialog"""
        self.setWindowTitle("Add Lesson")
        self.setModal(True)
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Lesson Type
        layout.addWidget(QLabel("Lesson Type:"))
        self.lesson_type_combo = QComboBox()
        self.lesson_type_combo.addItems([
            "lecture", "exercise", "lab", "reinforcement", 
            "training", "departmentHours", "other"
        ])
        layout.addWidget(self.lesson_type_combo)
        
        # Day
        layout.addWidget(QLabel("Day:"))
        self.day_combo = QComboBox()
        self.day_combo.addItems([
            "Sunday (1)", "Monday (2)", "Tuesday (3)", "Wednesday (4)",
            "Thursday (5)", "Friday (6)", "Saturday (7)"
        ])
        layout.addWidget(self.day_combo)
        
        # Start Hour
        layout.addWidget(QLabel("Start Hour:"))
        self.start_hour_spin = QSpinBox()
        self.start_hour_spin.setRange(8, 22)
        self.start_hour_spin.setValue(8)
        layout.addWidget(self.start_hour_spin)
        
        # End Hour
        layout.addWidget(QLabel("End Hour:"))
        self.end_hour_spin = QSpinBox()
        self.end_hour_spin.setRange(9, 22)
        self.end_hour_spin.setValue(10)
        layout.addWidget(self.end_hour_spin)
        
        # Building
        layout.addWidget(QLabel("Building:"))
        self.building_edit = QLineEdit()
        self.building_edit.setPlaceholderText("e.g., Building A")
        layout.addWidget(self.building_edit)
        
        # Room
        layout.addWidget(QLabel("Room:"))
        self.room_edit = QLineEdit()
        self.room_edit.setPlaceholderText("e.g., 101")
        layout.addWidget(self.room_edit)
        
        # Instructors
        layout.addWidget(QLabel("Instructors (comma separated):"))
        self.instructors_edit = QLineEdit()
        self.instructors_edit.setPlaceholderText("e.g., Dr. Smith, Prof. Johnson")
        layout.addWidget(self.instructors_edit)
        
        # Credit Points
        layout.addWidget(QLabel("Credit Points:"))
        self.credit_points_spin = QSpinBox()
        self.credit_points_spin.setRange(0, 10)
        self.credit_points_spin.setValue(3)
        layout.addWidget(self.credit_points_spin)
        
        # Weekly Hours
        layout.addWidget(QLabel("Weekly Hours:"))
        self.weekly_hours_spin = QSpinBox()
        self.weekly_hours_spin.setRange(0, 20)
        self.weekly_hours_spin.setValue(2)
        layout.addWidget(self.weekly_hours_spin)
        
        # Group Code
        layout.addWidget(QLabel("Group Code:"))
        self.group_code_spin = QSpinBox()
        self.group_code_spin.setRange(1, 99)
        self.group_code_spin.setValue(1)
        layout.addWidget(self.group_code_spin)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("Add Lesson")
        ok_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        
    def accept(self):
        """Create lesson object and close dialog"""
        if self.start_hour_spin.value() >= self.end_hour_spin.value():
            QMessageBox.warning(self, "Invalid Time", "Start hour must be before end hour.")
            return
            
        # Create lesson times
        lesson_times = LessonTimes(
            start_hour=self.start_hour_spin.value(),
            end_hour=self.end_hour_spin.value(),
            day=self.day_combo.currentIndex() + 1
        )
        
        # Parse instructors
        instructors_text = self.instructors_edit.text().strip()
        instructors = [inst.strip() for inst in instructors_text.split(',') if inst.strip()] if instructors_text else []
        
        # Create lesson
        self.lesson = Lesson(
            time=lesson_times,
            lesson_type=self.lesson_type_combo.currentText(),
            building=self.building_edit.text().strip(),
            room=self.room_edit.text().strip(),
            instructors=instructors,
            creditPoints=self.credit_points_spin.value(),
            weeklyHours=self.weekly_hours_spin.value(),
            groupCode=self.group_code_spin.value()
        )
        
        super().accept()
        
    def get_lesson(self):
        """Return the created lesson"""
        return self.lesson
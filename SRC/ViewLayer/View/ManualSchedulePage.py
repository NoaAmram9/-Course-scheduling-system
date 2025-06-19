from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from SRC.ViewLayer.Layout.ManualScheduleComponents.ExpandableCourseList import ExpandableCourseList
from SRC.ViewLayer.Logic.ManualScheduleLogic import ManualScheduleLogic
from SRC.ViewLayer.Layout.Timetable_qt5 import TimetableGridWidget
from SRC.ViewLayer.Layout.ManualScheduleComponents.header_navbar import HeaderNavbar
from SRC.ViewLayer.Layout.ManualScheduleComponents.bottom_navbar import BottomNavBar
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, QPushButton,
                             QSizePolicy, QVBoxLayout, QHBoxLayout, QSpacerItem)
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap

class ManualSchedulePage(QWidget):
    def __init__(self, controller, file_path):
        super().__init__()
        self.logic = ManualScheduleLogic(controller, file_path)
        self.courses_info = self.logic.courses_info
        
        self.setWindowTitle("Manual Schedule")
        
        self.init_ui()

    def init_ui(self):  
        self.setStyleSheet(ModernUIQt5.get_manual_schedule_stylesheet())

        # ====== MAIN LAYOUT: VERTICAL ======
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # ====== HEADER NAVBAR ======
        self.header = HeaderNavbar(self)
        main_layout.addLayout(self.header.create_layout())
        self.save_button, self.reset_button, self.undo_button = self.header.get_buttons()
        
        # ====== CONTENT LAYOUT: HORIZONTAL ======
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Course list component (left)
        self.course_list_component = ExpandableCourseList(self.courses_info, self)
        content_layout.addWidget(self.course_list_component, stretch=1)

        # Timetable container (right)
        self.create_timetable_container(content_layout)
        content_layout.setStretch(1, 3)  # timetable = 3/4 of the width
        
        bottom_layout = BottomNavBar(self)
        main_layout.addLayout(bottom_layout.create_layout())  
        
    def create_timetable_container(self, parent_layout):
        """Create the scrollable area to display timetable widgets"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setObjectName("scrollArea")

        self.timetable_widget = QWidget()
        self.timetable_widget.setObjectName("timetableWidgetContainer")
        self.timetable_layout = QVBoxLayout()
        self.timetable_layout.setContentsMargins(20, 20, 20, 20)
        self.timetable_widget.setLayout(self.timetable_layout)

        self.scroll_area.setWidget(self.timetable_widget)
        parent_layout.addWidget(self.scroll_area)

        self.setStyleSheet(ModernUIQt5.get_manual_schedule_stylesheet())
        
        # Create and show new timetable grid
        timetable_grid = TimetableGridWidget(self.logic.occupied_windows)
        # slot = self.logic.lessons_slot_map
        # timetable_grid = TimetableGridWidget({})
        self.timetable_layout.addWidget(timetable_grid)
        self.timetable_layout.addStretch()
        
        # Set size policies to allow the widget to expand and fill available space
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def handle_lesson_type_click(self, course_id, lesson_type):
        self.logic.handle_lesson_type_click(course_id, lesson_type)
    
    def handle_course_click(self, course_id):
        self.logic.handle_course_click(course_id)
    
    def update_view(self):
        pass
    
    def handle_reset(self):
        """Reset the current schedule."""
        self.logic.reset()
        # Optionally, you can update the view or notify the user
        print("Schedule reset")
        self.reset_button.setEnabled(False)  # Disable reset button after reset
        
    def save_schedule(self):
        """Save the current schedule to a file."""
        self.logic.save_schedule()
        # Optionally, you can update the view or notify the user
        print("Schedule saved")
    
    def undo_last_action(self):
        """Undo the last action in the schedule."""
        self.logic.undo_last_action()
        # Optionally, you can update the view or notify the user
        print("Last action undone")
        if self.logic.is_schedule_empty():
            self.reset_button.setEnabled(False)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from SRC.ViewLayer.Layout.ManualScheduleComponents.ExpandableCourseList import ExpandableCourseList
from SRC.ViewLayer.Logic.ManualScheduleLogic import ManualScheduleLogic
from SRC.ViewLayer.Layout.Timetable_qt5 import TimetableGridWidget
from SRC.ViewLayer.Layout.ManualScheduleComponents.header_navbar import HeaderNavbar
from SRC.ViewLayer.Layout.ManualScheduleComponents.bottom_navbar import BottomNavBar
from SRC.ViewLayer.Layout.ManualScheduleComponents.LessonSelectionDialog import LessonSelectionDialog
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, QPushButton, QMessageBox,
                             QSizePolicy, QVBoxLayout, QHBoxLayout, QSpacerItem)
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox, QListWidget

class ManualSchedulePage(QWidget):
    def __init__(self, controller, file_path):
        super().__init__()
        self.logic = ManualScheduleLogic(controller, file_path)
        self.courses_info = self.logic.limited_courses_info
        
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
        self.content_layout = QHBoxLayout()
        main_layout.addLayout(self.content_layout)

        # Course list component (left)
        self.course_list_component = ExpandableCourseList(self.courses_info, self)
        self.content_layout.addWidget(self.course_list_component, stretch=1)

        # Timetable container (right)
        self.create_timetable_container(self.content_layout)
        self.content_layout.setStretch(1, 3)  # timetable = 3/4 of the width
        
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
        self.timetable_grid = TimetableGridWidget(self.logic.occupied_windows, 
                                                    editing_mode=True,
                                                    on_available_click = self.handle_available_cell_click,
                                                    on_selected_lesson_click = self.handle_selected_lesson_click)
        self.timetable_layout.addWidget(self.timetable_grid)
        self.timetable_layout.addStretch()
        
        # Set size policies to allow the widget to expand and fill available space
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def handle_lesson_type_click(self, course_id, lesson_type):
        self.logic.handle_lesson_type_click(course_id, lesson_type)
        self.update_view()  # Update the view after handling the click
    
    def handle_course_click(self, course_id):
        self.logic.handle_course_click(course_id)
    
    def handle_available_cell_click(self, day, hour):
        """Handle cell click event to show available lessons."""
        available_lessons = self.logic.get_available_lessons_by_time(day, hour)
        if not available_lessons:
            return
        # Show a dialog to select a lesson
        dialog = LessonSelectionDialog(available_lessons, self)
        if dialog.exec_() == QDialog.Accepted:
            selected_lesson = dialog.get_selected_lesson()
            if selected_lesson:
                # print("User selected:", selected_lesson)
                # Do something with selected_lesson
                self.logic.add_lesson_to_schedule(day, hour, selected_lesson.get('code'), selected_lesson.get('lesson'))
        else:
            print("User canceled the selection")
        self.update_view()  # Update the view after selection
    
    def handle_selected_lesson_click(self, course_id, lesson):
        reply = QMessageBox.question(
            self, 'Delete', 'Are you sure you want to delete this lesson?',
            QMessageBox.Yes | QMessageBox.No, defaultButton=QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self.logic.handle_lesson_click(course_id, lesson)
            self.update_view()    
    
    def update_view(self):
        # self.create_timetable_container(self.content_layout)
        self.timetable_grid.update_timetable(self.logic.occupied_windows)
        
    def handle_reset(self):
        """Reset the current schedule."""
        self.logic.reset()
        # self.reset_button.setEnabled(False)  # Disable reset button after reset
        self.update_view()
        
    def save_schedule(self):
        """Save the current schedule to a file."""
        self.logic.save_schedule()
        # Optionally, you can update the view or notify the user
        print("Schedule saved")
    
    def undo_last_action(self):
        """Undo the last action in the schedule."""
        self.logic.undo_last_action()
        self.update_view()
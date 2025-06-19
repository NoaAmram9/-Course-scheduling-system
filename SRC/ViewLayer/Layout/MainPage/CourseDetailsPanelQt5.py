from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.Models.Course import Course
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from .CourseDetailsPopup import CourseDetailsPopup
from .CourseInfoDisplay import CourseInfoDisplay
from .CourseCalculator import CourseCalculator


class CourseDetailsPanelQt5(QWidget):
    # Signal emitted when the user requests to add the course (by its code)
    add_course_requested = pyqtSignal(str)
    # Signal emitted when a new course is created
    new_course_created = pyqtSignal(Course)


    def __init__(self):
        super().__init__()
        self.current_course = None
        self.details_popup = None
        self.add_course_dialog = None
        self.course_info_display = None
        self.course_calculator = CourseCalculator()
        self.init_ui()

    def init_ui(self):
        """Initialize the layout and widgets of the panel"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Panel title
        title_label = QLabel("Course Details")
        title_label.setObjectName("panelTitle")
        title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(title_label)

        # Create course info display component
        self.course_info_display = CourseInfoDisplay()
        layout.addWidget(self.course_info_display)

        # Buttons panel
        self._create_buttons_panel(layout)

        # Apply styling
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet())

    def _create_buttons_panel(self, parent_layout):
        """Create the buttons panel"""
        buttons_layout = QHBoxLayout()

        # Details button
        self.details_button = ModernUIQt5.create_button("Additional Details")
        self.details_button.setObjectName("DetailsButton")
        self.details_button.clicked.connect(self.show_details_popup)
        buttons_layout.addWidget(self.details_button)

        

        parent_layout.addLayout(buttons_layout)
    def get_current_course(self):
        return self.current_course if hasattr(self, 'current_course') else None
    def update_details(self, course):
        """Update the course detail panel with a specific course"""
        self.current_course = course
        if self.course_info_display:
            self.course_info_display.update_course_info(course, self.course_calculator)
   
    def show_details_popup(self):
        """Show the full details popup window when clicked"""
        if not self.current_course:
            return

        if not self.details_popup:
            self.details_popup = CourseDetailsPopup(self)
        
        self.details_popup.update_course_details(self.current_course)
        self._position_popup()
        self.details_popup.show()
        self.details_popup.raise_()
        self.details_popup.activateWindow()

    def _position_popup(self):
        """Position the popup smartly relative to parent widget"""
        parent_pos = self.mapToGlobal(self.pos())
        parent_rect = self.rect()
        screen = QApplication.desktop().screenGeometry()
        popup_width = self.details_popup.width()

        if parent_pos.x() + parent_rect.width() + popup_width < screen.width():
            x = parent_pos.x() + parent_rect.width() + 10
        else:
            x = parent_pos.x() - popup_width - 10
        
        y = max(parent_pos.y(), 50)
        self.details_popup.move(x, y)


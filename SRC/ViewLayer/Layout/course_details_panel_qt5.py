from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class CourseDetailsPanelQt5(QWidget):
    add_course_requested = pyqtSignal(str)  # Emits course code

    def __init__(self):
        super().__init__()
        self.current_course = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title
        title_label = QLabel("Course Details")
        title_label.setObjectName("panelTitle")
        layout.addWidget(title_label)

        # Content frame with orange border
        content_frame = QFrame()
        content_frame.setObjectName("detailsFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(0)  # אין מרווח בין המסגרות – רק קו

        # Labels wrapped in frames with separators
        for attr in [
            ('code_label', "Code: "),
            ('name_label', "Name: "),
            ('instructor_label', "Prof.: "),
            ('semester_label', "Semester: "),
            ('credits_label', "Credit Points: "),
            ('groups_label', "Groups: ")
        ]:
            label = QLabel(attr[1])
            label.setObjectName("detailLabel")
            label.setWordWrap(True)

            wrapper = QFrame()
            wrapper.setObjectName("detailRowFrame")
            wrapper_layout = QVBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(0, 8, 0, 8)
            wrapper_layout.addWidget(label)

            setattr(self, attr[0], label)
            content_layout.addWidget(wrapper)

            # Add separator line
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #FFA500;")  # Orange line
            content_layout.addWidget(line)

        layout.addWidget(content_frame)

        # Add button
        self.add_button = ModernUIQt5.create_button("Add Course")
        self.add_button.setObjectName("UploadButton")
        self.add_button.clicked.connect(self.add_course)
        layout.addWidget(self.add_button)

        self.setStyleSheet(ModernUIQt5.get_main_stylesheet())
    
    def update_details(self, course):
        """Update the panel with course details"""
        self.current_course = course

        if course:
            self.code_label.setText(f"Code: {course._code}")
            self.name_label.setText(f"Name: {course._name}")

            instructors = self._extract_instructors(course)
            self.instructor_label.setText(f"Prof.: {instructors}")

            self.semester_label.setText(f"Semester: {course._semester}")
            self.credits_label.setText(f"Credit Points: {getattr(course, 'creditPoints', 'N/A')}")
            self.groups_label.setText(f"Groups: {self._count_groups(course)}")
            
        else:
            self.code_label.setText("Code: ")
            self.name_label.setText("Name: ")
            self.instructor_label.setText("Prof.: ")
            self.semester_label.setText("Semester: ")
            self.credits_label.setText("Credit Points: ")
            self.groups_label.setText("Groups: ")
            

    def _extract_instructors(self, course):
        instructors_set = set()
        for lst in [course.lectures, course.exercises, course.labs, course.departmentHours, course.training]:
            for lesson in lst:
                instructors_set.update(lesson.instructors)
        return ', '.join(instructors_set) if instructors_set else "Unknown"

    def _count_groups(self, course):
        groups = set()
        for lst in [course.lectures, course.exercises, course.labs, course.departmentHours, course.training]:
            for lesson in lst:
                groups.add(lesson.groupCode)
        return len(groups)

    def add_course(self):
        if self.current_course:
            self.add_course_requested.emit(self.current_course._code)

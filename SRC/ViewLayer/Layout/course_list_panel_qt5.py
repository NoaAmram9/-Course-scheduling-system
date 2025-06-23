from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class CourseListPanelQt5(QWidget):
    course_selected = pyqtSignal(object)
    course_double_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.all_courses = []
        self.filtered_courses = []
        self.course_map = {}
        self.current_semester = '1'  # Default to Semester A
        self.semester_locked = False  # Boolean to track if semester is locked
        self.locked_semester = None   # Which semester is locked
        self.selected_courses = set()  # Track selected courses
        self.init_ui()

    def init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        outer_layout.setSpacing(10)

        # Create frame for inner content
        frame = QFrame()
        frame.setObjectName("detailsFrame")  # same style as in SelectedCoursesPanel
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)
        frame_layout.setSpacing(10)

        # Title
        title_label = QLabel("Available Courses")
        title_label.setObjectName("panelTitle")
        frame_layout.addWidget(title_label)

        # Semester selection
        semester_layout = QHBoxLayout()
        self.semester_a_radio = QRadioButton("סמסטר א")
        self.semester_b_radio = QRadioButton("סמסטר ב")
        self.semester_a_radio.setChecked(True)

        self.semester_a_radio.toggled.connect(self.on_semester_change)
        self.semester_b_radio.toggled.connect(self.on_semester_change)

        semester_layout.addWidget(self.semester_a_radio)
        semester_layout.addWidget(self.semester_b_radio)
        semester_layout.addStretch()
        frame_layout.addLayout(semester_layout)

        # Separator line
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        # line1.setStyleSheet("color: #FFA500;")
        frame_layout.addWidget(line1)

        # Frame around the course list
        tree_frame = QFrame()
        tree_frame.setObjectName("courseTreeFrame")
        tree_layout = QVBoxLayout(tree_frame)
        tree_layout.setContentsMargins(5, 5, 5, 5)
        tree_layout.setSpacing(5)

        self.course_tree = QTreeWidget()
        self.course_tree.setHeaderLabels(["Course Code"])
        self.course_tree.setRootIsDecorated(False)
        self.course_tree.setAlternatingRowColors(True)
        self.course_tree.setObjectName("courseTree")

        self.course_tree.itemClicked.connect(self.on_course_select)
        self.course_tree.itemDoubleClicked.connect(self.on_course_double_click)

        tree_layout.addWidget(self.course_tree)
        frame_layout.addWidget(tree_frame)

        # Separator line
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        # line2.setStyleSheet("color: #D3D4D9;")
        frame_layout.addWidget(line2)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses...")
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_courses)
        frame_layout.addWidget(self.search_input)

        # Add the frame to the outer layout
        outer_layout.addWidget(frame)

        # Apply stylesheet
        self.setStyleSheet(ModernUIQt5.get_main_stylesheet())

    def load_courses(self, courses):
        """Load all courses"""
        self.all_courses = courses
        self.course_map = {course._code: course for course in courses}
        self.apply_semester_filter()

    def apply_semester_filter(self):
        """Filter by selected semester and then apply search"""
        self.filtered_courses = [
            course for course in self.all_courses if str(course._semester) == self.current_semester
        ]
        self.populate_course_tree()
        self.filter_courses()

    def populate_course_tree(self):
        self.course_tree.clear()
        for course in self.filtered_courses:
            item = QTreeWidgetItem([course._code])
            item.setData(0, Qt.UserRole, course._code)
            self.course_tree.addTopLevelItem(item)

    def filter_courses(self):
        """Filter the visible courses based on search text"""
        search_text = self.search_input.text().lower().strip()

        for i in range(self.course_tree.topLevelItemCount()):
            item = self.course_tree.topLevelItem(i)
            course_code = item.data(0, Qt.UserRole)
            course = self.course_map.get(course_code)

            if not course:
                item.setHidden(True)
            elif not search_text:
                item.setHidden(False)
            else:
                visible = (search_text in course._code.lower() or 
                           search_text in course._name.lower())
                item.setHidden(not visible)

    def on_semester_change(self):
        """Triggered when semester radio selection changes"""
        # Check if semester is locked and prevent change
        if self.semester_locked:
            # Revert to locked semester
            if self.locked_semester == '1':
                self.semester_a_radio.setChecked(True)
            else:
                self.semester_b_radio.setChecked(True)
            return
        
        self.current_semester = '1' if self.semester_a_radio.isChecked() else '2'
        self.apply_semester_filter()

    def on_course_select(self, item):
        course_code = item.data(0, Qt.UserRole)
        course = self.course_map.get(course_code)
        if course:
            self.course_selected.emit(course)

    def on_course_double_click(self, item):
        course_code = item.data(0, Qt.UserRole)
        if course_code:
            self.course_double_clicked.emit(course_code)

    def mark_course_as_selected(self, course_code):
        """Mark course as selected and lock semester if first course"""
        for i in range(self.course_tree.topLevelItemCount()):
            item = self.course_tree.topLevelItem(i)
            if item.data(0, Qt.UserRole) == course_code:
                item.setBackground(0, QColor("#e3f2fd"))
                break
        
        # Add to selected courses
        self.selected_courses.add(course_code)
        
        # Lock semester on first course selection
        if not self.semester_locked and len(self.selected_courses) == 1:
            course = self.course_map.get(course_code)
            if course:
                self.semester_locked = True
                self.locked_semester = str(course._semester)
                self.update_semester_radio_state()

    def unmark_course_as_selected(self, course_code):
        for i in range(self.course_tree.topLevelItemCount()):
            item = self.course_tree.topLevelItem(i)
            if item.data(0, Qt.UserRole) == course_code:
                item.setBackground(0, QColor("transparent"))
                break
        
        # Remove from selected courses
        self.selected_courses.discard(course_code)
        
        # Unlock semester if no courses are selected
        if len(self.selected_courses) == 0:
            self.unlock_semester()
            
    def unlock_semester(self):
        """Unlock semester selection (call when all courses are deselected)"""
        self.semester_locked = False
        self.locked_semester = None
        self.update_semester_radio_state()

    def update_semester_radio_state(self):
        """Enable/disable semester radio buttons based on lock state"""
        if self.semester_locked:
            self.semester_a_radio.setEnabled(False)
            self.semester_b_radio.setEnabled(False)
        else:
            self.semester_a_radio.setEnabled(True)
            self.semester_b_radio.setEnabled(True)
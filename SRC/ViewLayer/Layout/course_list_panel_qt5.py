from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.modern_ui_qt5 import ModernUIQt5

class CourseListPanelQt5(QWidget):
    # Signals
    course_selected = pyqtSignal(object)  # Emits course object
    course_double_clicked = pyqtSignal(str)  # Emits course code
    
    def __init__(self):
        super().__init__()
        self.all_courses = []
        self.course_map = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Title
        title_label = QLabel("Available Courses")
        title_label.setObjectName("panelTitle")
        layout.addWidget(title_label)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses...")
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_courses)
        layout.addWidget(self.search_input)
        
        # Course list
        self.course_tree = QTreeWidget()
        self.course_tree.setHeaderLabels(["Course Code"])
        self.course_tree.setRootIsDecorated(False)
        self.course_tree.setAlternatingRowColors(True)
        self.course_tree.setObjectName("courseTree")
        
        # Connect signals
        self.course_tree.itemClicked.connect(self.on_course_select)
        self.course_tree.itemDoubleClicked.connect(self.on_course_double_click)
        
        layout.addWidget(self.course_tree)
        
        # Apply styling
        self.setStyleSheet(ModernUIQt5.get_panel_stylesheet())
        
    def load_courses(self, courses):
        """Load courses into the tree widget"""
        self.course_tree.clear()
        self.course_map = {course._code: course for course in courses}
        self.all_courses = courses
        
        for course in courses:
            item = QTreeWidgetItem([course._code])
            item.setData(0, Qt.UserRole, course._code)
            self.course_tree.addTopLevelItem(item)
            
    def filter_courses(self):
        """Filter courses based on search text"""
        search_text = self.search_input.text().lower().strip()
        
        for i in range(self.course_tree.topLevelItemCount()):
            item = self.course_tree.topLevelItem(i)
            course_code = item.data(0, Qt.UserRole)
            course = self.course_map.get(course_code)
            
            if not search_text:
                item.setHidden(False)
            elif course:
                visible = (search_text in course._code.lower() or 
                          search_text in course._name.lower())
                item.setHidden(not visible)
                
    def on_course_select(self, item):
        """Handle course selection"""
        course_code = item.data(0, Qt.UserRole)
        course = self.course_map.get(course_code)
        if course:
            self.course_selected.emit(course)
            
    def on_course_double_click(self, item):
        """Handle course double-click"""
        course_code = item.data(0, Qt.UserRole)
        if course_code:
            self.course_double_clicked.emit(course_code)
            
    def mark_course_as_selected(self, course_code):
        """Mark a course as selected visually"""
        for i in range(self.course_tree.topLevelItemCount()):
            item = self.course_tree.topLevelItem(i)
            if item.data(0, Qt.UserRole) == course_code:
                item.setBackground(0, QColor("#d5f5e3"))
                break
                
    def unmark_course_as_selected(self, course_code):
        """Remove selection marking from a course"""
        for i in range(self.course_tree.topLevelItemCount()):
            item = self.course_tree.topLevelItem(i)
            if item.data(0, Qt.UserRole) == course_code:
                item.setBackground(0, QColor("transparent"))
                break

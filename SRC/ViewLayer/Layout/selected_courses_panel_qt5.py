from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Theme.modern_ui_qt5 import ModernUIQt5

class SelectedCoursesPanelQt5(QWidget):
    # Signal
    course_removed = pyqtSignal(str)  # Emits course code
    
    def __init__(self, max_courses=7):
        super().__init__()
        self.max_courses = max_courses
        self.selected_course_ids = set()
        self.course_map = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header with count
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Selected Courses")
        title_label.setObjectName("panelTitle")
        header_layout.addWidget(title_label)
        
        self.count_label = QLabel(f"(0/{self.max_courses})")
        self.count_label.setObjectName("countLabel")
        header_layout.addWidget(self.count_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Selected courses table
        self.selected_table = QTreeWidget()
        self.selected_table.setHeaderLabels([
            "Code", "Name", "Instructor", "Lectures", "Exercises", "Labs"
        ])
        self.selected_table.setRootIsDecorated(False)
        self.selected_table.setAlternatingRowColors(True)
        self.selected_table.setObjectName("selectedTable")
        
        # Set column widths
        header = self.selected_table.header()
        header.resizeSection(0, 80)   # Code
        header.resizeSection(1, 200)  # Name
        header.resizeSection(2, 120)  # Instructor
        header.resizeSection(3, 70)   # Lectures
        header.resizeSection(4, 70)   # Exercises
        header.resizeSection(5, 70)   # Labs
        
        # Connect double-click to remove
        self.selected_table.itemDoubleClicked.connect(self.on_course_double_click)
        
        layout.addWidget(self.selected_table)
        
        # Apply styling
        self.setStyleSheet(ModernUIQt5.get_panel_stylesheet())
        
    def set_course_map(self, course_map):
        """Set the course map reference"""
        self.course_map = course_map
        
    def add_course(self, course_code):
        """Add a course to the selected courses panel"""
        if course_code in self.selected_course_ids:
            QMessageBox.information(self, "Already Selected", 
                                  "This course is already in your selection.")
            return False
            
        if len(self.selected_course_ids) >= self.max_courses:
            QMessageBox.warning(self, "Limit Reached", 
                              f"You can select up to {self.max_courses} courses only.")
            return False
            
        if course_code in self.course_map:
            course = self.course_map[course_code]
            self.selected_course_ids.add(course_code)
            
            # Add to table
            lectures = len(course._lectures)
            exercises = len(course._exercises)
            labs = len(course._labs)
            
            item = QTreeWidgetItem([
                course._code, course._name, course._instructor,
                str(lectures), str(exercises), str(labs)
            ])
            item.setData(0, Qt.UserRole, course_code)
            self.selected_table.addTopLevelItem(item)
            
            self.update_selected_count()
            return True
            
        return False
        
    def on_course_double_click(self, item):
        """Handle double-click on a selected course (to remove it)"""
        course_code = item.data(0, Qt.UserRole)
        if course_code:
            self.remove_course(course_code)
            
    def remove_course(self, course_code):
        """Remove a course from the selected courses"""
        if course_code in self.selected_course_ids:
            # Find and remove the item
            for i in range(self.selected_table.topLevelItemCount()):
                item = self.selected_table.topLevelItem(i)
                if item.data(0, Qt.UserRole) == course_code:
                    self.selected_table.takeTopLevelItem(i)
                    break
                    
            self.selected_course_ids.remove(course_code)
            self.update_selected_count()
            self.course_removed.emit(course_code)
            return True
            
        return False
        
    def remove_selected_course(self):
        """Remove the currently selected course"""
        current_item = self.selected_table.currentItem()
        if current_item:
            course_code = current_item.data(0, Qt.UserRole)
            return self.remove_course(course_code)
        else:
            QMessageBox.information(self, "No Selection", 
                                  "Please select a course to remove.")
            return False
            
    def update_selected_count(self):
        """Update the counter showing how many courses are selected"""
        count = len(self.selected_course_ids)
        self.count_label.setText(f"({count}/{self.max_courses})")
        
    def get_selected_courses(self):
        """Get a list of all selected course objects"""
        selected_courses = []
        for i in range(self.selected_table.topLevelItemCount()):
            item = self.selected_table.topLevelItem(i)
            course_code = item.data(0, Qt.UserRole)
            if course_code in self.course_map:
                selected_courses.append(self.course_map[course_code])
        return selected_courses
        
    def clear_selection(self):
        """Clear all selected courses"""
        while self.selected_table.topLevelItemCount() > 0:
            item = self.selected_table.topLevelItem(0)
            course_code = item.data(0, Qt.UserRole)
            self.remove_course(course_code)

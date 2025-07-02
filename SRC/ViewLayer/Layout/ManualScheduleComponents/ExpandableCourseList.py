# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame

# class ExpandableCourseList(QWidget):
#     def __init__(self, courses_info, instance):
#         super().__init__()
#         self.setObjectName("courseTreeFrame") # Set object name for styling
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#         self.instance = instance
#         self.create_course_list(courses_info)

#     def create_course_list(self, courses_info):
#         """Create a list of courses with expandable lesson types.
#         arguments:
#         courses_info -- List of dictionaries containing course information.
#                         Each dictionary should have keys: 'course_name', 'course_id', and 'required_lessons'.
#         """
#         for course in courses_info:
#             course_name = course["course_name"]
#             course_id = course["course_id"]
#             required_lessons = course["required_lessons"]

#             # Header (clickable)
#             course_label = QPushButton(f"{course_name} ({course_id})")
#             course_label.setCheckable(True)
#             course_label.setObjectName("panelTitle")  # Set object name for styling
#             course_label.clicked.connect(lambda checked, cid=course_id: self.instance.handle_course_click(cid))
#             self.layout.addWidget(course_label)

#             # Sub-layout for lesson types (initially hidden)
#             lesson_frame = QFrame()
#             lesson_frame.setObjectName("detailsFrame")
#             lesson_layout = QHBoxLayout()
#             lesson_frame.setLayout(lesson_layout)
#             lesson_frame.setVisible(False)
#             course_label.lesson_frame = lesson_frame  # store reference for toggling visibility

#             for lesson_type in required_lessons:
#                 btn = QPushButton(lesson_type)
#                 btn.setObjectName("DetailsButton")
#                 btn.clicked.connect(lambda _, cid=course_id, lt=lesson_type: self.instance.handle_lesson_type_click(cid, lt))
#                 lesson_layout.addWidget(btn)

#             self.layout.addWidget(lesson_frame)
#             course_label.clicked.connect(lambda checked, frame=lesson_frame: frame.setVisible(checked))
    
    
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from PyQt5.QtGui import QBrush, QColor, QFont

class ExpandableCourseList(QWidget):
    def __init__(self, courses_info, instance):
        super().__init__()
        self.setObjectName("courseTreeFrame")  
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20,20,20,20)
        self.setLayout(self.layout)
        self.instance = instance
        self.lesson_type_items = {}
        
        self.progress_label = QLabel("Scheduled 0 out of 0 required lessons")
        self.progress_label.setObjectName("progressLabel")  
        self.layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFormat("Scheduled 0 out of 0")
        self.progress_bar.setStyleSheet("QProgressBar { color: black; }")
        self.layout.addWidget(self.progress_bar)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # בלי כותרות עמודה
        self.tree.setObjectName("courseTree")   
        self.layout.addWidget(self.tree)

        self.populate_tree(courses_info)
        
        # with open("../../Theme/expandable_course_list.qss", "r") as f:
        path = os.path.join(os.path.dirname(__file__), "../../Theme/expandable_course_list.qss")
        with open(path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
            
    def populate_tree(self, courses_info):
        for course in courses_info:
            course_name = course["course_name"]
            course_id = course["course_id"]
            required_lessons = course["required_lessons"]

            # יצירת פריט ראשי עבור הקורס
            course_item = QTreeWidgetItem([f"{course_name} ({course_id})"])
            course_item.setData(0, Qt.UserRole, course_id)
            
            # ביטול אפשרות סימון קורס
            course_item.setFlags(course_item.flags() & ~Qt.ItemIsSelectable)

            self.tree.addTopLevelItem(course_item)

            # יצירת תתי-פריטים עבור סוגי השיעורים
            for lesson_type in required_lessons:
                lesson_item = QTreeWidgetItem([lesson_type])
                lesson_item.setData(0, Qt.UserRole, (course_id, lesson_type))
                lesson_item.setFlags(lesson_item.flags() & ~Qt.ItemIsSelectable)
                self.lesson_type_items[(course_id, lesson_type)] = lesson_item
                course_item.addChild(lesson_item)

        # חיבור לאירוע לחיצה
        self.tree.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if isinstance(data, tuple):
            course_id, lesson_type = data
            self.instance.handle_lesson_type_click(course_id, lesson_type)
        elif isinstance(data, str):
            course_id = data
            self.instance.handle_course_click(course_id)

    def mark_selected_lesson_types(self, selected_lessons):
        for (course_id, lesson_type), item in self.lesson_type_items.items():
            if self._lesson_type_selected(selected_lessons, course_id, lesson_type):
                # הוספת וי בתחילת הטקסט
                # item.setText(0, f"✔ {lesson_type}")
                item.setText(0, f"{lesson_type}")
                item.setBackground(0, QBrush(QColor("#E4E0DA")))  # רקע עדין
                item.setForeground(0, QBrush(QColor("#021431")))  # טקסט כהה
                bold_font = QFont()
                bold_font.setBold(True)
                item.setFont(0, bold_font)
            else:
                item.setText(0, lesson_type)  # הסרת ה־✔ אם לא נבחר
                item.setBackground(0, QBrush(Qt.transparent))
                item.setForeground(0, QBrush(QColor("#213555")))  # צבע רגיל
                normal_font = QFont()
                normal_font.setBold(False)
                item.setFont(0, normal_font)
        
    def _lesson_type_selected(self, selected_lessons, course_id, lesson_type):
        for cid, lesson in selected_lessons:
            if cid == course_id and lesson.lesson_type.capitalize() == lesson_type:
                return True
        return False

    def update_progress_bar(self, scheduled, total):
        if total == 0:
            percent = 0
            self.progress_bar.setFormat("No required lessons")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: gray; }")
        else:
            percent = int((scheduled / total) * 100)
            self.progress_bar.setFormat(f"Scheduled {scheduled} out of {total}")
            if percent == 100:
                self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #213555; }")
            else:
                self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #3E5879; }")

        self.progress_bar.setValue(percent)

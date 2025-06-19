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
    
    
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class ExpandableCourseList(QWidget):
    def __init__(self, courses_info, instance):
        super().__init__()
        self.setObjectName("courseTreeFrame")  # מתאים לקובץ העיצוב שלך
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.instance = instance

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # בלי כותרות עמודה
        self.tree.setObjectName("courseTree")   
        self.layout.addWidget(self.tree)

        self.populate_tree(courses_info)

    def populate_tree(self, courses_info):
        for course in courses_info:
            course_name = course["course_name"]
            course_id = course["course_id"]
            required_lessons = course["required_lessons"]

            # יצירת פריט ראשי עבור הקורס
            course_item = QTreeWidgetItem([f"{course_name} ({course_id})"])
            course_item.setData(0, Qt.UserRole, course_id)
            self.tree.addTopLevelItem(course_item)

            # יצירת תתי-פריטים עבור סוגי השיעורים
            for lesson_type in required_lessons:
                lesson_item = QTreeWidgetItem([lesson_type])
                lesson_item.setData(0, Qt.UserRole, (course_id, lesson_type))
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

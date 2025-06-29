from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget

DAY_NAMES = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday"
}

class LessonSelectionDialog(QDialog):
    def __init__(self, parent, alternatives):
        super().__init__(parent)
        self.setWindowTitle("Choose Alternative Lesson")
        self.selected_lesson = None
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        label = QLabel("Choose a replacement:")
        layout.addWidget(label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        for lesson in alternatives:
            day_str = DAY_NAMES.get(lesson.time.day, f"Day {lesson.time.day}")
            info = f"{lesson.lesson_type.capitalize()} | {day_str} {lesson.time.start_hour}:00–{lesson.time.end_hour}:00 | Group {lesson.groupCode}"
            button = QPushButton(info)
            button.clicked.connect(lambda checked, l=lesson: self.select_lesson(l))
            scroll_layout.addWidget(button)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        self.apply_stylesheet()

    def select_lesson(self, lesson):
        self.selected_lesson = lesson
        self.accept()

    def get_selected_lesson(self):
        return self.selected_lesson
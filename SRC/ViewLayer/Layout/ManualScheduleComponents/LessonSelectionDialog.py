from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QDialogButtonBox
from PyQt5.QtCore import Qt

class LessonSelectionDialog(QDialog):
    def __init__(self, available_lessons, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a Lesson")
        self.setMinimumWidth(300)
        self.selected_lesson = None

        layout = QVBoxLayout(self)

        # List of lessons
        self.lesson_list = QListWidget()
        for lesson in available_lessons:
            text = f"{lesson['name']} ({lesson['code']}) - {lesson['type']} | {lesson['location']}"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, lesson)
            self.lesson_list.addItem(item)
        layout.addWidget(self.lesson_list)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept_selection)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept_selection(self):
        selected_items = self.lesson_list.selectedItems()
        if selected_items:
            self.selected_lesson = selected_items[0].data(Qt.UserRole)
        self.accept()

    def get_selected_lesson(self):
        return self.selected_lesson

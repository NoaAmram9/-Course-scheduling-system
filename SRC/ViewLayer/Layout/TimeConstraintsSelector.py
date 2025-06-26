from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HOURS = list(range(8, 22))  # 8:00 to 21:00

class TimeConstraintsSelector(QWidget):
    constraints_selected = pyqtSignal(list)  # Emits list of {"day": int, "start": int, "end": int}

    def __init__(self, preselected_slots=None):
        super().__init__()
        self.setStyleSheet("""
            QPushButton#timeSlotButton[selected="true"] {
                background-color: #D8C4B6;
                color: white;
                border: 1px solid #dee2e6;
            }
            QPushButton#timeSlotButton {
                background-color: white;
                border: 1px solid #dee2e6;
            }
        """ + ModernUIQt5.get_timetable_stylesheet())

        self.grid = QGridLayout(self)
        self.cells = {}  # (day_index, hour) -> QPushButton
        self.selected_slots = set(preselected_slots) if preselected_slots else set()

        self.grid.setSpacing(3)
        self.grid.setContentsMargins(10, 10, 10, 10)

        # Add top-left empty header
        top_left = QLabel("")
        top_left.setFixedSize(80, 40)
        self.grid.addWidget(top_left, 0, 0)

        # Add day headers
        for col, day in enumerate(DAYS, start=1):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(80, 40)
            label.setObjectName("dayHeaderLabel")
            self.grid.addWidget(label, 0, col)

        # Add hour labels and time slot buttons
        for row, hour in enumerate(HOURS, start=1):
            hour_label = QLabel(f"{hour:02d}:00")
            hour_label.setAlignment(Qt.AlignCenter)
            hour_label.setFixedSize(80, 40)
            hour_label.setObjectName("timeHeaderLabel")
            self.grid.addWidget(hour_label, row, 0)

            for col, _ in enumerate(DAYS, start=1):
                btn = QPushButton("")
                btn.setCheckable(True)
                btn.setFixedSize(80, 40)
                btn.setObjectName("timeSlotButton")
                self.grid.addWidget(btn, row, col)
                self.cells[(col, hour)] = btn
                btn.clicked.connect(lambda _, d=col, h=hour: self.toggle_slot(d, h))

                if (col, hour) in self.selected_slots:
                    btn.setChecked(True)
                    btn.setProperty("selected", True)
                    btn.style().unpolish(btn)
                    btn.style().polish(btn)

    def toggle_slot(self, day, hour):
        key = (day, hour)
        btn = self.cells[key]
        if key in self.selected_slots:
            self.selected_slots.remove(key)
            btn.setProperty("selected", False)
        else:
            self.selected_slots.add(key)
            btn.setProperty("selected", True)
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    def get_constraints(self):
        return [{"day": d, "start": h, "end": h + 1} for (d, h) in self.selected_slots]

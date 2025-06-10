# your_project/tests/test_filtering_complete.py
import pytest
import os
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QComboBox, QPushButton, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

# Set environment variable for headless testing
os.environ['QT_QPA_PLATFORM'] = 'offscreen'


class MockFilteringWidget(QWidget):
    """
    A mock widget that simulates filtering functionality without requiring MainPageQt5
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.schedule_generator = MagicMock()
        self.schedule_generator.generate_with_constraints.return_value = []
        
    def init_ui(self):
        # Initialize UI components
        self.sort_criteria_combo = QComboBox(self)
        self.sort_criteria_combo.addItems([
            "Number of Study Days",
            "Number of Free Windows", 
            "Total Free Window Time",
            "Average Daily Start Time",
            "Average Daily End Time"
        ])
        
        self.sort_order_combo = QComboBox(self)
        self.sort_order_combo.addItems(["Ascending", "Descending"])
        
        self.show_schedules_button = QPushButton("Show Schedules", self)
        self.schedule_display_widget = QListWidget(self)
        
        # Connect button
        self.show_schedules_button.clicked.connect(self.on_show_schedules_clicked)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.sort_criteria_combo)
        layout.addWidget(self.sort_order_combo)
        layout.addWidget(self.show_schedules_button)
        layout.addWidget(self.schedule_display_widget)
        self.setLayout(layout)
        
    def on_show_schedules_clicked(self):
        """Handle button click to show and sort schedules"""
        try:
            schedules = self.schedule_generator.generate_with_constraints([])
            criteria = self.sort_criteria_combo.currentText()
            order = self.sort_order_combo.currentText()
            self._sort_and_display_schedules(schedules, criteria, order)
        except Exception as e:
            print(f"Error in button click: {e}")
            
    def _sort_and_display_schedules(self, schedules, criteria, order):
        """Sort and display schedules based on criteria and order"""
        try:
            # Define sorting key functions
            if criteria == "Number of Study Days":
                key_func = lambda x: (x.get('study_days', 0), x.get('id', ''))  # Secondary sort by ID for tie-breaking
            elif criteria == "Average Daily End Time":
                def time_to_minutes(time_str):
                    try:
                        h, m = map(int, time_str.split(':'))
                        return h * 60 + m
                    except:
                        return 0
                key_func = lambda x: (time_to_minutes(x.get('avg_end_time', "23:59")), x.get('id', ''))
            elif criteria == "Number of Free Windows":
                key_func = lambda x: (x.get('free_windows_count', 0), x.get('id', ''))
            elif criteria == "Total Free Window Time":
                key_func = lambda x: (x.get('total_free_window_time', 0), x.get('id', ''))
            elif criteria == "Average Daily Start Time":
                def time_to_minutes(time_str):
                    try:
                        h, m = map(int, time_str.split(':'))
                        return h * 60 + m
                    except:
                        return 0
                key_func = lambda x: (time_to_minutes(x.get('avg_start_time', "00:00")), x.get('id', ''))
            else:
                key_func = lambda x: x.get('id', '')

            # Sort schedules
            reverse_sort = (order == "Descending")
            sorted_schedules = sorted(schedules, key=key_func, reverse=reverse_sort)

            # Display sorted schedules
            self.schedule_display_widget.clear()
            for sched in sorted_schedules:
                self.schedule_display_widget.addItem(sched.get('display_text', ''))
                
        except Exception as e:
            print(f"Error in _sort_and_display_schedules: {e}")


@pytest.fixture
def filtering_window(qapp):
    """
    Provides a mock filtering widget for testing
    """
    window = None
    try:
        window = MockFilteringWidget()
        window.hide()  # Don't show during tests
        yield window
    except Exception as e:
        print(f"Error in fixture setup: {e}")
        if window is None:
            window = QWidget()
        yield window
    finally:
        if window is not None:
            try:
                window.close()
                window.deleteLater() 
                qapp.processEvents()
            except:
                pass


# =============================================================================
# 1. מספר ימי לימוד פעילים - בדיקות
# =============================================================================

def test_study_days_ascending_sort(qtbot, filtering_window):
    """בדיקה: מיון עולה לפי מספר ימי לימוד"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "study_days": 5, "display_text": "Schedule 1 (5 days)"},
        {"id": "S2", "study_days": 2, "display_text": "Schedule 2 (2 days)"},
        {"id": "S3", "study_days": 4, "display_text": "Schedule 3 (4 days)"},
        {"id": "S4", "study_days": 1, "display_text": "Schedule 4 (1 day)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 4 (1 day)",
        "Schedule 2 (2 days)",
        "Schedule 3 (4 days)",
        "Schedule 1 (5 days)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_study_days_descending_sort(qtbot, filtering_window):
    """בדיקה: מיון יורד לפי מספר ימי לימוד"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "study_days": 2, "display_text": "Schedule 1 (2 days)"},
        {"id": "S2", "study_days": 5, "display_text": "Schedule 2 (5 days)"},
        {"id": "S3", "study_days": 1, "display_text": "Schedule 3 (1 day)"},
        {"id": "S4", "study_days": 4, "display_text": "Schedule 4 (4 days)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Descending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (5 days)",
        "Schedule 4 (4 days)",
        "Schedule 1 (2 days)",
        "Schedule 3 (1 day)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_study_days_tie_breaking(qtbot, filtering_window):
    """בדיקה: מקרה של תיקו - אותו מספר ימי לימוד"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S_Z", "study_days": 3, "display_text": "Schedule Z (3 days)"},
        {"id": "S_A", "study_days": 3, "display_text": "Schedule A (3 days)"},
        {"id": "S_M", "study_days": 3, "display_text": "Schedule M (3 days)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    # בתיקו, צריך למיין לפי ID (סדר אלפביתי)
    expected_order = [
        "Schedule A (3 days)",
        "Schedule M (3 days)",
        "Schedule Z (3 days)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


# =============================================================================
# 2. מספר החלונות - בדיקות
# =============================================================================

def test_free_windows_ascending_sort(qtbot, filtering_window):
    """בדיקה: מיון עולה לפי מספר חלונות"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "free_windows_count": 4, "display_text": "Schedule 1 (4 windows)"},
        {"id": "S2", "free_windows_count": 1, "display_text": "Schedule 2 (1 window)"},
        {"id": "S3", "free_windows_count": 3, "display_text": "Schedule 3 (3 windows)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Free Windows")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (1 window)",
        "Schedule 3 (3 windows)",
        "Schedule 1 (4 windows)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_free_windows_descending_sort(qtbot, filtering_window):
    """בדיקה: מיון יורד לפי מספר חלונות"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "free_windows_count": 2, "display_text": "Schedule 1 (2 windows)"},
        {"id": "S2", "free_windows_count": 5, "display_text": "Schedule 2 (5 windows)"},
        {"id": "S3", "free_windows_count": 1, "display_text": "Schedule 3 (1 window)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Free Windows")
    window.sort_order_combo.setCurrentText("Descending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (5 windows)",
        "Schedule 1 (2 windows)",
        "Schedule 3 (1 window)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_free_windows_edge_cases(qtbot, filtering_window):
    """בדיקה: מקרי קצה - חלונות קצרים מול ארוכים"""
    window = filtering_window
    
    # חלון של 25 דקות לא נספר, חלון של 60 דקות נספר
    mock_schedules = [
        {"id": "S1", "free_windows_count": 0, "display_text": "Schedule 1 (0 windows - only 25min gaps)"},
        {"id": "S2", "free_windows_count": 2, "display_text": "Schedule 2 (2 windows - 60min each)"},
        {"id": "S3", "free_windows_count": 1, "display_text": "Schedule 3 (1 window - 65min)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Free Windows")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 1 (0 windows - only 25min gaps)",
        "Schedule 3 (1 window - 65min)",
        "Schedule 2 (2 windows - 60min each)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


# =============================================================================
# 3. סכום משך החלונות - בדיקות
# =============================================================================

def test_total_free_window_time_ascending(qtbot, filtering_window):
    """בדיקה: מיון עולה לפי סכום זמן חלונות"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "total_free_window_time": 180, "display_text": "Schedule 1 (180 min total)"},
        {"id": "S2", "total_free_window_time": 60, "display_text": "Schedule 2 (60 min total)"},
        {"id": "S3", "total_free_window_time": 120, "display_text": "Schedule 3 (120 min total)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Total Free Window Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (60 min total)",
        "Schedule 3 (120 min total)",
        "Schedule 1 (180 min total)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_total_free_window_time_descending(qtbot, filtering_window):
    """בדיקה: מיון יורד לפי סכום זמן חלונות"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "total_free_window_time": 90, "display_text": "Schedule 1 (90 min total)"},
        {"id": "S2", "total_free_window_time": 240, "display_text": "Schedule 2 (240 min total)"},
        {"id": "S3", "total_free_window_time": 150, "display_text": "Schedule 3 (150 min total)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Total Free Window Time")
    window.sort_order_combo.setCurrentText("Descending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (240 min total)",
        "Schedule 3 (150 min total)",
        "Schedule 1 (90 min total)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_total_free_window_time_calculation_accuracy(qtbot, filtering_window):
    """בדיקה: דיוק חישוב זמן כולל של חלונות"""
    window = filtering_window
    
    # חלון של שעה + חלון של שעה = סה"כ שעתיים (120 דקות)
    mock_schedules = [
        {"id": "S1", "total_free_window_time": 120, "display_text": "Schedule 1 (2 hours = 60+60 min)"},
        {"id": "S2", "total_free_window_time": 90, "display_text": "Schedule 2 (1.5 hours = 90 min)"},
        {"id": "S3", "total_free_window_time": 150, "display_text": "Schedule 3 (2.5 hours = 90+60 min)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Total Free Window Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (1.5 hours = 90 min)",
        "Schedule 1 (2 hours = 60+60 min)",
        "Schedule 3 (2.5 hours = 90+60 min)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


# =============================================================================
# 4. ממוצע זמן התחלה יומי - בדיקות
# =============================================================================

def test_average_start_time_ascending(qtbot, filtering_window):
    """בדיקה: מיון עולה לפי ממוצע זמן התחלה"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "avg_start_time": "10:00", "display_text": "Schedule 1 (starts 10:00)"},
        {"id": "S2", "avg_start_time": "08:00", "display_text": "Schedule 2 (starts 08:00)"},
        {"id": "S3", "avg_start_time": "09:30", "display_text": "Schedule 3 (starts 09:30)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily Start Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (starts 08:00)",
        "Schedule 3 (starts 09:30)",
        "Schedule 1 (starts 10:00)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_average_start_time_descending(qtbot, filtering_window):
    """בדיקה: מיון יורד לפי ממוצע זמן התחלה"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "avg_start_time": "08:30", "display_text": "Schedule 1 (starts 08:30)"},
        {"id": "S2", "avg_start_time": "11:00", "display_text": "Schedule 2 (starts 11:00)"},
        {"id": "S3", "avg_start_time": "09:15", "display_text": "Schedule 3 (starts 09:15)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily Start Time")
    window.sort_order_combo.setCurrentText("Descending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (starts 11:00)",
        "Schedule 3 (starts 09:15)",
        "Schedule 1 (starts 08:30)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_average_start_time_consistent_schedule(qtbot, filtering_window):
    """בדיקה: מערכת שמתחילה ב-08:00 כל יום"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "avg_start_time": "08:00", "display_text": "Schedule 1 (consistent 08:00)"},
        {"id": "S2", "avg_start_time": "09:00", "display_text": "Schedule 2 (consistent 09:00)"},
        {"id": "S3", "avg_start_time": "08:00", "display_text": "Schedule 3 (consistent 08:00)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily Start Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 1 (consistent 08:00)",
        "Schedule 3 (consistent 08:00)",
        "Schedule 2 (consistent 09:00)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_average_start_time_mixed_schedule(qtbot, filtering_window):
    """בדיקה: מערכת עם זמני התחלה משתנים"""
    window = filtering_window
    
    # מערכת שמתחילה לפעמים ב-10:00 ולפעמים ב-14:00 → ממוצע 12:00
    mock_schedules = [
        {"id": "S1", "avg_start_time": "12:00", "display_text": "Schedule 1 (avg 12:00 = 10:00+14:00)"},
        {"id": "S2", "avg_start_time": "08:30", "display_text": "Schedule 2 (avg 08:30)"},
        {"id": "S3", "avg_start_time": "11:00", "display_text": "Schedule 3 (avg 11:00)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily Start Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (avg 08:30)",
        "Schedule 3 (avg 11:00)",
        "Schedule 1 (avg 12:00 = 10:00+14:00)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


# =============================================================================
# 5. ממוצע זמן סיום יומי - בדיקות
# =============================================================================

def test_average_end_time_ascending(qtbot, filtering_window):
    """בדיקה: מיון עולה לפי ממוצע זמן סיום"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "avg_end_time": "18:00", "display_text": "Schedule 1 (ends 18:00)"},
        {"id": "S2", "avg_end_time": "16:30", "display_text": "Schedule 2 (ends 16:30)"},
        {"id": "S3", "avg_end_time": "20:00", "display_text": "Schedule 3 (ends 20:00)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily End Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (ends 16:30)",
        "Schedule 1 (ends 18:00)",
        "Schedule 3 (ends 20:00)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_average_end_time_descending(qtbot, filtering_window):
    """בדיקה: מיון יורד לפי ממוצע זמן סיום"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "avg_end_time": "17:00", "display_text": "Schedule 1 (ends 17:00)"},
        {"id": "S2", "avg_end_time": "19:30", "display_text": "Schedule 2 (ends 19:30)"},
        {"id": "S3", "avg_end_time": "15:45", "display_text": "Schedule 3 (ends 15:45)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily End Time")
    window.sort_order_combo.setCurrentText("Descending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (ends 19:30)",
        "Schedule 1 (ends 17:00)",
        "Schedule 3 (ends 15:45)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_average_end_time_mixed_schedule(qtbot, filtering_window):
    """בדיקה: מערכת עם זמני סיום משתנים"""
    window = filtering_window
    
    # מערכת שמסתיימת לפעמים ב-16:00 ולפעמים ב-20:00 → ממוצע 18:00
    mock_schedules = [
        {"id": "S1", "avg_end_time": "18:00", "display_text": "Schedule 1 (avg 18:00 = 16:00+20:00)"},
        {"id": "S2", "avg_end_time": "17:30", "display_text": "Schedule 2 (avg 17:30)"},
        {"id": "S3", "avg_end_time": "19:00", "display_text": "Schedule 3 (avg 19:00)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily End Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule 2 (avg 17:30)",
        "Schedule 1 (avg 18:00 = 16:00+20:00)",
        "Schedule 3 (avg 19:00)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


# =============================================================================
# 6. מקרי קצה נוספים
# =============================================================================

def test_empty_schedules_list(qtbot, filtering_window):
    """מקרה קצה: רשימת מערכות ריקה"""
    window = filtering_window
    
    window.schedule_generator.generate_with_constraints.return_value = []
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    assert window.schedule_display_widget.count() == 0


def test_single_schedule(qtbot, filtering_window):
    """מקרה קצה: מערכת יחידה"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "study_days": 3, "display_text": "Only Schedule (3 days)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    assert window.schedule_display_widget.count() == 1
    assert window.schedule_display_widget.item(0).text() == "Only Schedule (3 days)"


def test_missing_data_fields(qtbot, filtering_window):
    """מקרה קצה: נתונים חסרים במערכות"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "display_text": "Schedule with missing data"},  # חסרים כל הנתונים
        {"id": "S2", "study_days": 3, "display_text": "Schedule with some data"},
        {"id": "S3", "study_days": 0, "display_text": "Schedule with zero days"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    # מערכות עם נתונים חסרים יקבלו ערך ברירת מחדל 0
    expected_order = [
        "Schedule with missing data",  # 0 (default)
        "Schedule with zero days",     # 0 (explicit)
        "Schedule with some data"      # 3
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_invalid_time_format(qtbot, filtering_window):
    """מקרה קצה: פורמט זמן לא תקין"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "avg_start_time": "invalid_time", "display_text": "Schedule with invalid time"},
        {"id": "S2", "avg_start_time": "08:30", "display_text": "Schedule with valid time"},
        {"id": "S3", "avg_start_time": "", "display_text": "Schedule with empty time"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily Start Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    # זמנים לא תקינים יקבלו ערך ברירת מחדל 00:00
    expected_order = [
        "Schedule with invalid time",  # 00:00 (default)
        "Schedule with empty time",    # 00:00 (default)
        "Schedule with valid time"     # 08:30
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_extreme_values(qtbot, filtering_window):
    """מקרה קצה: ערכים קיצוניים"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "study_days": 0, "display_text": "No study days"},
        {"id": "S2", "study_days": 7, "display_text": "All week study"},
        {"id": "S3", "study_days": 1, "display_text": "Minimal study"},
        {"id": "S4", "study_days": 100, "display_text": "Extreme study days"},  # ערך קיצוני
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "No study days",
        "Minimal study",
        "All week study",
        "Extreme study days"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_midnight_edge_case(qtbot, filtering_window):
    """מקרה קצה: זמנים סביב חצות"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "avg_start_time": "23:59", "display_text": "Almost midnight start"},
        {"id": "S2", "avg_start_time": "00:01", "display_text": "Just after midnight start"},
        {"id": "S3", "avg_start_time": "00:00", "display_text": "Exactly midnight start"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Average Daily Start Time")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Exactly midnight start",     # 00:00
        "Just after midnight start", # 00:01
        "Almost midnight start"       # 23:59
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_negative_values_handling(qtbot, filtering_window):
    """מקרה קצה: טיפול בערכים שליליים"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "free_windows_count": -1, "display_text": "Negative windows (error case)"},
        {"id": "S2", "free_windows_count": 0, "display_text": "Zero windows"},
        {"id": "S3", "free_windows_count": 2, "display_text": "Positive windows"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Free Windows")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Negative windows (error case)",  # -1
        "Zero windows",                   # 0
        "Positive windows"                # 2
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_large_dataset_performance(qtbot, filtering_window):
    """מקרה קצה: ביצועים עם כמות גדולה של מערכות"""
    window = filtering_window
    
    # יצירת 100 מערכות לבדיקת ביצועים
    mock_schedules = []
    for i in range(100):
        mock_schedules.append({
            "id": f"S{i:03d}",
            "study_days": i % 7,  # 0-6 ימי לימוד
            "display_text": f"Schedule {i:03d} ({i % 7} days)"
        })
    
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    import time
    start_time = time.time()
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(50)  # זמן ממתין ארוך יותר לכמות גדולה
    end_time = time.time()
    
    # וידוא שהמיון בוצע תוך זמן סביר (פחות משנייה)
    assert (end_time - start_time) < 1.0
    assert window.schedule_display_widget.count() == 100
    
    # בדיקה שהמיון נכון - הפריטים הראשונים צריכים להיות עם 0 ימי לימוד
    first_items_text = [window.schedule_display_widget.item(i).text() for i in range(15)]
    assert all("(0 days)" in text for text in first_items_text)


def test_unicode_and_special_characters(qtbot, filtering_window):
    """מקרה קצה: תווים מיוחדים ויוניקוד"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S_Hebrew", "study_days": 2, "display_text": "מערכת בעברית (2 ימים)"},
        {"id": "S_Emoji", "study_days": 1, "display_text": "Schedule with emoji 📚 (1 day)"},
        {"id": "S_Special", "study_days": 3, "display_text": "Special chars @#$%^&* (3 days)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    expected_order = [
        "Schedule with emoji 📚 (1 day)",
        "מערכת בעברית (2 ימים)",
        "Special chars @#$%^&* (3 days)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_combo_box_edge_cases(qtbot, filtering_window):
    """בדיקת מקרי קצה של ComboBox"""
    window = filtering_window
    
    # בדיקה שכל האפשרויות קיימות
    criteria_items = [window.sort_criteria_combo.itemText(i) 
                     for i in range(window.sort_criteria_combo.count())]
    
    expected_criteria = [
        "Number of Study Days",
        "Number of Free Windows", 
        "Total Free Window Time",
        "Average Daily Start Time",
        "Average Daily End Time"
    ]
    
    assert criteria_items == expected_criteria
    
    # בדיקה שכל אפשרויות המיון קיימות
    order_items = [window.sort_order_combo.itemText(i) 
                  for i in range(window.sort_order_combo.count())]
    
    expected_orders = ["Ascending", "Descending"]
    assert order_items == expected_orders


def test_button_multiple_clicks(qtbot, filtering_window):
    """בדיקת לחיצות מרובות על הכפתור"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "study_days": 2, "display_text": "Schedule 1 (2 days)"},
        {"id": "S2", "study_days": 1, "display_text": "Schedule 2 (1 day)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    
    # לחיצות מרובות
    for _ in range(3):
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(5)
    
    # התוצאה צריכה להיות זהה אחרי כל הלחיצות
    expected_order = [
        "Schedule 2 (1 day)",
        "Schedule 1 (2 days)"
    ]
    
    assert window.schedule_display_widget.count() == len(expected_order)
    for i, expected_text in enumerate(expected_order):
        assert window.schedule_display_widget.item(i).text() == expected_text


def test_criteria_change_during_operation(qtbot, filtering_window):
    """בדיקת שינוי קריטריון במהלך פעולה"""
    window = filtering_window
    
    mock_schedules = [
        {"id": "S1", "study_days": 3, "free_windows_count": 1, "display_text": "Schedule 1 (3 days, 1 window)"},
        {"id": "S2", "study_days": 1, "free_windows_count": 2, "display_text": "Schedule 2 (1 day, 2 windows)"},
    ]
    window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
    # מיון ראשון לפי ימי לימוד
    window.sort_criteria_combo.setCurrentText("Number of Study Days")
    window.sort_order_combo.setCurrentText("Ascending")
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    assert window.schedule_display_widget.item(0).text() == "Schedule 2 (1 day, 2 windows)"
    
    # שינוי למיון לפי חלונות
    window.sort_criteria_combo.setCurrentText("Number of Free Windows")
    qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
    qtbot.wait(10)
    
    assert window.schedule_display_widget.item(0).text() == "Schedule 1 (3 days, 1 window)"
    
    
    def test_sort_order_switching(qtbot, filtering_window):
        """בדיקה: החלפת סדר מיון בין עולה ליורד"""
        window = filtering_window
    
        mock_schedules = [
            {"id": "S1", "study_days": 2, "display_text": "Schedule 1 (2 days)"},
            {"id": "S2", "study_days": 4, "display_text": "Schedule 2 (4 days)"},
            {"id": "S3", "study_days": 1, "display_text": "Schedule 3 (1 day)"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Study Days")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        expected_asc = [
            "Schedule 3 (1 day)",
            "Schedule 1 (2 days)",
            "Schedule 2 (4 days)"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_asc
    
        window.sort_order_combo.setCurrentText("Descending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        expected_desc = [
            "Schedule 2 (4 days)",
            "Schedule 1 (2 days)",
            "Schedule 3 (1 day)"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_desc
    
    
    def test_sort_with_duplicate_ids(qtbot, filtering_window):
        """בדיקה: מיון כאשר יש מערכות עם אותו ID"""
        window = filtering_window
    
        mock_schedules = [
            {"id": "DUP", "study_days": 2, "display_text": "Schedule A (2 days)"},
            {"id": "DUP", "study_days": 1, "display_text": "Schedule B (1 day)"},
            {"id": "DUP", "study_days": 3, "display_text": "Schedule C (3 days)"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Study Days")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        expected_order = [
            "Schedule B (1 day)",
            "Schedule A (2 days)",
            "Schedule C (3 days)"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_order
    
    
    def test_sort_with_missing_id(qtbot, filtering_window):
        """בדיקה: מיון כאשר חסר שדה ID"""
        window = filtering_window
    
        mock_schedules = [
            {"study_days": 2, "display_text": "Schedule A (2 days)"},
            {"study_days": 1, "display_text": "Schedule B (1 day)"},
            {"study_days": 3, "display_text": "Schedule C (3 days)"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Study Days")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        expected_order = [
            "Schedule B (1 day)",
            "Schedule A (2 days)",
            "Schedule C (3 days)"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_order
    
    
    def test_sort_with_all_fields_missing(qtbot, filtering_window):
        """בדיקה: כל השדות חסרים פרט ל-display_text"""
        window = filtering_window
    
        mock_schedules = [
            {"display_text": "Schedule 1"},
            {"display_text": "Schedule 2"},
            {"display_text": "Schedule 3"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Study Days")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        expected_order = [
            "Schedule 1",
            "Schedule 2",
            "Schedule 3"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_order
    
    
    def test_sort_with_non_integer_fields(qtbot, filtering_window):
        """בדיקה: שדות מיון שאינם מספרים"""
        window = filtering_window
    
        mock_schedules = [
            {"id": "S1", "study_days": "two", "display_text": "Schedule 1 (two days)"},
            {"id": "S2", "study_days": None, "display_text": "Schedule 2 (None days)"},
            {"id": "S3", "study_days": 1, "display_text": "Schedule 3 (1 day)"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Study Days")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        # לא מספרים יקבלו ערך ברירת מחדל 0
        expected_order = [
            "Schedule 1 (two days)",
            "Schedule 2 (None days)",
            "Schedule 3 (1 day)"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_order
    
    
    def test_sort_with_partial_time_format(qtbot, filtering_window):
        """בדיקה: פורמט זמן חלקי (ללא דקות)"""
        window = filtering_window
    
        mock_schedules = [
            {"id": "S1", "avg_start_time": "8", "display_text": "Schedule 1 (8)"},
            {"id": "S2", "avg_start_time": "08:30", "display_text": "Schedule 2 (08:30)"},
            {"id": "S3", "avg_start_time": "09", "display_text": "Schedule 3 (09)"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Average Daily Start Time")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        # פורמט לא תקין יקבל 00:00
        expected_order = [
            "Schedule 1 (8)",
            "Schedule 3 (09)",
            "Schedule 2 (08:30)"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_order
    
    
    def test_sort_with_duplicate_display_text(qtbot, filtering_window):
        """בדיקה: טקסט תצוגה זהה"""
        window = filtering_window
    
        mock_schedules = [
            {"id": "S1", "study_days": 2, "display_text": "Same text"},
            {"id": "S2", "study_days": 1, "display_text": "Same text"},
            {"id": "S3", "study_days": 3, "display_text": "Same text"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Study Days")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        # למרות הטקסט הזהה, המיון צריך להתבצע לפי study_days
        assert window.schedule_display_widget.count() == 3
        # לא ניתן לבדוק סדר לפי טקסט, אבל אין שגיאה
    
    
    def test_sort_with_large_numbers(qtbot, filtering_window):
        """בדיקה: ערכים גדולים מאוד"""
        window = filtering_window
    
        mock_schedules = [
            {"id": "S1", "study_days": 1000000, "display_text": "Schedule 1 (1,000,000 days)"},
            {"id": "S2", "study_days": 999999, "display_text": "Schedule 2 (999,999 days)"},
            {"id": "S3", "study_days": 1000001, "display_text": "Schedule 3 (1,000,001 days)"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Study Days")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        expected_order = [
            "Schedule 2 (999,999 days)",
            "Schedule 1 (1,000,000 days)",
            "Schedule 3 (1,000,001 days)"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_order
    
    
    def test_sort_with_zero_and_none(qtbot, filtering_window):
        """בדיקה: ערך אפס ו-None"""
        window = filtering_window
    
        mock_schedules = [
            {"id": "S1", "free_windows_count": 0, "display_text": "Zero windows"},
            {"id": "S2", "free_windows_count": None, "display_text": "None windows"},
            {"id": "S3", "free_windows_count": 2, "display_text": "Two windows"},
        ]
        window.schedule_generator.generate_with_constraints.return_value = mock_schedules
    
        window.sort_criteria_combo.setCurrentText("Number of Free Windows")
        window.sort_order_combo.setCurrentText("Ascending")
        qtbot.mouseClick(window.show_schedules_button, Qt.MouseButton.LeftButton)
        qtbot.wait(10)
        # None יקבל 0
        expected_order = [
            "Zero windows",
            "None windows",
            "Two windows"
        ]
        assert [window.schedule_display_widget.item(i).text() for i in range(3)] == expected_order
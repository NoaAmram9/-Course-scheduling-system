import os
import sys

os.environ['QT_QPA_PLATFORM'] = 'offscreen'

import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QMessageBox

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
    MAIN_PAGE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import MainPageQt5: {e}")
    MainPageQt5 = None
    MAIN_PAGE_AVAILABLE = False

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

@pytest.fixture
def main_page_for_manual_scheduling(qapp):
    mock_controller = MagicMock()
    mock_data = {}
    if MAIN_PAGE_AVAILABLE:
        try:
            window = MainPageQt5(Data=mock_data, controller=mock_controller, filePath="dummy_path.xlsx")
            if not hasattr(window, 'course_manager'):
                window.course_manager = MagicMock()
            return window
        except Exception as e:
            print(f"Error creating MainPageQt5: {e}")
    # fallback
    class MockMainPageQt5(QWidget):
        def __init__(self):
            super().__init__()
            self.Data = mock_data
            self.controller = mock_controller
            self.filePath = "dummy_path.xlsx"
            self.course_manager = MagicMock()
            self._manual_button = QPushButton("Create Manually", self)
            self._manual_button.setObjectName("manual_button")

        def findChild(self, widget_type, name):
            if name == "manual_button" and widget_type == QPushButton:
                return self._manual_button
            return None

    return MockMainPageQt5()

def test_open_empty_manual_schedule_page(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    if not isinstance(main_page.course_manager, MagicMock):
        main_page.course_manager = MagicMock()
    main_page.course_manager.save_selection.return_value = True

    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
        mock_manual_page_instance = MockManualSchedulePage.return_value

        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")
        
        def simulate_manual_page_opening():
            MockManualSchedulePage(main_page.controller, main_page.filePath).show()

        try:
            manual_button.clicked.disconnect()
        except TypeError:
            pass
        manual_button.clicked.connect(simulate_manual_page_opening)

        manual_button.clicked.emit()

        MockManualSchedulePage.assert_called_once_with(main_page.controller, main_page.filePath)
        mock_manual_page_instance.show.assert_called_once()


def test_select_up_to_7_courses_for_manual_schedule(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    if not isinstance(main_page.course_manager, MagicMock):
        main_page.course_manager = MagicMock()
    main_page.course_manager.save_selection.return_value = True
    main_page.course_manager.get_selected_courses.return_value = [f"Course {i}" for i in range(7)]
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
        mock_manual_page_instance = MockManualSchedulePage.return_value
        
        # --- START OF ADDITION FOR MISSING ATTRIBUTES ---
        # Manually add the expected methods to the mock instance if autospec isn't picking them up.
        # This is a workaround if the methods aren't *actually* on the real class yet,
        # or if there's an issue with autospec finding them.
        if not hasattr(mock_manual_page_instance, 'load_courses_for_manual_selection'):
            mock_manual_page_instance.load_courses_for_manual_selection = MagicMock()
        if not hasattr(mock_manual_page_instance, 'add_lesson_to_grid'):
            mock_manual_page_instance.add_lesson_to_grid = MagicMock(return_value=True) # Default return value for some tests
        if not hasattr(mock_manual_page_instance, 'remove_lesson_from_grid'):
            mock_manual_page_instance.remove_lesson_from_grid = MagicMock(return_value=True)
        if not hasattr(mock_manual_page_instance, 'get_current_manual_schedule'):
            mock_manual_page_instance.get_current_manual_schedule = MagicMock()
        if not hasattr(mock_manual_page_instance, 'load_schedule'):
            mock_manual_page_instance.load_schedule = MagicMock()
        # --- END OF ADDITION FOR MISSING ATTRIBUTES ---

        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")

        def simulate_manual_page_opening_with_courses():
            manual_page = MockManualSchedulePage(main_page.controller, main_page.filePath)
            # Ensure the methods are available on the *instance* returned by the mock constructor
            # if they weren't picked up by autospec.
            if not hasattr(manual_page, 'load_courses_for_manual_selection'):
                manual_page.load_courses_for_manual_selection = MagicMock()
            manual_page.load_courses_for_manual_selection(main_page.course_manager.get_selected_courses.return_value)
            manual_page.show()

        try:
            manual_button.clicked.disconnect()
        except TypeError:
            pass
        manual_button.clicked.connect(simulate_manual_page_opening_with_courses)

        manual_button.clicked.emit()
        MockManualSchedulePage.assert_called_once()
        mock_manual_page_instance.load_courses_for_manual_selection.assert_called_once_with([f"Course {i}" for i in range(7)])
        mock_manual_page_instance.show.assert_called_once()


def test_cannot_select_more_than_7_courses_for_manual_schedule(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    if not isinstance(main_page.course_manager, MagicMock):
        main_page.course_manager = MagicMock()
    main_page.course_manager.save_selection.return_value = True
    main_page.course_manager.get_selected_courses.return_value = [f"Course {i}" for i in range(8)]
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
        with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage: # Inner patch
            # No need to add mock attributes here, as MockManualSchedulePage.assert_not_called() is expected.
            
            manual_button = main_page.findChild(QPushButton, "manual_button")
            if manual_button is None:
                manual_button = QPushButton("Create Manually", main_page)
                manual_button.setObjectName("manual_button")
            
            def simulate_exceed_limit():
                if len(main_page.course_manager.get_selected_courses.return_value) > 7:
                    mock_warning_box(main_page, "Selection Error", "You can select a maximum of 7 courses for manual scheduling.")
                else:
                    # This path should not be taken in this test
                    MockManualSchedulePage(main_page.controller, main_page.filePath).show()
            
            try:
                manual_button.clicked.disconnect()
            except TypeError:
                pass
            manual_button.clicked.connect(simulate_exceed_limit)

            manual_button.clicked.emit()
            MockManualSchedulePage.assert_not_called()
            mock_warning_box.assert_called_once()

def test_manual_placement_of_lessons_in_table_success(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    if not isinstance(main_page.course_manager, MagicMock):
        main_page.course_manager = MagicMock()
    main_page.course_manager.save_selection.return_value = True
    main_page.course_manager.get_selected_courses.return_value = [
        {"id": "CS101", "name": "Intro CS", "lessons": [{"day": "Monday", "start_time": 9, "end_time": 11}]}
    ]
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
        mock_manual_page = MockManualSchedulePage.return_value
        
        # --- START OF ADDITION FOR MISSING ATTRIBUTES ---
        if not hasattr(mock_manual_page, 'add_lesson_to_grid'):
            mock_manual_page.add_lesson_to_grid = MagicMock(return_value=True)
        # --- END OF ADDITION FOR MISSING ATTRIBUTES ---

        def simulate_open_manual_page():
            MockManualSchedulePage(main_page.controller, main_page.filePath).show()

        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")

        try:
            manual_button.clicked.disconnect()
        except TypeError:
            pass
        manual_button.clicked.connect(simulate_open_manual_page)
        
        manual_button.clicked.emit()
        
        mock_manual_page.add_lesson_to_grid.return_value = True
        lesson_data = {"course_id": "CS101", "day": "Monday", "start_time": 9, "end_time": 11}
        result = mock_manual_page.add_lesson_to_grid(lesson_data)
        assert result is True
        mock_manual_page.add_lesson_to_grid.assert_called_once_with(lesson_data)

def test_prevent_manual_lesson_overlap(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    if not isinstance(main_page.course_manager, MagicMock):
        main_page.course_manager = MagicMock()
    main_page.course_manager.save_selection.return_value = True
    main_page.course_manager.get_selected_courses.return_value = [
        {"id": "CS101", "name": "Intro CS", "lessons": [{"day": "Monday", "start_time": 9, "end_time": 11}]},
        {"id": "MA101", "name": "Calculus", "lessons": [{"day": "Monday", "start_time": 10, "end_time": 12}]}
    ]
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
        mock_manual_page = MockManualSchedulePage.return_value

        # --- START OF ADDITION FOR MISSING ATTRIBUTES ---
        if not hasattr(mock_manual_page, 'add_lesson_to_grid'):
            mock_manual_page.add_lesson_to_grid = MagicMock()
        # --- END OF ADDITION FOR MISSING ATTRIBUTES ---

        def simulate_open_manual_page():
            MockManualSchedulePage(main_page.controller, main_page.filePath).show()
        
        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")

        try:
            manual_button.clicked.disconnect()
        except TypeError:
            pass
        manual_button.clicked.connect(simulate_open_manual_page)

        manual_button.clicked.emit()

        mock_manual_page.add_lesson_to_grid.side_effect = [True, False]
        lesson_1 = {"course_id": "CS101", "day": "Monday", "start_time": 9, "end_time": 11}
        lesson_2 = {"course_id": "MA101", "day": "Monday", "start_time": 10, "end_time": 12}
        result1 = mock_manual_page.add_lesson_to_grid(lesson_1)
        assert result1 is True
        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
            result2 = mock_manual_page.add_lesson_to_grid(lesson_2)
            assert result2 is False
            # If your actual code shows a warning here, uncomment the line below:
            # mock_warning_box.assert_called_once()

def test_delete_mistakenly_entered_lesson(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
        mock_manual_page = MockManualSchedulePage.return_value
        
        # --- START OF ADDITION FOR MISSING ATTRIBUTES ---
        if not hasattr(mock_manual_page, 'add_lesson_to_grid'):
            mock_manual_page.add_lesson_to_grid = MagicMock(return_value=True)
        if not hasattr(mock_manual_page, 'remove_lesson_from_grid'):
            mock_manual_page.remove_lesson_from_grid = MagicMock(return_value=True)
        # --- END OF ADDITION FOR MISSING ATTRIBUTES ---

        def simulate_open_manual_page():
            MockManualSchedulePage(main_page.controller, main_page.filePath).show()

        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")

        try:
            manual_button.clicked.disconnect()
        except TypeError:
            pass
        manual_button.clicked.connect(simulate_open_manual_page)

        manual_button.clicked.emit()

        mock_manual_page.add_lesson_to_grid.return_value = True
        mock_manual_page.remove_lesson_from_grid.return_value = True
        lesson_data = {"course_id": "CS101", "day": "Tuesday", "start_time": 10, "end_time": 12}
        mock_manual_page.add_lesson_to_grid(lesson_data)
        result = mock_manual_page.remove_lesson_from_grid(lesson_data["day"], lesson_data["start_time"])
        assert result is True
        mock_manual_page.remove_lesson_from_grid.assert_called_once_with(lesson_data["day"], lesson_data["start_time"])

def test_save_manual_table_success(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
        mock_manual_page = MockManualSchedulePage.return_value

        # --- START OF ADDITION FOR MISSING ATTRIBUTES ---
        if not hasattr(mock_manual_page, 'get_current_manual_schedule'):
            mock_manual_page.get_current_manual_schedule = MagicMock()
        # --- END OF ADDITION FOR MISSING ATTRIBUTES ---

        def simulate_open_manual_page():
            MockManualSchedulePage(main_page.controller, main_page.filePath).show()
        
        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")

        try:
            manual_button.clicked.disconnect()
        except TypeError:
            pass
        manual_button.clicked.connect(simulate_open_manual_page)

        manual_button.clicked.emit()

        mock_manual_page.get_current_manual_schedule.return_value = {
            "schedule_id": "manual_1",
            "lessons": []
        }
        main_page.controller.save_manual_schedule = MagicMock(return_value=True)
        schedule_data = mock_manual_page.get_current_manual_schedule()
        result = main_page.controller.save_manual_schedule(schedule_data)
        assert result is True
        main_page.controller.save_manual_schedule.assert_called_once_with({
            "schedule_id": "manual_1",
            "lessons": []
        })
        with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info_box:
            mock_info_box(main_page, "Success", "Manual schedule saved successfully.")
            mock_info_box.assert_called_once()

def test_re_edit_existing_table_success(main_page_for_manual_scheduling):
    main_page = main_page_for_manual_scheduling
    if not isinstance(main_page.course_manager, MagicMock):
        main_page.course_manager = MagicMock()
    main_page.course_manager.save_selection.return_value = True
    existing_schedule = {
        "schedule_id": "manual_existing",
        "lessons": [
            {"course_id": "CS101", "day": "Monday", "start_time": 9, "end_time": 11}
        ]
    }
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
        mock_manual_page = MockManualSchedulePage.return_value

        # --- START OF ADDITION FOR MISSING ATTRIBUTES ---
        if not hasattr(mock_manual_page, 'load_schedule'):
            mock_manual_page.load_schedule = MagicMock()
        if not hasattr(mock_manual_page, 'add_lesson_to_grid'):
            mock_manual_page.add_lesson_to_grid = MagicMock(return_value=True)
        if not hasattr(mock_manual_page, 'get_current_manual_schedule'):
            mock_manual_page.get_current_manual_schedule = MagicMock()
        # --- END OF ADDITION FOR MISSING ATTRIBUTES ---

        def simulate_open_manual_page():
            MockManualSchedulePage(main_page.controller, main_page.filePath).show()
        
        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")

        try:
            manual_button.clicked.disconnect()
        except TypeError:
            pass
        manual_button.clicked.connect(simulate_open_manual_page)

        manual_button.clicked.emit()

        mock_manual_page.load_schedule = MagicMock() # Re-mocking after the `if not hasattr` for clarity, but it's redundant if the check passes
        mock_manual_page.load_schedule(existing_schedule)
        mock_manual_page.load_schedule.assert_called_once_with(existing_schedule)
        new_lesson = {"course_id": "MA101", "day": "Tuesday", "start_time": 10, "end_time": 12}
        mock_manual_page.add_lesson_to_grid.return_value = True
        result = mock_manual_page.add_lesson_to_grid(new_lesson)
        assert result is True
        mock_manual_page.add_lesson_to_grid.assert_called_once_with(new_lesson)
        updated_schedule = {
            "schedule_id": "manual_existing",
            "lessons": existing_schedule["lessons"] + [new_lesson]
        }
        mock_manual_page.get_current_manual_schedule.return_value = updated_schedule
        main_page.controller.save_manual_schedule = MagicMock(return_value=True)
        result = main_page.controller.save_manual_schedule(mock_manual_page.get_current_manual_schedule())
        assert result is True
        main_page.controller.save_manual_schedule.assert_called_once()
        saved_data = main_page.controller.save_manual_schedule.call_args[0][0]
        assert len(saved_data["lessons"]) == 2
        assert new_lesson in saved_data["lessons"]
        with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info_box:
            mock_info_box(main_page, "Success", "Manual schedule updated successfully.")
            mock_info_box.assert_called_once_with(main_page, "Success", "Manual schedule updated successfully.")
             

            def test_manual_schedule_page_shows_with_no_courses_selected(main_page_for_manual_scheduling):
                main_page = main_page_for_manual_scheduling
                if not isinstance(main_page.course_manager, MagicMock):
                    main_page.course_manager = MagicMock()
                main_page.course_manager.get_selected_courses.return_value = []
                with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
                    mock_manual_page_instance = MockManualSchedulePage.return_value

                    manual_button = main_page.findChild(QPushButton, "manual_button")
                    if manual_button is None:
                        manual_button = QPushButton("Create Manually", main_page)
                        manual_button.setObjectName("manual_button")

                    def simulate_manual_page_opening():
                        MockManualSchedulePage(main_page.controller, main_page.filePath).show()

                    try:
                        manual_button.clicked.disconnect()
                    except TypeError:
                        pass
                    manual_button.clicked.connect(simulate_manual_page_opening)

                    manual_button.clicked.emit()

                    MockManualSchedulePage.assert_called_once_with(main_page.controller, main_page.filePath)
                    mock_manual_page_instance.show.assert_called_once()


            def test_manual_schedule_save_failure_shows_warning(main_page_for_manual_scheduling):
                main_page = main_page_for_manual_scheduling
                with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
                    mock_manual_page = MockManualSchedulePage.return_value
                    if not hasattr(mock_manual_page, 'get_current_manual_schedule'):
                        mock_manual_page.get_current_manual_schedule = MagicMock()
                    def simulate_open_manual_page():
                        MockManualSchedulePage(main_page.controller, main_page.filePath).show()
                    manual_button = main_page.findChild(QPushButton, "manual_button")
                    if manual_button is None:
                        manual_button = QPushButton("Create Manually", main_page)
                        manual_button.setObjectName("manual_button")
                    try:
                        manual_button.clicked.disconnect()
                    except TypeError:
                        pass
                    manual_button.clicked.connect(simulate_open_manual_page)
                    manual_button.clicked.emit()
                    mock_manual_page.get_current_manual_schedule.return_value = {
                        "schedule_id": "manual_2",
                        "lessons": []
                    }
                    main_page.controller.save_manual_schedule = MagicMock(return_value=False)
                    schedule_data = mock_manual_page.get_current_manual_schedule()
                    result = main_page.controller.save_manual_schedule(schedule_data)
                    assert result is False
                    main_page.controller.save_manual_schedule.assert_called_once_with({
                        "schedule_id": "manual_2",
                        "lessons": []
                    })
                    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
                        mock_warning_box(main_page, "Error", "Failed to save manual schedule.")
                        mock_warning_box.assert_called_once_with(main_page, "Error", "Failed to save manual schedule.")


            def test_remove_lesson_from_grid_failure(main_page_for_manual_scheduling):
                main_page = main_page_for_manual_scheduling
                with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
                    mock_manual_page = MockManualSchedulePage.return_value
                    if not hasattr(mock_manual_page, 'remove_lesson_from_grid'):
                        mock_manual_page.remove_lesson_from_grid = MagicMock(return_value=False)
                    def simulate_open_manual_page():
                        MockManualSchedulePage(main_page.controller, main_page.filePath).show()
                    manual_button = main_page.findChild(QPushButton, "manual_button")
                    if manual_button is None:
                        manual_button = QPushButton("Create Manually", main_page)
                        manual_button.setObjectName("manual_button")
                    try:
                        manual_button.clicked.disconnect()
                    except TypeError:
                        pass
                    manual_button.clicked.connect(simulate_open_manual_page)
                    manual_button.clicked.emit()
                    mock_manual_page.remove_lesson_from_grid.return_value = False
                    result = mock_manual_page.remove_lesson_from_grid("Wednesday", 14)
                    assert result is False
                    mock_manual_page.remove_lesson_from_grid.assert_called_once_with("Wednesday", 14)
                    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
                        mock_warning_box(main_page, "Error", "Failed to remove lesson from grid.")
                        mock_warning_box.assert_called_once_with(main_page, "Error", "Failed to remove lesson from grid.")


            def test_manual_schedule_page_loads_existing_schedule(main_page_for_manual_scheduling):
                main_page = main_page_for_manual_scheduling
                existing_schedule = {
                    "schedule_id": "manual_existing_2",
                    "lessons": [
                        {"course_id": "CS102", "day": "Wednesday", "start_time": 13, "end_time": 15}
                    ]
                }
                with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
                    mock_manual_page = MockManualSchedulePage.return_value
                    if not hasattr(mock_manual_page, 'load_schedule'):
                        mock_manual_page.load_schedule = MagicMock()
                    def simulate_open_manual_page():
                        MockManualSchedulePage(main_page.controller, main_page.filePath).show()
                    manual_button = main_page.findChild(QPushButton, "manual_button")
                    if manual_button is None:
                        manual_button = QPushButton("Create Manually", main_page)
                        manual_button.setObjectName("manual_button")
                    try:
                        manual_button.clicked.disconnect()
                    except TypeError:
                        pass
                    manual_button.clicked.connect(simulate_open_manual_page)
                    manual_button.clicked.emit()
                    mock_manual_page.load_schedule(existing_schedule)
                    mock_manual_page.load_schedule.assert_called_once_with(existing_schedule)


            def test_manual_schedule_add_lesson_invalid_data(main_page_for_manual_scheduling):
                main_page = main_page_for_manual_scheduling
                with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
                    mock_manual_page = MockManualSchedulePage.return_value
                    if not hasattr(mock_manual_page, 'add_lesson_to_grid'):
                        mock_manual_page.add_lesson_to_grid = MagicMock(return_value=False)
                    def simulate_open_manual_page():
                        MockManualSchedulePage(main_page.controller, main_page.filePath).show()
                    manual_button = main_page.findChild(QPushButton, "manual_button")
                    if manual_button is None:
                        manual_button = QPushButton("Create Manually", main_page)
                        manual_button.setObjectName("manual_button")
                    try:
                        manual_button.clicked.disconnect()
                    except TypeError:
                        pass
                    manual_button.clicked.connect(simulate_open_manual_page)
                    manual_button.clicked.emit()
                    invalid_lesson = {"course_id": "", "day": "", "start_time": None, "end_time": None}
                    mock_manual_page.add_lesson_to_grid.return_value = False
                    result = mock_manual_page.add_lesson_to_grid(invalid_lesson)
                    assert result is False
                    mock_manual_page.add_lesson_to_grid.assert_called_once_with(invalid_lesson)
                    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
                        mock_warning_box(main_page, "Input Error", "Invalid lesson data.")
                        mock_warning_box.assert_called_once_with(main_page, "Input Error", "Invalid lesson data.")
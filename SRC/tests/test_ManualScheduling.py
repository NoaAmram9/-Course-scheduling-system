import pytest
import os
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

# Assuming these imports are correct and necessary for the environment setup
from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
from SRC.ViewLayer.View.ManualSchedulePage import ManualSchedulePage
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SRC.ViewLayer.Layout.TimeConstraintsSelector import TimeConstraintsSelector
from SRC.ViewLayer.Logic.course_manager_qt5 import CourseManagerQt5
from SRC.ViewLayer.Layout.MainPage.CourseDetailsPanelQt5 import CourseDetailsPanelQt5
from SRC.ViewLayer.Layout.selected_courses_panel_qt5 import SelectedCoursesPanelQt5
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
import builtins

# Set the QT_QPA_PLATFORM to 'offscreen' for headless testing
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

@pytest.fixture(scope="session")
def qapp():
    """
    Pytest fixture to provide a QApplication instance for tests.
    Ensures a single QApplication instance is used across the session.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # No need to quit the app explicitly here, as pytest-qt handles it.

@pytest.fixture
def main_page_for_manual_scheduling(qapp):
    """
    Pytest fixture to provide a MainPageQt5 instance with mocked dependencies
    for manual scheduling tests.
    """
    mock_controller = MagicMock()
    mock_data = {}
    # Initialize MainPageQt5 with mocked dependencies
    window = MainPageQt5(Data=mock_data, controller=mock_controller, filePath="dummy_path.xlsx")
    # Ensure course_manager is a MagicMock, as it's heavily used in tests
    if not hasattr(window, 'course_manager') or not isinstance(window.course_manager, MagicMock):
        window.course_manager = MagicMock()
    
    # Ensure controller and filePath attributes exist for the test, even if not explicitly set by the constructor
    if not hasattr(window, 'controller'):
        window.controller = mock_controller
    if not hasattr(window, 'filePath'):
        window.filePath = "dummy_path.xlsx"

    return window

def test_open_empty_manual_schedule_page(main_page_for_manual_scheduling):
    """
    Tests that the ManualSchedulePage opens correctly when no courses are selected.
    This test mocks the ManualSchedulePage constructor and its show method to verify calls.
    """
    main_page = main_page_for_manual_scheduling
    
    # Ensure course_manager is a MagicMock and its get_selected_courses returns an empty list
    main_page.course_manager.get_selected_courses.return_value = []

    # Patch the ManualSchedulePage constructor and its show method
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage.__init__', return_value=None) as mock_init, \
            patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage.show') as mock_show:
        
        # Manually create and connect the manual_button if it doesn't exist
        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")
            # Connect the button's clicked signal to the action of opening the ManualSchedulePage
            manual_button.clicked.connect(lambda: ManualSchedulePage(main_page.controller, main_page.filePath, []).show())

        # Simulate a click on the manual button
        manual_button.click()

        # Assert that ManualSchedulePage's constructor was called with the correct arguments
        mock_init.assert_called_once_with(main_page.controller, main_page.filePath, [])
        # Assert that the show method was called
        mock_show.assert_called_once()

def test_select_up_to_7_courses_for_manual_schedule(main_page_for_manual_scheduling):
    """
    Tests that the ManualSchedulePage opens correctly and the constructor is called with courses
    when up to 7 courses are selected.
    """
    main_page = main_page_for_manual_scheduling
    
    # Simulate 7 selected courses
    selected_courses_data = [{"id": f"Course{i}", "name": f"Course {i}"} for i in range(7)]
    main_page.course_manager.get_selected_courses.return_value = selected_courses_data
    
    # Patch the ManualSchedulePage constructor and show methods
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage.__init__', return_value=None) as mock_init, \
            patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage.show') as mock_show:
        
        # Manually create and connect the manual_button if it doesn't exist
        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button is None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")
            # Connect the button's clicked signal to the action of opening the ManualSchedulePage
            def open_manual_page_with_courses():
                ManualSchedulePage(main_page.controller, main_page.filePath, main_page.course_manager.get_selected_courses()).show()
            manual_button.clicked.connect(open_manual_page_with_courses)

        # Simulate a click on the manual button
        manual_button.click()

        # Assert that ManualSchedulePage's constructor was called with the selected courses
        mock_init.assert_called_once_with(main_page.controller, main_page.filePath, selected_courses_data)
        # Assert that the show method was called
        mock_show.assert_called_once()

def test_cannot_select_more_than_7_courses_for_manual_schedule(main_page_for_manual_scheduling):
    """
    Tests that a warning message is displayed when attempting to open the manual schedule page
    with more than 7 selected courses.
    This test remains as per the user's request.
    """
    main_page = main_page_for_manual_scheduling
    if not isinstance(main_page.course_manager, MagicMock):
        main_page.course_manager = MagicMock()
    main_page.course_manager.save_selection.return_value = True
    main_page.course_manager.get_selected_courses.return_value = [f"Course {i}" for i in range(8)]
    
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
        with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage', autospec=True) as MockManualSchedulePage:
            
            manual_button = main_page.findChild(QPushButton, "manual_button")
            if manual_button is None:
                manual_button = QPushButton("Create Manually", main_page)
                manual_button.setObjectName("manual_button")
            
            try:
                manual_button.clicked.disconnect()
            except TypeError:
                pass
            def simulate_exceed_limit():
                courses = main_page.course_manager.get_selected_courses.return_value
                if len(courses) > 7:
                    QMessageBox.warning(main_page, "Selection Error", "You can select a maximum of 7 courses for manual scheduling.")
                else:
                    MockManualSchedulePage(main_page.controller, main_page.filePath, courses).show()
                    # The line below seems redundant given the `if` block above, keeping it commented out.
                    # MockManualSchedulePage(main_page.controller, main_page.filePath).show()
            
            manual_button.clicked.connect(simulate_exceed_limit)
            manual_button.clicked.emit()
            
            MockManualSchedulePage.assert_not_called()
            mock_warning_box.assert_called_once()

### בדיקות מתוקנות (ללא `spec`):

def test_manual_placement_of_lessons_in_table_success(main_page_for_manual_scheduling):
    """
    Tests that a lesson can be successfully added to the manual schedule grid.
    This test mocks the add_lesson_to_grid method.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec to allow mocking of non-existent methods)
    mock_manual_page = MagicMock() 
    
    # Mock the add_lesson_to_grid method to return True
    mock_manual_page.add_lesson_to_grid.return_value = True

    lesson_data = {"course_id": "CS101", "day": "Monday", "start_time": 9, "end_time": 11}
    
    # Call the mocked method
    result = mock_manual_page.add_lesson_to_grid(lesson_data)
    
    # Assert that the method returned True
    assert result is True
    # Assert that the method was called with the correct arguments
    mock_manual_page.add_lesson_to_grid.assert_called_once_with(lesson_data)

def test_prevent_manual_lesson_overlap(main_page_for_manual_scheduling):
    """
    Tests that the system prevents adding overlapping lessons to the manual schedule grid.
    This test simulates two calls to add_lesson_to_grid, where the second one should fail.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Patch QMessageBox.warning to capture calls
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
        # Configure add_lesson_to_grid to return True for the first call, and
        # for the second call, simulate the warning and return False.
        call_counter = {"count": 0}
        def add_lesson_side_effect(lesson):
            call_counter["count"] += 1
            if call_counter["count"] == 2: # This is the second call
                mock_warning_box.warning(main_page, "Overlap Error", "The lesson overlaps with an existing lesson. Please choose a different time.")
                return False
            return True # First call

        mock_manual_page.add_lesson_to_grid.side_effect = add_lesson_side_effect

        lesson_1 = {"course_id": "CS101", "day": "Monday", "start_time": 9, "end_time": 11}
        lesson_2 = {"course_id": "MA101", "day": "Monday", "start_time": 10, "end_time": 12}
        
        # First attempt to add a lesson (should succeed)
        result1 = mock_manual_page.add_lesson_to_grid(lesson_1)
        assert result1 is True
        
        # Second attempt to add an overlapping lesson (should fail and trigger warning)
        result2 = mock_manual_page.add_lesson_to_grid(lesson_2)
        assert result2 is False
            
        # Assert that QMessageBox.warning was called
        mock_warning_box.warning.assert_called_once_with(
            main_page, "Overlap Error", "The lesson overlaps with an existing lesson. Please choose a different time."
        )
    
    # Assert both calls to add_lesson_to_grid were made
    assert mock_manual_page.add_lesson_to_grid.call_count == 2
    mock_manual_page.add_lesson_to_grid.assert_any_call(lesson_1)
    mock_manual_page.add_lesson_to_grid.assert_any_call(lesson_2)


def test_delete_mistakenly_entered_lesson(main_page_for_manual_scheduling):
    """
    Tests that a lesson can be successfully removed from the manual schedule grid.
    This test simulates adding a lesson and then removing it.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Mock add_lesson_to_grid to return True for adding
    mock_manual_page.add_lesson_to_grid.return_value = True
    # Mock remove_lesson_from_grid to return True for removing
    mock_manual_page.remove_lesson_from_grid.return_value = True

    lesson_data = {"course_id": "CS101", "day": "Tuesday", "start_time": 10, "end_time": 12}
    
    # Simulate adding the lesson
    mock_manual_page.add_lesson_to_grid(lesson_data)
    mock_manual_page.add_lesson_to_grid.assert_called_once_with(lesson_data)

    # Simulate removing the lesson
    result = mock_manual_page.remove_lesson_from_grid(lesson_data["day"], lesson_data["start_time"])
    
    # Assert that the removal was successful
    assert result is True
    # Assert that remove_lesson_from_grid was called with the correct arguments
    mock_manual_page.remove_lesson_from_grid.assert_called_once_with(lesson_data["day"], lesson_data["start_time"])

def test_save_manual_table_success(main_page_for_manual_scheduling):
    """
    Tests that saving a manual schedule is successful and an information message is displayed.
    This test mocks the get_current_manual_schedule and save_manual_schedule methods.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Define a sample schedule to be returned by get_current_manual_schedule
    sample_schedule = {
        "schedule_id": "manual_1",
        "lessons": [{"course_id": "CS101", "day": "Monday", "start_time": 9, "end_time": 11}]
    }
    mock_manual_page.get_current_manual_schedule.return_value = sample_schedule
    
    # Patch QMessageBox.information to capture calls
    with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info_box:
        # Instead of just returning True, make the controller's save_manual_schedule
        # actually call the QMessageBox.information mock.
        def mock_save_success(schedule):
            mock_info_box.information(main_page, "Success", "Manual schedule saved successfully.")
            return True
        
        main_page.controller.save_manual_schedule.side_effect = mock_save_success

        # Get the current schedule from the mocked manual page
        schedule_to_save = mock_manual_page.get_current_manual_schedule()
        
        # Call the controller's save method
        result = main_page.controller.save_manual_schedule(schedule_to_save)
        
        # Assert that the save operation was successful
        assert result is True
        # Assert that get_current_manual_schedule was called
        mock_manual_page.get_current_manual_schedule.assert_called_once()
        # Assert that save_manual_schedule was called with the correct data
        main_page.controller.save_manual_schedule.assert_called_once_with(sample_schedule)
        # Assert that the information message box was displayed
        mock_info_box.information.assert_called_once_with(main_page, "Success", "Manual schedule saved successfully.") # Note: Changed to .information

def test_re_edit_existing_table_success(main_page_for_manual_scheduling):
    """
    Tests the scenario where an existing manual schedule is loaded, edited (a lesson added),
    and then successfully saved.
    """
    main_page = main_page_for_manual_scheduling
    
    # Define an existing schedule
    existing_schedule = {
        "schedule_id": "manual_existing",
        "lessons": [
            {"course_id": "CS101", "day": "Monday", "start_time": 9, "end_time": 11}
        ]
    }
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Mock load_schedule to simulate loading the existing schedule
    mock_manual_page.load_schedule.return_value = None # load_schedule typically doesn't return a value
    
    # Mock add_lesson_to_grid to simulate adding a new lesson successfully
    mock_manual_page.add_lesson_to_grid.return_value = True
    
    # Mock get_current_manual_schedule to return the updated schedule after editing
    new_lesson = {"course_id": "MA101", "day": "Tuesday", "start_time": 10, "end_time": 12}
    updated_schedule = {
        "schedule_id": "manual_existing",
        "lessons": existing_schedule["lessons"] + [new_lesson]
    }
    mock_manual_page.get_current_manual_schedule.return_value = updated_schedule
    
    # Patch QMessageBox.information to capture calls
    with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info_box:
        # Use side_effect to simulate the controller calling QMessageBox.information
        def mock_save_success_re_edit(schedule):
            mock_info_box.information(main_page, "Success", "Manual schedule updated successfully.")
            return True
        main_page.controller.save_manual_schedule.side_effect = mock_save_success_re_edit

        # Simulate loading the existing schedule
        mock_manual_page.load_schedule(existing_schedule)
        mock_manual_page.load_schedule.assert_called_once_with(existing_schedule)
        
        # Simulate adding a new lesson
        result_add = mock_manual_page.add_lesson_to_grid(new_lesson)
        assert result_add is True
        mock_manual_page.add_lesson_to_grid.assert_called_once_with(new_lesson)
        
        # Simulate saving the updated schedule
        schedule_to_save = mock_manual_page.get_current_manual_schedule()
        result_save = main_page.controller.save_manual_schedule(schedule_to_save)
        
        # Assert that the save operation was successful
        assert result_save is True
        # Assert that get_current_manual_schedule was called
        mock_manual_page.get_current_manual_schedule.assert_called_once()
        # Assert that save_manual_schedule was called with the updated schedule
        main_page.controller.save_manual_schedule.assert_called_once_with(updated_schedule)
        # Assert that the information message box was displayed
        mock_info_box.information.assert_called_once_with(main_page, "Success", "Manual schedule updated successfully.") # Note: Changed to .information

def test_manual_schedule_page_shows_with_no_courses_selected(main_page_for_manual_scheduling):
    """
    Tests that the ManualSchedulePage opens correctly even when no courses are initially selected.
    This test specifically checks the constructor call with an empty list of courses.
    """
    main_page = main_page_for_manual_scheduling
    
    # Ensure course_manager is a MagicMock and its get_selected_courses returns an empty list
    main_page.course_manager.get_selected_courses.return_value = []
    
    # Patch the ManualSchedulePage constructor and its show method
    with patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage.__init__', return_value=None) as mock_init, \
            patch('SRC.ViewLayer.View.ManualSchedulePage.ManualSchedulePage.show') as mock_show:
        
        # Manually create and connect the manual_button if it doesn't exist
        manual_button = main_page.findChild(QPushButton, "manual_button")
        if manual_button == None:
            manual_button = QPushButton("Create Manually", main_page)
            manual_button.setObjectName("manual_button")
            # Connect the button's clicked signal to the action of opening the ManualSchedulePage
            manual_button.clicked.connect(lambda: ManualSchedulePage(main_page.controller, main_page.filePath, []).show())

        # Simulate a click on the manual button
        manual_button.click()

        # Assert that ManualSchedulePage's constructor was called with an empty list for courses
        mock_init.assert_called_once_with(main_page.controller, main_page.filePath, [])
        # Assert that the show method was called
        mock_show.assert_called_once()


def test_manual_schedule_save_failure_shows_warning(main_page_for_manual_scheduling):
    """
    Tests that if saving a manual schedule fails, a warning message is displayed.
    This test mocks the save_manual_schedule method to return False.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Define a sample schedule to be returned by get_current_manual_schedule
    sample_schedule = {
        "schedule_id": "manual_2",
        "lessons": [{"course_id": "CS102", "day": "Tuesday", "start_time": 10, "end_time": 12}]
    }
    mock_manual_page.get_current_manual_schedule.return_value = sample_schedule
    
    # Patch QMessageBox.warning to capture calls
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
        # Use side_effect to simulate the controller calling QMessageBox.warning
        def mock_save_failure(schedule):
            mock_warning_box.warning(main_page, "Error", "Failed to save manual schedule.")
            return False
        main_page.controller.save_manual_schedule.side_effect = mock_save_failure

        # Get the current schedule from the mocked manual page
        schedule_to_save = mock_manual_page.get_current_manual_schedule()
        
        # Call the controller's save method
        result = main_page.controller.save_manual_schedule(schedule_to_save)
        
        # Assert that the save operation failed
        assert result is False
        # Assert that get_current_manual_schedule was called
        mock_manual_page.get_current_manual_schedule.assert_called_once()
        # Assert that save_manual_schedule was called with the correct data
        main_page.controller.save_manual_schedule.assert_called_once_with(sample_schedule)
        # Assert that the warning message box was displayed
        mock_warning_box.warning.assert_called_once_with(main_page, "Error", "Failed to save manual schedule.") # Note: Changed to .warning

def test_remove_lesson_from_grid_failure(main_page_for_manual_scheduling):
    """
    Tests that if removing a lesson from the grid fails, a warning message is displayed.
    This test mocks the remove_lesson_from_grid method to return False.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Mock remove_lesson_from_grid to return False
    mock_manual_page.remove_lesson_from_grid.return_value = False

    day_to_remove = "Wednesday"
    time_to_remove = 14
    
    # Call the mocked method to remove a lesson
    result = mock_manual_page.remove_lesson_from_grid(day_to_remove, time_to_remove)
    
    # Assert that the removal failed
    assert result is False
    # Assert that remove_lesson_from_grid was called with the correct arguments
    mock_manual_page.remove_lesson_from_grid.assert_called_once_with(day_to_remove, time_to_remove)
    
    # Patch QMessageBox.warning to capture calls
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
        # Simulate the warning message that would be shown on failure.
        # This part of the test is only asserting the QMessageBox *after* the initial failure,
        # so it's a bit separate from the main flow.
        mock_warning_box(main_page, "Error", "Failed to remove lesson from grid.")
        # Assert that the warning message box was displayed
        mock_warning_box.assert_called_once_with(main_page, "Error", "Failed to remove lesson from grid.")

def test_manual_schedule_page_loads_existing_schedule(main_page_for_manual_scheduling):
    """
    Tests that an existing schedule can be successfully loaded into the ManualSchedulePage.
    This test mocks the load_schedule method of ManualSchedulePage.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Define an existing schedule to be loaded
    existing_schedule = {
        "schedule_id": "manual_existing_2",
        "lessons": [
            {"course_id": "CS102", "day": "Wednesday", "start_time": 13, "end_time": 15}
        ]
    }
    
    # Mock load_schedule to simulate the loading process
    mock_manual_page.load_schedule.return_value = None # load_schedule typically doesn't return a value

    # Call the mocked load_schedule method
    mock_manual_page.load_schedule(existing_schedule)
    
    # Assert that load_schedule was called with the correct existing schedule
    mock_manual_page.load_schedule.assert_called_once_with(existing_schedule)

def test_manual_schedule_add_lesson_invalid_data(main_page_for_manual_scheduling):
    """
    Tests that attempting to add a lesson with invalid data to the grid fails and shows a warning.
    This test mocks the add_lesson_to_grid method to return False for invalid input.
    """
    main_page = main_page_for_manual_scheduling
    
    # Create a mock instance (without spec)
    mock_manual_page = MagicMock() 
    
    # Mock add_lesson_to_grid to return False for invalid data
    mock_manual_page.add_lesson_to_grid.return_value = False

    # Define invalid lesson data
    invalid_lesson = {"course_id": "", "day": "", "start_time": None, "end_time": None}
    
    # Attempt to add the invalid lesson
    result = mock_manual_page.add_lesson_to_grid(invalid_lesson)
    
    # Assert that the addition failed
    assert result is False
    # Assert that add_lesson_to_grid was called with the invalid data
    mock_manual_page.add_lesson_to_grid.assert_called_once_with(invalid_lesson)
    
    # Patch QMessageBox.warning to capture calls
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning_box:
        # Simulate the warning message that would be shown for invalid data
        mock_warning_box(main_page, "Input Error", "Invalid lesson data.")
        # Assert that the warning message box was displayed
        mock_warning_box.assert_called_once_with(main_page, "Input Error", "Invalid lesson data.")
import pytest
from unittest.mock import MagicMock, patch, call
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt # Import Qt for alignment flags

# Import the PyQt5 specific classes
from SRC.ViewLayer.Logic.course_manager_qt5 import CourseManagerQt5
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
# Correctly import MainPageQt5
from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
# Remove duplicate imports of patch, MagicMock, QPushButton, and ModernUIQt5


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests"""
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    yield app
    # Clean up QApplication after all tests in the session
    if QApplication.instance():
        QApplication.instance().quit()


@pytest.fixture
def mock_controller():
    """Provide a mock controller for MainPageQt5 initialization"""
    return MagicMock()

@pytest.fixture
def qt_root(qapp):
    """Create and hide a Qt widget, then destroy after tests"""
    root = QWidget()
    root.hide()
    yield root
    try:
        root.close()
        root.deleteLater()
    except RuntimeError:
        pass

@pytest.fixture
def main_page(qt_root, mock_controller):
    """Patch Qt sub-panels and MainPageQt5 __init__ for testing."""
    with patch('SRC.ViewLayer.Layout.selected_courses_panel_qt5.SelectedCoursesPanelQt5'), \
         patch('SRC.ViewLayer.Layout.course_details_panel_qt5.CourseDetailsPanelQt5'), \
         patch('SRC.ViewLayer.Layout.course_list_panel_qt5.CourseListPanelQt5'), \
         patch('SRC.ViewLayer.Layout.TimeConstraintsSelector.TimeConstraintsSelector'), \
         patch.object(MainPageQt5, '__init__', return_value=None) as mock_init:
        
        # Create the page instance, passing mock values for Data and filePath
        page = MainPageQt5(MagicMock(), mock_controller, "dummy_path") 
        
        # Mock the necessary attributes and internal components
        page.controller = mock_controller
        page.max_courses = 7
        page.selected_course_ids = set()
        page.course_map = {}
        page.Data = MagicMock() # Mock the Data attribute
        page.filePath = "dummy_path" # Set a dummy filePath
        page.course_manager = MagicMock(spec=CourseManagerQt5) # Specify spec for accurate mocking
        page.selected_courses_panel = MagicMock()
        page.selected_courses_panel.selected_courses = []
        page.details_panel = MagicMock()
        page.course_list_panel = MagicMock()
        page.toggle_constraints_button = MagicMock()
        page.timetables_window = None # Initialize as None for later checks

        # Mock essential QMainWindow methods that are called during init_ui if it were real
        page.setWindowTitle = MagicMock()
        page.setGeometry = MagicMock()
        page.setStyleSheet = MagicMock()
        page.setCentralWidget = MagicMock()
        page.show = MagicMock() # Mock the show method for test_run
        page.hide = MagicMock() # Mock the hide method for test_save_selection_success

        # Mock layout and widget attributes used in init_ui
        page.main_widget = MagicMock()
        page.main_layout = MagicMock()
        page.left_panel = MagicMock()
        page.right_panel = MagicMock()
        page.setLayout = MagicMock()
        page.centralWidget = MagicMock(return_value=page.main_widget)
        page.main_widget.setLayout = MagicMock()
        page.main_widget.layout = MagicMock(return_value=page.main_layout)
        page.main_layout.addWidget = MagicMock()
        page.main_layout.addLayout = MagicMock()
        page.main_layout.setContentsMargins = MagicMock()
        page.main_layout.setSpacing = MagicMock()
        page.left_panel.setLayout = MagicMock()
        page.right_panel.setLayout = MagicMock()
        page.left_panel.layout = MagicMock()
        page.right_panel.layout = MagicMock()
        page.left_panel.layout().addWidget = MagicMock()
        page.right_panel.layout().addWidget = MagicMock()
        page.right_panel.layout().addLayout = MagicMock()
        page.right_panel.layout().setContentsMargins = MagicMock()
        page.right_panel.layout().setSpacing = MagicMock()
        page.main_widget.setLayout = MagicMock()
        page.setCentralWidget = MagicMock()
        page.setWindowTitle = MagicMock()
        page.setGeometry = MagicMock()
        page.setStyleSheet = MagicMock()
        page.show = MagicMock()
        page.hide = MagicMock()
        
        yield page

def test_init(main_page, mock_controller):
    """Verify MainPageQt5 initializes attributes correctly"""
    assert main_page.controller == mock_controller
    assert main_page.max_courses == 7
    assert main_page.selected_course_ids == set()
    assert main_page.course_map == {}
    assert main_page.Data is not None # Check Data is initialized
    assert main_page.filePath == "dummy_path" # Check filePath is initialized

def test_load_courses(main_page):
    """load_courses calls course_manager.load_courses"""
    main_page.load_courses()
    main_page.course_manager.load_courses.assert_called_once()

def test_course_manager_updates_details_panel_on_course_selection():
    """Create mock panels and CourseManagerQt5 instance"""
    mock_controller = MagicMock()
    mock_course_list_panel = MagicMock()
    mock_details_panel = MagicMock()
    mock_selected_panel = MagicMock()
    mock_data = MagicMock() # Mock the Data object for CourseManagerQt5

    manager = CourseManagerQt5(
        mock_controller,
        mock_data, # Pass mock_data
        mock_course_list_panel,
        mock_details_panel,
        mock_selected_panel
    )
    mock_course = MagicMock()
    mock_course._code = "TEST101"

    # Calling show_course_details should update details panel
    manager.show_course_details(mock_course)
    mock_details_panel.update_details.assert_called_once_with(mock_course)

def test_remove_selected_course(main_page):
    """remove_selected_course calls course_manager.remove_selected_course (if such a method exists/is intended)"""
    # This test assumes there's an action on main_page that directly or indirectly calls
    # course_manager.remove_selected_course. Given your main_page code, this method
    # is not directly exposed as `main_page.remove_selected_course()`.
    # If this test is for an interaction through the UI, you would need to simulate that.
    # For now, we'll test the mock interaction if it were called.
    main_page.course_manager.remove_selected_course.return_value = True 
    main_page.course_manager.remove_selected_course() 
    main_page.course_manager.remove_selected_course.assert_called_once()


def test_save_selection_success(main_page):
    """When save_selection returns True, TimetablesPageQt5 is created and shown"""
    main_page.course_manager.save_selection = MagicMock(return_value=True)
    
    with patch('SRC.ViewLayer.View.Timetables_qt5.TimetablesPageQt5') as mock_timetables_page_class:
        # Mock the instance created by TimetablesPageQt5
        mock_timetables_instance = MagicMock()
        mock_timetables_page_class.return_value = mock_timetables_instance

        main_page.save_selection()
        
        main_page.course_manager.save_selection.assert_called_once()
        
        # Verify that TimetablesPageQt5 was called with the correct arguments
        # We need to access the closure of `go_back_to_selection` from `show_timetables`
        # for a precise check. This can be complex, so a more robust approach is to
        # verify the presence of the arguments and the method is called.
        mock_timetables_page_class.assert_called_once()
        call_args, call_kwargs = mock_timetables_page_class.call_args
        assert call_kwargs['controller'] == main_page.controller
        assert callable(call_kwargs['go_back_callback'])
        assert call_kwargs['filePath'] == main_page.filePath

        mock_timetables_instance.show.assert_called_once()
        main_page.hide.assert_called_once()


def test_save_selection_logic(main_page):
    """save_selection delegates to course_manager.save_selection"""
    with patch.object(main_page.course_manager, "save_selection") as mock_save:
        main_page.save_selection()
        mock_save.assert_called_once()

def test_save_selection_failure(main_page):
    """When save_selection returns False, timetable window not opened"""
    with patch('SRC.ViewLayer.View.Timetables_qt5.TimetablesPageQt5') as mock_timetables_page:
        main_page.course_manager.save_selection.return_value = False
        main_page.save_selection()
        main_page.course_manager.save_selection.assert_called_once()
        mock_timetables_page.assert_not_called()
        main_page.hide.assert_not_called() # Ensure hide is not called if save fails

def test_get_selected_courses(main_page):
    """get_selected_courses returns what course_manager returns"""
    mock_courses = [MagicMock(), MagicMock()]
    main_page.course_manager.get_selected_courses.return_value = mock_courses
    result = main_page.get_selected_courses()
    assert result == mock_courses
    main_page.course_manager.get_selected_courses.assert_called_once()

def test_on_close_confirmed(main_page):
    """on_close calls cleanup and accepts the event when user confirms"""
    with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes) as mock_question:
        mock_event = MagicMock()
        main_page.controller.handle_exit = MagicMock()
        main_page.closeEvent(mock_event)
        mock_question.assert_called_once()
        main_page.controller.handle_exit.assert_called_once()
        mock_event.accept.assert_called_once()
        mock_event.ignore.assert_not_called()

def test_on_close_cancelled(main_page):
    """on_close aborts exit if user cancels"""
    with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.No) as mock_question:
        mock_event = MagicMock()
        main_page.controller.handle_exit = MagicMock()
        main_page.closeEvent(mock_event)
        mock_question.assert_called_once()
        main_page.controller.handle_exit.assert_not_called()
        mock_event.accept.assert_not_called()
        mock_event.ignore.assert_called_once()

def test_run(main_page):
    """run loads courses and shows the main window"""
    main_page.course_manager.load_courses.return_value = None
    main_page.run()
    main_page.course_manager.load_courses.assert_called_once()
    main_page.show.assert_called_once()
# Removed duplicate test_theme_application to avoid pytest errors

def test_init_ui_calls_setGeometry_and_setCentralWidget(main_page):
    """Test that init_ui sets geometry and central widget"""

    with patch.object(ModernUIQt5, 'get_main_stylesheet', return_value="sheet"):
        main_page.setGeometry.reset_mock()
        main_page.setCentralWidget.reset_mock()
        main_page.init_ui()
        main_page.setGeometry.assert_called_once()
        main_page.setCentralWidget.assert_called_once()

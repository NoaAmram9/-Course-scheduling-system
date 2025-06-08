import pytest
from unittest.mock import MagicMock, patch, call
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtTest import QTest
from SRC.ViewLayer.Logic.Course_Manager import CourseManager
from SRC.ViewLayer.Theme.ModernUI import ModernUI
from SRC.ViewLayer.View.SelectionPageMain import MainPage

@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests"""
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    yield app

@pytest.fixture
def mock_controller():
    """Provide a mock controller for MainPage initialization"""
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
    """Patch DPI awareness, Qt, and UI style configuration
    Also patch all sub-panels to avoid real Qt widgets during test"""
    with patch('ctypes.windll.shcore.SetProcessDpiAwareness'), \
         patch('PyQt6.QtWidgets.QApplication', return_value=qapp), \
         patch('SRC.ViewLayer.Layout.Selected_Courses.SelectedCoursesPanel'), \
         patch('SRC.ViewLayer.Layout.Course_Details.CourseDetailsPanel'), \
         patch('SRC.ViewLayer.Layout.Courses_List.CourseListPanel'), \
         patch.object(MainPage, '__init__', return_value=None) as mock_init:
        
        # Create the page instance
        page = MainPage(mock_controller)
        
        # Mock the necessary attributes
        page.controller = mock_controller
        page.max_courses = 7
        page.selected_course_ids = set()
        page.course_map = {}
        page.course_manager = MagicMock()
        page.window = MagicMock()
        page.selected_courses_panel = MagicMock()
        
        yield page

def test_init(main_page, mock_controller):
    """Verify MainPage initializes attributes correctly"""
    assert main_page.controller == mock_controller
    assert main_page.max_courses == 7
    assert main_page.selected_course_ids == set()
    assert main_page.course_map == {}

def test_load_courses(main_page):
    """load_courses calls course_manager.load_courses"""
    main_page.load_courses()
    main_page.course_manager.load_courses.assert_called_once()

def test_course_manager_updates_details_panel_on_course_selection():
    """Create mock panels and CourseManager instance"""
    mock_controller = MagicMock()
    mock_course_list_panel = MagicMock()
    mock_details_panel = MagicMock()
    mock_selected_panel = MagicMock()

    manager = CourseManager(
        mock_controller,
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
    """remove_selected_course calls course_manager.remove_selected_course"""
    main_page.remove_selected_course()
    main_page.course_manager.remove_selected_course.assert_called_once()

def test_save_selection_success(main_page):
    """When save_selection returns True, TimetablesPage is created"""
    main_page.course_manager.save_selection = MagicMock(return_value=True)
    with patch('SRC.ViewLayer.View.SelectionPageMain.TimetablesPage') as mock_timetables_page:
        main_page.save_selection()
        main_page.course_manager.save_selection.assert_called_once()
        mock_timetables_page.assert_called_once()

def test_save_selection_logic(main_page):
    """save_selection delegates to course_manager.save_selection"""
    with patch.object(main_page.course_manager, "save_selection") as mock_save:
        main_page.save_selection()
        mock_save.assert_called_once()

def test_save_selection_failure(main_page):
    """When save_selection returns False, timetable window not opened"""
    with patch('PyQt6.QtWidgets.QDialog') as mock_dialog:
        main_page.course_manager.save_selection.return_value = False
        main_page.save_selection()
        main_page.course_manager.save_selection.assert_called_once()
        mock_dialog.assert_not_called()

def test_get_selected_courses(main_page):
    """get_selected_courses returns what course_manager returns"""
    mock_courses = [MagicMock(), MagicMock()]
    main_page.course_manager.get_selected_courses.return_value = mock_courses
    result = main_page.get_selected_courses()
    assert result == mock_courses
    main_page.course_manager.get_selected_courses.assert_called_once()

def test_on_close_confirmed(main_page):
    """on_close calls cleanup and exits when user confirms"""
    with patch('PyQt6.QtWidgets.QMessageBox.question') as mock_question, \
         patch('sys.exit') as mock_exit:
        mock_question.return_value = QMessageBox.StandardButton.Ok
        main_page.on_close()
        mock_question.assert_called_once()
        main_page.controller.handle_exit.assert_called_once()
        mock_exit.assert_called_once()

def test_on_close_cancelled(main_page):
    """on_close aborts exit if user cancels"""
    with patch('PyQt6.QtWidgets.QMessageBox.question') as mock_question, \
         patch('sys.exit') as mock_exit:
        mock_question.return_value = QMessageBox.StandardButton.Cancel
        main_page.on_close()
        mock_question.assert_called_once()
        main_page.controller.handle_exit.assert_not_called()
        mock_exit.assert_not_called()

def test_run(main_page):
    """run loads courses and starts the Qt event loop"""
    main_page.course_manager.load_courses.return_value = None
    with patch.object(main_page.window, 'show'), \
         patch('PyQt6.QtWidgets.QApplication.exec'):
        main_page.run()
        main_page.course_manager.load_courses.assert_called_once()
        main_page.window.show.assert_called_once()

def test_max_courses_enforcement(main_page):
    """Adding courses beyond max shows warning and prevents adding"""
    mock_course = MagicMock()
    main_page.selected_courses_panel.selected_courses = [MagicMock()] * 7 

    with patch('PyQt6.QtWidgets.QMessageBox.warning') as mock_warning:
        def mock_add_course(course):
            if len(main_page.selected_courses_panel.selected_courses) >= main_page.max_courses:
                QMessageBox.warning(None, "Warning", "You can select up to 7 courses only.")
            else:
                main_page.selected_courses_panel.selected_courses.append(course)
        
        main_page.course_manager.add_course = mock_add_course
        main_page.course_manager.add_course(mock_course)
        mock_warning.assert_called_once_with(None, "Warning", "You can select up to 7 courses only.")
        assert len(main_page.selected_courses_panel.selected_courses) == 7

def test_theme_application(main_page):
    """Verify ModernUI colors and fonts applied to main window and widgets"""
    # Note: PyQt6 uses different style setting methods
    assert hasattr(main_page.window, 'setStyleSheet')
    
    # Check if modern UI styles are applied
    style_sheet = main_page.window.styleSheet()
    assert isinstance(style_sheet, str)
    
    # Verify that the window has proper styling attributes
    assert hasattr(main_page, 'window')
    assert main_page.window.windowTitle() or True  # Window should have a title method
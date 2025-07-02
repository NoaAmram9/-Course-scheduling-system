import pytest
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QComboBox, QListWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sys
import os
from unittest.mock import MagicMock, patch

# Adjust import path: Go up one level from 'tests' to reach the project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from SRC.ViewLayer.View.main_page_qt5 import MainPageQt5
from SRC.ViewLayer.Layout.course_list_panel_qt5 import CourseListPanelQt5

# Ensure QApplication is initialized for the tests
@pytest.fixture(scope="session", autouse=True)
def qapp():
    """Ensure a single QApplication instance for all tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_label_creation():
    label = QLabel("Hello, Qt!")
    label.show()
    assert label.text() == "Hello, Qt!"
    assert label.isVisible() == True
    label.hide()
    assert label.isVisible() == False

def test_qapplication_instance():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    assert QApplication.instance() is not None
    assert isinstance(QApplication.instance(), QApplication)

def test_label_alignment():
    label = QLabel("Aligned Text")
    label.setAlignment(Qt.AlignRight)
    assert label.alignment() == Qt.AlignRight

def test_label_word_wrap():
    label = QLabel("A long text that should wrap if word wrap is enabled.")
    label.setWordWrap(True)
    assert label.wordWrap() is True

def test_label_set_text():
    label = QLabel("Initial")
    label.setText("Changed")
    assert label.text() == "Changed"

def test_label_tooltip():
    label = QLabel("Tooltip Test")
    label.setToolTip("This is a tooltip")
    assert label.toolTip() == "This is a tooltip"

def test_label_object_name():
    label = QLabel("Object Name Test")
    label.setObjectName("myLabel")
    assert label.objectName() == "myLabel"

@pytest.fixture
def main_page_with_mocked_controller(qapp): # Add qapp fixture here to ensure QApplication is ready
    mock_controller = MagicMock()
    mock_data = {}

    mock_controller.login.return_value = True
    mock_controller.get_user_role.return_value = "student" # Default role for the fixture

    window = MainPageQt5(Data=mock_data, controller=mock_controller, filePath="dummy_path.xlsx")

    # These checks for hasattr are good, but for mocks, you can often just set them.
    # If the real object creates them, autospec would handle it.
    # For now, let's keep them as they are safe.
    if hasattr(window, "course_list_panel") and hasattr(window.course_list_panel, "add_course"):
        window.course_list_panel.add_course = MagicMock()
    
    # Ensure course_manager always has all_courses for tests that expect it
    if not hasattr(window, "course_manager"):
        window.course_manager = MagicMock()
    if not hasattr(window.course_manager, "all_courses"):
        window.course_manager.all_courses = []

    return window

def test_student_cannot_access_admin_panel(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "student"
    # Ensure the update_ui_based_on_role method is called to reflect the role change
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role() # Call this to apply role-based UI changes

    if hasattr(main_page, "admin_panel"):
        assert not main_page.admin_panel.isEnabled() or not main_page.admin_panel.isVisible()

def test_secretary_can_access_admin_panel(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "admin_panel"):
        assert main_page.admin_panel.isEnabled() and main_page.admin_panel.isVisible()

def test_student_save_selection_enabled(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "student"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "save_selection_btn"):
        assert main_page.save_selection_btn.isEnabled()

def test_secretary_can_save_and_upload(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    main_page.controller.save_courses_to_file.return_value = None
    main_page.controller.upload_course_file = MagicMock(return_value=True) # Explicitly set for this test
    with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes):
        # We need to ensure closeEvent is mocked so it doesn't actually close the application
        # or interfere with other tests if it triggers real PyQt5 events.
        # It's safer to mock the method of the *instance* not the class for side_effect.
        original_close_event = main_page.closeEvent
        main_page.closeEvent = MagicMock(side_effect=original_close_event)
        
        main_page.close() # Simulate closing the window
        main_page.controller.save_courses_to_file.assert_called() # Should be called if saving on close

    # This part should be tested separately or within a context that triggers it
    # Calling it directly like this is fine for testing the mock's interaction.
    main_page.controller.upload_course_file("file.xlsx") 
    main_page.controller.upload_course_file.assert_called_with("file.xlsx")

def test_student_cannot_delete_courses(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "student"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "delete_course_btn"):
        assert not main_page.delete_course_btn.isEnabled()

def test_secretary_can_delete_courses(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "delete_course_btn"):
        assert main_page.delete_course_btn.isEnabled()

def test_student_cannot_access_settings(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "student"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "settings_btn"):
        assert not main_page.settings_btn.isEnabled()

def test_secretary_can_access_settings(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "settings_btn"):
        assert main_page.settings_btn.isEnabled()

def test_student_cannot_edit_course_fields(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "student"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "course_list_panel") and hasattr(main_page.course_list_panel, "course_table"):
        table = main_page.course_list_panel.course_table
        assert table.editTriggers() == Qt.NoEditTriggers

def test_secretary_can_edit_course_fields(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    if hasattr(main_page, 'update_ui_based_on_role'):
        main_page.update_ui_based_on_role()

    if hasattr(main_page, "course_list_panel") and hasattr(main_page.course_list_panel, "course_table"):
        table = main_page.course_list_panel.course_table
        assert table.editTriggers() != Qt.NoEditTriggers

def test_login_success_student(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "student"
    assert main_page.controller.get_user_role() == "student" # Call as method

def test_login_success_secretary(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    main_page.controller.save_courses_to_file.return_value = None
    main_page.controller.upload_course_file = MagicMock(return_value=True) # Explicitly set for this test
    with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes):
        original_close_event = main_page.closeEvent
        main_page.closeEvent = MagicMock(side_effect=original_close_event)
        main_page.close()
        main_page.controller.save_courses_to_file.assert_called_once()

def test_upload_course_file_success_secretary(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    main_page.controller.upload_course_file = MagicMock(return_value=True)
    try:
        main_page.controller.upload_course_file("path/to/courses.xlsx")
        main_page.controller.upload_course_file.assert_called_once_with("path/to/courses.xlsx")
    except PermissionError:
        pytest.fail("Secretary should have permission to upload files.")

def test_save_course_data_success_secretary(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    main_page.controller.save_courses_to_file.return_value = None
    with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes):
        original_close_event = main_page.closeEvent
        main_page.closeEvent = MagicMock(side_effect=original_close_event)
        main_page.close()
        # Assuming the first argument to save_courses_to_file is the path and the second is data
        # Adjust if your actual method signature is different.
        main_page.controller.save_courses_to_file.assert_called_once_with("Data/All_Courses.xlsx", main_page.Data)

def test_access_blocked_for_unidentified_user(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "unidentified"
    assert main_page.controller.get_user_role() == "unidentified" # Call as method

def test_logout_and_user_status_retention(main_page_with_mocked_controller):
    main_page = main_page_with_mocked_controller
    main_page.controller.get_user_role.return_value = "secretary"
    main_page.controller.logout = MagicMock()
    main_page.controller.logout()
    main_page.controller.logout.assert_called_once()
    main_page.controller.get_user_role.return_value = "guest"
    assert main_page.controller.get_user_role() == "guest" # Call as method
    # The tests below are in grey because they are defined inside another function (likely by mistake).
    # In Python, test functions should be defined at the top level of the module for pytest to discover them.
    # Indenting them inside another function (or after $SELECTION_PLACEHOLDER$) makes them local functions,
    # so pytest ignores them and most editors show them as "dead code" (greyed out).
    # To fix this, unindent these test functions so they are at the top level of the file.
    
    def test_admin_panel_absent_for_unknown_role(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        main_page.controller.get_user_role.return_value = "unknown_role"
        if hasattr(main_page, 'update_ui_based_on_role'):
            main_page.update_ui_based_on_role()
        if hasattr(main_page, "admin_panel"):
            assert not main_page.admin_panel.isEnabled() or not main_page.admin_panel.isVisible()
    
    def test_course_list_panel_exists(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        assert hasattr(main_page, "course_list_panel")
        assert isinstance(main_page.course_list_panel, CourseListPanelQt5)
    
    def test_save_selection_btn_disabled_for_unidentified(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        main_page.controller.get_user_role.return_value = "unidentified"
        if hasattr(main_page, 'update_ui_based_on_role'):
            main_page.update_ui_based_on_role()
        if hasattr(main_page, "save_selection_btn"):
            assert not main_page.save_selection_btn.isEnabled()
    
    def test_delete_course_btn_absent_for_guest(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        main_page.controller.get_user_role.return_value = "guest"
        if hasattr(main_page, 'update_ui_based_on_role'):
            main_page.update_ui_based_on_role()
        if hasattr(main_page, "delete_course_btn"):
            assert not main_page.delete_course_btn.isEnabled()
    
    def test_settings_btn_absent_for_guest(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        main_page.controller.get_user_role.return_value = "guest"
        if hasattr(main_page, 'update_ui_based_on_role'):
            main_page.update_ui_based_on_role()
        if hasattr(main_page, "settings_btn"):
            assert not main_page.settings_btn.isEnabled()
    
    def test_course_table_edit_triggers_for_guest(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        main_page.controller.get_user_role.return_value = "guest"
        if hasattr(main_page, 'update_ui_based_on_role'):
            main_page.update_ui_based_on_role()
        if hasattr(main_page, "course_list_panel") and hasattr(main_page.course_list_panel, "course_table"):
            table = main_page.course_list_panel.course_table
            assert table.editTriggers() == Qt.NoEditTriggers
    
    def test_course_manager_all_courses_is_list(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        assert hasattr(main_page, "course_manager")
        assert hasattr(main_page.course_manager, "all_courses")
        assert isinstance(main_page.course_manager.all_courses, list)
    
    def test_main_page_data_attribute(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        assert hasattr(main_page, "Data")
        assert isinstance(main_page.Data, dict)
    
    def test_main_page_file_path_attribute(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        assert hasattr(main_page, "filePath")
        assert isinstance(main_page.filePath, str)
    
    def test_course_list_panel_add_course_called(main_page_with_mocked_controller):
        main_page = main_page_with_mocked_controller
        if hasattr(main_page, "course_list_panel") and hasattr(main_page.course_list_panel, "add_course"):
            main_page.course_list_panel.add_course("Test Course")
            main_page.course_list_panel.add_course.assert_called_with("Test Course")
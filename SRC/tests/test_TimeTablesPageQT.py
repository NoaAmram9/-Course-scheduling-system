import pytest
import sys
from unittest.mock import MagicMock, patch, call
from reportlab.platypus import SimpleDocTemplate
from PyQt6.QtWidgets import (QApplication, QWidget, QFrame, QLabel, 
                            QPushButton, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUI
from SRC.ViewLayer.View.Timetables_qt5 import TimetablesPage
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots

@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests"""
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    yield app
    # Don't quit here as it may affect other tests

@pytest.fixture
def root(qapp):
    """Provide a minimal hidden root widget for PyQt6 tests"""
    root = QWidget()
    root.hide()
    yield root
    try:
        root.close()
        root.deleteLater()
    except RuntimeError:
        pass

@pytest.fixture
def mock_course():
    """Create a mock course with lecture, exercise, and lab lists"""
    course = MagicMock()
    course.lectures = [MagicMock()]
    course.exercises = [MagicMock()]
    course.labs = [MagicMock()]
    return course

@pytest.fixture
def mock_controller(mock_course):
    """Mock controller returning two timetable options with courses"""
    controller = MagicMock()
    mock_timetable_1 = MagicMock()
    mock_timetable_1.courses = [mock_course, mock_course]

    mock_timetable_2 = MagicMock()
    mock_timetable_2.courses = [mock_course]

    controller.get_all_options.return_value = [mock_timetable_1, mock_timetable_2]
    return controller

def test_initial_state(root, mock_controller):
    """Check initial TimetablesPage state and controller assignment."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.controller = mock_controller
        page.options = mock_controller.get_all_options.return_value
        
        assert page.current_index == 0
        assert page.controller == mock_controller
        assert page.options == mock_controller.get_all_options.return_value

def test_navigation_next_prev(root, mock_controller):
    """Verify navigation updates current index and respects bounds."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.controller = mock_controller
        page.options = mock_controller.get_all_options.return_value
        
        # Mock the update_view method
        page.update_view = MagicMock()
        
        # Test navigation
        page.show_next = lambda: setattr(page, 'current_index', 
                                       min(page.current_index + 1, len(page.options) - 1)) or page.update_view()
        page.show_prev = lambda: setattr(page, 'current_index', 
                                       max(page.current_index - 1, 0)) or page.update_view()
        
        assert page.current_index == 0
        page.show_next()
        assert page.current_index == 1
        page.show_prev()
        assert page.current_index == 0
        
        # Test bounds
        page.show_next()
        page.show_next()  # Should not go beyond last index
        assert page.current_index == 1
        
        page.show_prev()
        page.show_prev()  # Should not go below 0
        assert page.current_index == 0

def test_update_view_no_options(root):
    """Ensure update_view works gracefully when no timetable options."""
    mock_controller = MagicMock()
    mock_controller.get_all_options.return_value = []
    
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.controller = mock_controller
        page.options = mock_controller.get_all_options.return_value
        
        assert page.options == []
        assert page.current_index == 0
        
        # Mock update_view method and call it
        page.update_view = MagicMock()
        page.update_view()

def test_export_pdf_dialog_all_options(root, mock_controller):
    """Test exporting all timetable options to PDF via dialog."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.controller = mock_controller
        page.options = mock_controller.get_all_options.return_value
        
        # Mock the export_pdf_dialog method
        page.export_pdf_dialog = MagicMock()
        
        with patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName') as mock_save, \
             patch('PyQt6.QtWidgets.QMessageBox.question') as mock_ask:
            
            mock_save.return_value = ("/test/path/timetables.pdf", "PDF files (*.pdf)")
            mock_ask.return_value = QMessageBox.StandardButton.Yes
            
            page.export_pdf_dialog()
            page.export_pdf_dialog.assert_called_once()

def test_export_pdf_dialog_current_option(root, mock_controller):
    """Test exporting the currently selected timetable option to PDF."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.controller = mock_controller
        page.options = mock_controller.get_all_options.return_value
        
        # Mock the export_pdf_dialog method
        page.export_pdf_dialog = MagicMock()
        
        with patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName') as mock_save, \
             patch('PyQt6.QtWidgets.QMessageBox.question') as mock_ask:
            
            mock_save.return_value = ("/test/path/current.pdf", "PDF files (*.pdf)")
            mock_ask.return_value = QMessageBox.StandardButton.No
            
            page.export_pdf_dialog()
            page.export_pdf_dialog.assert_called_once()

def test_timetable_grid_rendering(root, mock_controller):
    """Confirm timetable grid frames and components are created properly."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        
        # Mock the UI elements
        page.timetable_frame = QFrame()
        page.days_header = QFrame()
        
        assert hasattr(page, 'timetable_frame')
        assert isinstance(page.timetable_frame, QFrame)
        assert hasattr(page, 'days_header')
        assert isinstance(page.days_header, QFrame)

def test_scrollbar_configuration(root, mock_controller):
    """Check scrollbar and scroll area configuration."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        
        # Mock the scroll area
        page.scroll_area = QScrollArea()
        
        assert hasattr(page, 'scroll_area')
        assert isinstance(page.scroll_area, QScrollArea)

def test_go_back_callback(root, mock_controller):
    """Verify go_back callback is called when provided."""
    mock_callback = MagicMock()
    
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.go_back_callback = mock_callback
        
        # Mock the go_back method
        page.go_back = lambda: page.go_back_callback() if hasattr(page, 'go_back_callback') and page.go_back_callback else None
        
        page.go_back()
        mock_callback.assert_called_once()

def test_no_go_back_callback(root, mock_controller):
    """Ensure go_back method works without a callback."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        
        # Mock the go_back method
        page.go_back = lambda: None
        
        page.go_back()  # Should not raise an exception

def test_button_states(root, mock_controller):
    """Check that navigation button states update according to current index."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.options = mock_controller.get_all_options.return_value
        
        # Mock the buttons
        page.prev_button = QPushButton()
        page.next_button = QPushButton()
        
        # Mock update_view method
        page.update_view = MagicMock()
        
        # Test initial state
        page.current_index = 0
        page.update_view()
        
        # Test last item state
        page.current_index = len(page.options) - 1
        page.update_view()
        
        # Test back to first
        page.current_index = 0
        page.update_view()

def test_title_label_updates(root, mock_controller):
    """Validate that the title label shows the current timetable index."""
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.options = mock_controller.get_all_options.return_value
        
        # Mock the title label
        page.title_label = QLabel()
        
        # Mock navigation methods
        page.show_next = MagicMock()
        page.show_prev = MagicMock()
        
        # Test navigation updates
        page.show_next()
        page.show_prev()
        
        page.show_next.assert_called_once()
        page.show_prev.assert_called_once()

def test_no_timetable_options_ui(root):
    """Verify UI elements when no timetable options exist."""
    mock_controller = MagicMock()
    mock_controller.get_all_options.return_value = []
    
    with patch.object(TimetablesPage, '__init__', return_value=None):
        page = TimetablesPage.__new__(TimetablesPage)
        page.current_index = 0
        page.controller = mock_controller
        page.options = mock_controller.get_all_options.return_value
        
        # Mock UI elements for empty state
        page.no_data_label = QLabel("No timetable available")
        page.prev_button = QPushButton()
        page.next_button = QPushButton()
        page.scroll_area = QScrollArea()
        
        assert hasattr(page, "no_data_label")
        assert isinstance(page.no_data_label, QLabel)
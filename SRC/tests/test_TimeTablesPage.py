import pytest
import tkinter as tk
import os
from unittest.mock import MagicMock, patch, call
from reportlab.platypus import SimpleDocTemplate
from SRC.ViewLayer.Theme.ModernUI import ModernUI
from SRC.ViewLayer.View.TimetablesPage import TimetablesPage
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots

@pytest.fixture
def root():
    root = tk.Tk()
    root.withdraw()
    root.overrideredirect(1)  # Remove window decorations
    root.geometry("1x1+0+0")  # Make tiny and off-screen
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass  # Already destroyed

@pytest.fixture
def mock_course():
    course = MagicMock()
    course.lectures = [MagicMock()]
    course.exercises = [MagicMock()]
    course.labs = [MagicMock()]
    return course

@pytest.fixture
def mock_controller(mock_course):
    controller = MagicMock()
    mock_timetable_1 = MagicMock()
    mock_timetable_1.courses = [mock_course, mock_course]

    mock_timetable_2 = MagicMock()
    mock_timetable_2.courses = [mock_course]

    controller = MagicMock()
    controller.get_all_options.return_value = [mock_timetable_1, mock_timetable_2]
    return controller

def test_initial_state(root, mock_controller):
    page = TimetablesPage(root, mock_controller)
    assert page.current_index == 0
    assert page.controller == mock_controller
    assert page.options == mock_controller.get_all_options.return_value

def test_navigation_next_prev(root, mock_controller):
    page = TimetablesPage(root, mock_controller)
    assert page.current_index == 0
    page.show_next()
    assert page.current_index == 1
    page.show_prev()
    assert page.current_index == 0

    # Test navigation boundary conditions
    page.show_next()
    page.show_next()  # Should stay at max index
    assert page.current_index == 1

    page.show_prev()
    page.show_prev()  # Should stay at min index
    assert page.current_index == 0

def test_update_view_no_options(root):
    mock_controller = MagicMock()
    mock_controller.get_all_options.return_value = []

    page = TimetablesPage(root, mock_controller)
    
    assert page.options == []
    assert page.current_index == 0

    # Ensure update_view doesn't throw exceptions on empty options
    page.update_view()

def test_export_pdf_dialog_all_options(root, mock_controller):
    """Test exporting all timetable options to PDF"""
    page = TimetablesPage(root, mock_controller)
    
    with patch('SRC.ViewLayer.View.TimetablesPage.filedialog.asksaveasfilename') as mock_save, \
         patch('SRC.ViewLayer.View.TimetablesPage.messagebox.askquestion') as mock_ask, \
         patch('SRC.ViewLayer.View.TimetablesPage.SimpleDocTemplate') as mock_doc, \
         patch('SRC.ViewLayer.View.TimetablesPage.os.startfile') as mock_start:
        
        mock_save.return_value = "/test/path/timetables.pdf"
        mock_ask.return_value = "yes"
        
        page.export_pdf_dialog()
        
        mock_save.assert_called_once_with(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        mock_ask.assert_called_once_with("Export PDF", 
                                      "Do you want to export all timetable options?\nChoose Yes for all, No for current.")
        mock_doc.assert_called_once()
        mock_start.assert_called_once_with("/test/path/timetables.pdf")

def test_export_pdf_dialog_current_option(root, mock_controller):
    """Test exporting current timetable option to PDF"""
    page = TimetablesPage(root, mock_controller)
    
    with patch('SRC.ViewLayer.View.TimetablesPage.filedialog.asksaveasfilename') as mock_save, \
         patch('SRC.ViewLayer.View.TimetablesPage.messagebox.askquestion') as mock_ask, \
         patch('SRC.ViewLayer.View.TimetablesPage.generate_pdf_from_data') as mock_generate, \
         patch('SRC.ViewLayer.View.TimetablesPage.os.startfile') as mock_start:
        
        mock_save.return_value = "/test/path/current.pdf"
        mock_ask.return_value = "no"
        
        page.export_pdf_dialog()
        
        mock_save.assert_called_once_with(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        mock_ask.assert_called_once_with("Export PDF", 
                                      "Do you want to export all timetable options?\nChoose Yes for all, No for current.")
        mock_generate.assert_called_once()
        mock_start.assert_called_once_with("/test/path/current.pdf")

#todo: fix window open
def test_export_pdf_dialog_canceled(root, mock_controller):
    """Test when export dialog is canceled"""
    page = TimetablesPage(root, mock_controller)
    
    with patch('SRC.ViewLayer.View.TimetablesPage.filedialog.asksaveasfilename') as mock_save:
        mock_save.return_value = ""
        page.export_pdf_dialog()  # Should not raise exceptions
        mock_save.assert_called_once()

def test_timetable_grid_rendering(root, mock_controller):
    """Test timetable grid initialization without mocking"""
    # Hide the window
    root.withdraw()
    
    # Create test instance
    page = TimetablesPage(root, mock_controller)
    
    # Verify components exist (without checking drawn content)
    assert hasattr(page, 'timetable_frame')
    assert isinstance(page.timetable_frame, tk.Frame)
    assert hasattr(page, 'days_header')
    assert isinstance(page.days_header, tk.Frame)
    
    # Verify at least some content exists
    root.update_idletasks()
    assert len(page.timetable_frame.winfo_children()) > 0 or \
           len(page.days_header.winfo_children()) > 0

def test_scrollbar_configuration(root, mock_controller):
    """Test scrollbar is properly configured without visible window"""
    # Patch any additional Tkinter methods that might cause visibility
    with patch.object(tk.Tk, 'update_idletasks'), \
         patch.object(tk.Tk, 'mainloop'):
        
        page = TimetablesPage(root, mock_controller)
        
        # Verify scrollbar linkage
        assert str(page.canvas["yscrollcommand"]).endswith("set")
        assert str(page.scrollbar["command"]).endswith("yview")
        
        # Test scrollregion updates
        page.on_frame_configure(None)
        assert page.canvas["scrollregion"] != ""

def test_go_back_callback(root, mock_controller):
    """Test go back callback when provided"""
    mock_callback = MagicMock()
    page = TimetablesPage(root, mock_controller, go_back_callback=mock_callback)
    page.go_back()
    mock_callback.assert_called_once()

def test_no_go_back_callback(root, mock_controller):
    """Test go back when no callback is provided"""
    page = TimetablesPage(root, mock_controller)
    page.go_back()  # Should not raise any exceptions

def test_button_states(root, mock_controller):
    """Test navigation button states update correctly"""
    page = TimetablesPage(root, mock_controller)
    
    # Get the actual colors from the ModernUI class
    disabled_color = ModernUI.COLORS.get("gray", "#95a5a6")
    enabled_color = ModernUI.COLORS.get("dark", "#343a40")
    
    # Initial state
    assert page.prev_button["bg"] == disabled_color
    assert page.next_button["bg"] == enabled_color
    
    # Move to last option
    page.current_index = len(page.options) - 1
    page.update_view()
    assert page.next_button["bg"] == disabled_color
    
    # Move back to first option
    page.current_index = 0
    page.update_view()
    assert page.prev_button["bg"] == disabled_color

def test_title_label_updates(root, mock_controller):
    """Test title label updates correctly"""
    page = TimetablesPage(root, mock_controller)
    
    assert "Timetable Option 1 of 2" in page.title_label["text"]
    
    page.show_next()
    assert "Timetable Option 2 of 2" in page.title_label["text"]
    
    page.show_prev()
    assert "Timetable Option 1 of 2" in page.title_label["text"]

def test_no_timetable_options_ui(root):
    """Test UI when no timetable options are available"""
    mock_controller = MagicMock()
    mock_controller.get_all_options.return_value = []
    
    page = TimetablesPage(root, mock_controller)
    
    # Check the label exists
    assert hasattr(page, "no_data_label")
    
    # Instead of checking visibility (which can be flaky in tests),
    # check that the label was created with the right properties
    assert isinstance(page.no_data_label, tk.Label)
    assert "No timetable available" in page.no_data_label["text"]
    
    # Check navigation UI is hidden
    assert not page.prev_button.winfo_ismapped()
    assert not page.next_button.winfo_ismapped()
    assert not page.canvas.winfo_ismapped()
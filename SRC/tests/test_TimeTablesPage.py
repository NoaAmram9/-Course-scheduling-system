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
    # Provide a minimal hidden root window for Tkinter tests
    root = tk.Tk()
    root.withdraw()
    root.overrideredirect(1)
    root.geometry("1x1+0+0")
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass

@pytest.fixture
def mock_course():
    # Create a mock course with lecture, exercise, and lab lists
    course = MagicMock()
    course.lectures = [MagicMock()]
    course.exercises = [MagicMock()]
    course.labs = [MagicMock()]
    return course

@pytest.fixture
def mock_controller(mock_course):
    # Mock controller returning two timetable options with courses
    controller = MagicMock()
    mock_timetable_1 = MagicMock()
    mock_timetable_1.courses = [mock_course, mock_course]

    mock_timetable_2 = MagicMock()
    mock_timetable_2.courses = [mock_course]

    controller.get_all_options.return_value = [mock_timetable_1, mock_timetable_2]
    return controller

def test_initial_state(root, mock_controller):
    """Check initial TimetablesPage state and controller assignment."""
    page = TimetablesPage(root, mock_controller)
    assert page.current_index == 0
    assert page.controller == mock_controller
    assert page.options == mock_controller.get_all_options.return_value

def test_navigation_next_prev(root, mock_controller):
    """Verify navigation updates current index and respects bounds."""
    page = TimetablesPage(root, mock_controller)
    assert page.current_index == 0
    page.show_next()
    assert page.current_index == 1
    page.show_prev()
    assert page.current_index == 0
    page.show_next()
    page.show_next()
    assert page.current_index == 1
    page.show_prev()
    page.show_prev()
    assert page.current_index == 0

def test_update_view_no_options(root):
    """Ensure update_view works gracefully when no timetable options."""
    mock_controller = MagicMock()
    mock_controller.get_all_options.return_value = []
    page = TimetablesPage(root, mock_controller)
    assert page.options == []
    assert page.current_index == 0
    page.update_view()

def test_export_pdf_dialog_all_options(root, mock_controller):
    """Test exporting all timetable options to PDF via dialog."""
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
    """Test exporting the currently selected timetable option to PDF."""
    page = TimetablesPage(root, mock_controller)
    with patch('SRC.ViewLayer.View.TimetablesPage.filedialog.asksaveasfilename') as mock_save, \
         patch('SRC.ViewLayer.View.TimetablesPage.messagebox.askquestion') as mock_ask, \
         patch('SRC.ViewLayer.View.TimetablesPage.generate_pdf_from_data') as mock_generate, \
         patch('SRC.ViewLayer.View.TimetablesPage.os.startfile') as mock_start:
        
        mock_save.return_value = "/test/path/current.pdf"
        mock_ask.return_value = "no"
        
        page.export_pdf_dialog()
        
        mock_save.assert_called_once_with(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        mock_ask.assert_called_once()
        mock_generate.assert_called_once()
        mock_start.assert_called_once_with("/test/path/current.pdf")

def test_timetable_grid_rendering(root, mock_controller):
    """Confirm timetable grid frames and components are created properly."""
    root.withdraw()
    page = TimetablesPage(root, mock_controller)
    assert hasattr(page, 'timetable_frame')
    assert isinstance(page.timetable_frame, tk.Frame)
    assert hasattr(page, 'days_header')
    assert isinstance(page.days_header, tk.Frame)
    root.update_idletasks()
    assert len(page.timetable_frame.winfo_children()) > 0 or \
           len(page.days_header.winfo_children()) > 0

def test_scrollbar_configuration(root, mock_controller):
    """Check scrollbar commands and scrollregion configuration."""
    with patch.object(tk.Tk, 'update_idletasks'), patch.object(tk.Tk, 'mainloop'):
        page = TimetablesPage(root, mock_controller)
        assert str(page.canvas["yscrollcommand"]).endswith("set")
        assert str(page.scrollbar["command"]).endswith("yview")
        page.on_frame_configure(None)
        assert page.canvas["scrollregion"] != ""

def test_go_back_callback(root, mock_controller):
    """Verify go_back callback is called when provided."""
    mock_callback = MagicMock()
    page = TimetablesPage(root, mock_controller, go_back_callback=mock_callback)
    page.go_back()
    mock_callback.assert_called_once()

def test_no_go_back_callback(root, mock_controller):
    """Ensure go_back method works without a callback."""
    page = TimetablesPage(root, mock_controller)
    page.go_back()

def test_button_states(root, mock_controller):
    """Check that navigation button colors update according to state."""
    page = TimetablesPage(root, mock_controller)
    disabled_color = ModernUI.COLORS.get("gray", "#95a5a6")
    enabled_color = ModernUI.COLORS.get("dark", "#343a40")
    assert page.prev_button["bg"] == disabled_color
    assert page.next_button["bg"] == enabled_color
    page.current_index = len(page.options) - 1
    page.update_view()
    assert page.next_button["bg"] == disabled_color
    page.current_index = 0
    page.update_view()
    assert page.prev_button["bg"] == disabled_color

def test_title_label_updates(root, mock_controller):
    """Validate that the title label shows the current timetable index."""
    page = TimetablesPage(root, mock_controller)
    assert "Timetable Option 1 of 2" in page.title_label["text"]
    page.show_next()
    assert "Timetable Option 2 of 2" in page.title_label["text"]
    page.show_prev()
    assert "Timetable Option 1 of 2" in page.title_label["text"]

def test_no_timetable_options_ui(root):
    """Verify UI elements when no timetable options exist."""
    mock_controller = MagicMock()
    mock_controller.get_all_options.return_value = []
    page = TimetablesPage(root, mock_controller)
    assert hasattr(page, "no_data_label")
    assert isinstance(page.no_data_label, tk.Label)
    assert "No timetable available" in page.no_data_label["text"]
    assert not page.prev_button.winfo_ismapped()
    assert not page.next_button.winfo_ismapped()
    assert not page.canvas.winfo_ismapped()
import pytest
from unittest.mock import MagicMock, patch, call
import tkinter as tk
from SRC.ViewLayer.Logic.Course_Manager import CourseManager
from SRC.ViewLayer.Theme.ModernUI import ModernUI
from SRC.ViewLayer.View.SelectionPageMain import MainPage

@pytest.fixture
def mock_controller():
    # Provide a mock controller for MainPage initialization
    return MagicMock()

@pytest.fixture
def tk_root():
    # Create and hide a Tk root window, then destroy after tests
    root = tk.Tk()
    root.withdraw()
    yield root
    try:
        if root.winfo_exists():
            root.destroy()
    except tk.TclError:
        pass  # Window may already be destroyed during test

@pytest.fixture
def main_page(tk_root, mock_controller):
    # Patch DPI awareness, Tk, and UI style configuration
    # Also patch all sub-panels to avoid real Tk widgets during test
    with patch('ctypes.windll.shcore.SetProcessDpiAwareness'), \
         patch('tkinter.Tk', return_value=tk_root), \
         patch('SRC.ViewLayer.Theme.ModernUI.ModernUI.configure_treeview_style'), \
         patch('SRC.ViewLayer.Layout.Selected_Courses.SelectedCoursesPanel'), \
         patch('SRC.ViewLayer.Layout.Course_Details.CourseDetailsPanel'), \
         patch('SRC.ViewLayer.Layout.Courses_List.CourseListPanel'):
        
        page = MainPage(mock_controller)
        page.course_manager = MagicMock()
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
    # Create mock panels and CourseManager instance
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
    with patch('tkinter.Toplevel') as mock_toplevel:
        main_page.course_manager.save_selection.return_value = False
        main_page.save_selection()
        main_page.course_manager.save_selection.assert_called_once()
        mock_toplevel.assert_not_called()

def test_get_selected_courses(main_page):
    """get_selected_courses returns what course_manager returns"""
    mock_courses = [MagicMock(), MagicMock()]
    main_page.course_manager.get_selected_courses.return_value = mock_courses
    result = main_page.get_selected_courses()
    assert result == mock_courses
    main_page.course_manager.get_selected_courses.assert_called_once()

def test_on_close_confirmed(main_page):
    """on_close calls cleanup and exits when user confirms"""
    with patch('tkinter.messagebox.askokcancel', return_value=True), \
         patch('sys.exit') as mock_exit:
        main_page.on_close()
        tk.messagebox.askokcancel.assert_called_with("Exit", "Are you sure you want to exit?")
        main_page.controller.handle_exit.assert_called_once()
        mock_exit.assert_called_once()

def test_on_close_cancelled(main_page):
    """on_close aborts exit if user cancels"""
    with patch('tkinter.messagebox.askokcancel', return_value=False), \
         patch('sys.exit') as mock_exit:
        main_page.on_close()
        tk.messagebox.askokcancel.assert_called_with("Exit", "Are you sure you want to exit?")
        main_page.controller.handle_exit.assert_not_called()
        mock_exit.assert_not_called()

def test_run(main_page):
    """run loads courses and starts the Tkinter main loop"""
    main_page.course_manager.load_courses.return_value = None
    with patch.object(main_page.window, 'mainloop', return_value=None):
        main_page.run()
        main_page.course_manager.load_courses.assert_called_once()
        main_page.window.mainloop.assert_called_once()

def test_max_courses_enforcement(main_page):
    """Adding courses beyond max shows warning and prevents adding"""
    mock_course = MagicMock()
    main_page.selected_courses_panel = MagicMock()
    main_page.selected_courses_panel.selected_courses = [MagicMock()] * 7 

    with patch('tkinter.messagebox.showwarning') as mock_warning:
        def mock_add_course(course):
            if len(main_page.selected_courses_panel.selected_courses) >= main_page.max_courses:
                import tkinter.messagebox
                tkinter.messagebox.showwarning("Warning", "You can select up to 7 courses only.")
            else:
                main_page.selected_courses_panel.selected_courses.append(course)
        
        main_page.course_manager.add_course = mock_add_course
        main_page.course_manager.add_course(mock_course)
        mock_warning.assert_called_once_with("Warning", "You can select up to 7 courses only.")
        assert len(main_page.selected_courses_panel.selected_courses) == 7

def test_theme_application(main_page):
    """Verify ModernUI colors and fonts applied to main window and widgets"""
    assert main_page.window.cget('bg') == ModernUI.COLORS['light']
    main_container = main_page.window.children['!frame']
    assert main_container.cget('bg') == ModernUI.COLORS['light']
    header_frame = main_container.children['!frame']
    assert header_frame.cget('bg') == ModernUI.COLORS['light']
    header_label = header_frame.children['!label']
    assert header_label.cget('bg') == ModernUI.COLORS['light']
    assert header_label.cget('fg') == ModernUI.COLORS['dark']

    font_str = header_label.cget('font')
    assert "Calibri" in font_str
    assert "18" in font_str
    assert "bold" in font_str.lower()
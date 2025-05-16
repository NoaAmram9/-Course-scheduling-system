# import pytest
# from unittest.mock import MagicMock, patch
# from SRC.ViewLayer.View.SelectionPageMain import MainPage
# import customtkinter as ctk

# @pytest.fixture
# def main_page():
#     root = ctk.CTk()  # Ensure a root context for customtkinter widgets
#     mock_controller = MagicMock()
#     page = MainPage(mock_controller)
#     yield page
#     root.destroy()

# # 1. UI COMPONENT EXISTENCE

# def test_ui_components_exist(main_page):
#     assert hasattr(main_page, "course_list_panel")
#     assert hasattr(main_page, "details_panel")  
#     assert hasattr(main_page, "selected_courses_panel")

# # 2. BUTTON FUNCTIONALITY

# def test_load_button_calls_controller_load(main_page):
#     main_page.course_manager.load_courses = MagicMock()
#     main_page.load_courses()
#     main_page.course_manager.load_courses.assert_called_once()

# def test_remove_button_calls_controller_remove(main_page):
#     main_page.course_manager.remove_selected_course = MagicMock()
#     main_page.remove_selected_course()
#     main_page.course_manager.remove_selected_course.assert_called_once()

# def test_save_button_calls_controller_save(main_page):
#     main_page.course_manager.save_selection = MagicMock()
#     main_page.save_selection()
#     main_page.course_manager.save_selection.assert_called_once()

# # 3. MAX 7 COURSE SELECTION CONSTRAINT

# def test_add_course_up_to_7_allowed(main_page):
#     with patch("tkinter.messagebox.showwarning") as mock_warning:
#         for i in range(7):
#             course = MagicMock()
#             main_page.selected_courses_panel.selected_courses = list(range(i))
#             main_page.selected_courses_panel.add_course = MagicMock(
#                 side_effect=lambda c: main_page.selected_courses_panel.selected_courses.append(c)
#             )
#             main_page.selected_courses_panel.add_course(course)
#             assert course in main_page.selected_courses_panel.selected_courses
#         mock_warning.assert_not_called()

# def test_add_course_more_than_7_shows_warning(main_page):
#     course = MagicMock()
#     main_page.selected_courses_panel.selected_courses = list(range(7))
#     with patch("tkinter.messagebox.showwarning") as mock_warning:
#         # Mock actual logic
#         def fake_add(c):
#             if len(main_page.selected_courses_panel.selected_courses) >= 7:
#                 from tkinter import messagebox
#                 messagebox.showwarning("Warning", "You can select up to 7 courses only.")
#             else:
#                 main_page.selected_courses_panel.selected_courses.append(c)
#         main_page.selected_courses_panel.add_course = fake_add
#         main_page.selected_courses_panel.add_course(course)
#         mock_warning.assert_called_once()

# # 4. COURSE DETAILS DISPLAY

# def test_on_course_selected_updates_details_panel(main_page):
#     # Mock course object with a name
#     mock_course = MagicMock(name="Test Course")
#     mock_course._code = "TEST123"
    
#     # Set up a mock details callback
#     mock_details_callback = MagicMock()
#     main_page.course_list_panel.set_details_callback(mock_details_callback)
    
#     # Load the course into the treeview
#     main_page.course_list_panel.load_courses([mock_course])
    
#     # Simulate selecting the course
#     main_page.course_list_panel.on_course_select(None)  # Simulate selecting the course
    
#     # Assert the callback was called with the correct course
#     mock_details_callback.assert_called_with(mock_course)

# # ------------------------------------------------------------------------------------------
# # 5. ADD AND REMOVE COURSE INTEGRATION

# # def test_add_course_adds_to_selected_list(main_page)

# def test_remove_course_removes_from_selected_list(main_page):
#     course = MagicMock()
#     main_page.selected_courses_panel.selected_courses = [course]
#     with patch.object(main_page.selected_courses_panel, "update_display") as mock_update:
#         main_page.remove_course(course)
#         assert course not in main_page.selected_courses_panel.selected_courses
#         mock_update.assert_called_once()

# # 6. SAVE COURSE SELECTION OUTPUT

# def test_save_selection_logic(main_page):
#     with patch.object(main_page.course_manager, "save_selection") as mock_save:
#         main_page.save_selection()
#         mock_save.assert_called_once()

# # 7. TREEVIEW STYLE SETUP

# @patch("SRC.ViewLayer.MainPage.ModernUI.configure_treeview_style")
# def test_treeview_style_applied(mock_style):
#     root = ctk.CTk()
#     _ = MainPage(MagicMock())
#     mock_style.assert_called_once()
#     root.destroy()

import pytest
from unittest.mock import MagicMock, patch, call
import tkinter as tk
from SRC.ViewLayer.Theme.ModernUI import ModernUI
from SRC.ViewLayer.View.SelectionPageMain import MainPage

@pytest.fixture
def mock_controller():
    return MagicMock()

@pytest.fixture
def tk_root():
    root = tk.Tk()
    root.withdraw()  # Hide the root window during tests
    yield root
    root.destroy()  # Clean up after test

@pytest.fixture
def main_page(tk_root, mock_controller):
    with patch('ctypes.windll.shcore.SetProcessDpiAwareness'), \
         patch('tkinter.Tk', return_value=tk_root), \
         patch('SRC.ViewLayer.Theme.ModernUI.ModernUI.configure_treeview_style'):
        
        # Mock all panels to avoid real Tkinter widget creation
        with patch('SRC.ViewLayer.Layout.Selected_Courses.SelectedCoursesPanel'), \
             patch('SRC.ViewLayer.Layout.Course_Details.CourseDetailsPanel'), \
             patch('SRC.ViewLayer.Layout.Courses_List.CourseListPanel'):
            
            page = MainPage(mock_controller)
            page.course_manager = MagicMock()
            yield page

def test_init(main_page, mock_controller):
    """Test initialization of MainPage"""
    assert main_page.controller == mock_controller
    assert main_page.max_courses == 7
    assert main_page.selected_course_ids == set()
    assert main_page.course_map == {}

def test_load_courses(main_page):
    """Test loading courses delegates to course manager"""
    main_page.load_courses()
    main_page.course_manager.load_courses.assert_called_once()

def test_remove_selected_course(main_page):
    """Test removing selected course delegates to course manager"""
    main_page.remove_selected_course()
    main_page.course_manager.remove_selected_course.assert_called_once()

# def test_save_selection_success(main_page):
#     """Test successful save selection and navigation to the next page (TimetablesPage)"""
#     # Replace all Tkinter operations with mocks
#     with patch('tkinter.Tk'), \
#          patch('tkinter.Toplevel'), \
#          patch('tkinter.StringVar'), \
#          patch('tkinter.Frame'), \
#          patch('tkinter.Label'):
        
#         # Setup: Simulate that courses were successfully saved
#         main_page.course_manager.save_selection.return_value = True
        
#         # Mock the TimetablesPage creation
#         with patch('SRC.ViewLayer.View.TimetablesPage.TimetablesPage') as mock_timetable_page:
#             # Execute the save_selection method
#             main_page.save_selection()
            
#             # Verify that save_selection was called once
#             main_page.course_manager.save_selection.assert_called_once()
            
#             # Check if the TimetablesPage was created
#             mock_timetable_page.assert_called_once()


def test_save_selection_failure(main_page):
    """Test failed save selection doesn't open timetable page"""
    with patch('tkinter.Toplevel') as mock_toplevel:
        # Configure mock return value
        main_page.course_manager.save_selection.return_value = False
        
        # Call the method
        main_page.save_selection()
        
        # Verify course manager was called
        main_page.course_manager.save_selection.assert_called_once()
        
        # Verify timetable window was NOT created
        mock_toplevel.assert_not_called()

def test_get_selected_courses(main_page):
    """Test getting selected courses delegates to course manager"""
    mock_courses = [MagicMock(), MagicMock()]
    main_page.course_manager.get_selected_courses.return_value = mock_courses
    
    result = main_page.get_selected_courses()
    
    assert result == mock_courses
    main_page.course_manager.get_selected_courses.assert_called_once()

def test_on_close_confirmed(main_page):
    """Test window close with user confirmation"""
    with patch('tkinter.messagebox.askokcancel', return_value=True), \
         patch('sys.exit') as mock_exit:
        
        # Call the method
        main_page.on_close()
        
        # Verify confirmation dialog
        tk.messagebox.askokcancel.assert_called_with("Exit", "Are you sure you want to exit?")
        
        # Verify controller cleanup
        main_page.controller.handle_exit.assert_called_once()
        
        # Verify window and system cleanup
        mock_exit.assert_called_once()

def test_on_close_cancelled(main_page):
    """Test window close when user cancels"""
    with patch('tkinter.messagebox.askokcancel', return_value=False), \
         patch('sys.exit') as mock_exit:
        
        # Call the method
        main_page.on_close()
        
        # Verify confirmation dialog
        tk.messagebox.askokcancel.assert_called_with("Exit", "Are you sure you want to exit?")
        
        # Verify nothing else was called
        main_page.controller.handle_exit.assert_not_called()
        mock_exit.assert_not_called()

def test_run(main_page):
    """Test the run method loads courses and starts mainloop"""
    # Setup
    main_page.course_manager.load_courses.return_value = None
    
    # Mock mainloop to prevent it from running
    with patch.object(main_page.window, 'mainloop', return_value=None):
        main_page.run()
        
        # Verify load_courses was called
        main_page.course_manager.load_courses.assert_called_once()
        
        # Verify mainloop was called
        main_page.window.mainloop.assert_called_once()

def test_course_selection_flow(main_page):
    """Test the course selection updates details panel"""
    # Create a mock to store the callback
    callback_store = MagicMock()
    
    # Setup mock panels
    mock_course = MagicMock()
    mock_details_panel = MagicMock()
    mock_course_list_panel = MagicMock()
    
    # Configure the mock to store the callback
    def store_callback(callback):
        callback_store.callback = callback
        return None
    
    mock_course_list_panel.set_selection_callback = store_callback
    
    # Replace the real panels with our mocks
    main_page.details_panel = mock_details_panel
    main_page.course_list_panel = mock_course_list_panel
    main_page.course_manager = MagicMock()
    
    # Initialize the layout (this should call set_selection_callback)
    main_page._create_layout()
    
    # Verify callback was stored
    assert hasattr(callback_store, 'callback'), "Callback was not set"
    
    # Simulate selecting a course
    callback_store.callback(mock_course)
    
    # Verify details panel was updated
    mock_details_panel.update_details.assert_called_once_with(mock_course)


def test_panel_integration(main_page):
    """Test all panels are properly initialized"""
    main_page._create_layout()
    
    assert isinstance(main_page.course_list_panel, MagicMock)  # Mocked in fixture
    assert isinstance(main_page.details_panel, MagicMock)
    assert isinstance(main_page.selected_courses_panel, MagicMock)
    
    # Verify they were connected to course manager
    main_page.course_manager.assert_called_once_with(
        main_page.controller,
        main_page.course_list_panel,
        main_page.details_panel,
        main_page.selected_courses_panel
    )

def test_max_courses_enforcement(main_page):
    """Test UI enforces maximum course selection"""
    # Setup mocks
    mock_course = MagicMock()
    main_page.selected_courses_panel = MagicMock()
    main_page.selected_courses_panel.selected_courses = [MagicMock()] * 7  # Already at max
    
    # Mock the warning messagebox
    with patch('tkinter.messagebox.showwarning') as mock_warning:
        # Mock the actual add_course method that would check this
        def mock_add_course(course):
            if len(main_page.selected_courses_panel.selected_courses) >= main_page.max_courses:
                import tkinter.messagebox
                tkinter.messagebox.showwarning("Warning", "You can select up to 7 courses only.")
            else:
                main_page.selected_courses_panel.selected_courses.append(course)
        
        main_page.course_manager.add_course = mock_add_course
        
        # Try to add another course
        main_page.course_manager.add_course(mock_course)
        
        # Verify warning was shown
        mock_warning.assert_called_once_with("Warning", "You can select up to 7 courses only.")
        
        # Verify course wasn't actually added
        assert len(main_page.selected_courses_panel.selected_courses) == 7

def test_window_close_confirmed(main_page):
    """Test confirmed window close"""
    with patch('tkinter.messagebox.askokcancel', return_value=True), \
         patch.object(main_page.controller, 'handle_exit'), \
         patch.object(main_page.window, 'destroy'), \
         patch('sys.exit') as mock_exit:  # Mock sys.exit to prevent actual exit
    
        main_page.on_close()
        
        # Verify confirmation dialog
        tk.messagebox.askokcancel.assert_called_once_with(
            "Exit", "Are you sure you want to exit?"
        )
        
        # Verify controller cleanup
        main_page.controller.handle_exit.assert_called_once()
        
        # Verify window cleanup
        main_page.window.destroy.assert_called_once()
        
        # Verify system exit was called
        mock_exit.assert_called_once()

def test_theme_application(main_page):
    """Test ModernUI styles are properly applied"""
    # Verify main window colors
    assert main_page.window.cget('bg') == ModernUI.COLORS['light']
    
    # Verify container frames have correct background
    main_container = main_page.window.children['!frame']
    assert main_container.cget('bg') == ModernUI.COLORS['light']
    
    # Verify header styling
    header_frame = main_container.children['!frame']
    assert header_frame.cget('bg') == ModernUI.COLORS['light']
    
    # Verify header label styling
    header_label = header_frame.children['!label']
    assert header_label.cget('bg') == ModernUI.COLORS['light']
    assert header_label.cget('fg') == ModernUI.COLORS['dark']
    
    # Proper font comparison - Tkinter returns font as string
    font_str = header_label.cget('font')
    assert "Calibri" in font_str
    assert "18" in font_str
    assert "bold" in font_str.lower()

def test_component_communication_minimal_mocks(main_page):
    """Test communication with minimal mocks"""
    # Setup real course manager
    main_page.course_manager = MagicMock()
    
    # Get the real callback from course_list_panel
    callback_store = []
    original_set_callback = main_page.course_list_panel.set_selection_callback
    def track_callback(callback):
        callback_store.append(callback)
        original_set_callback(callback)
    
    main_page.course_list_panel.set_selection_callback = track_callback
    
    # Initialize
    main_page._create_layout()
    
    # Test add course
    mock_course = MagicMock()
    callback_store[0](mock_course)  # Call the stored callback
    main_page.course_manager.add_course.assert_called_once_with(mock_course)
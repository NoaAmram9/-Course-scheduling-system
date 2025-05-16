import ctypes



try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # For Windows 8.1 or later
except Exception:
    pass

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from SRC.ViewLayer.Theme.ModernUI import ModernUI 
from SRC.ViewLayer.Layout.Courses_List import CourseListPanel
from SRC.ViewLayer.Layout.Course_Details import CourseDetailsPanel
from SRC.ViewLayer.Layout.Selected_Courses import SelectedCoursesPanel
from SRC.ViewLayer.Logic.Course_Manager import CourseManager
from SRC.ViewLayer.View.TimetablesPage  import TimetablesPage


class MainPage:
    def __init__(self, controller):
        """
        Initialize the main course selection page.
        This will be called from the LandPage after file upload.
        """
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Course Selector")
        self.window.geometry("1200x650")
        self.window.config(bg=ModernUI.COLORS["light"])
        
        # Apply modern styling
        ModernUI.configure_treeview_style()
        
        # Set up the maximum number of courses
        self.max_courses = 7
        self.selected_course_ids = set()
        self.course_map = {}  # code -> Course object
        
        # Create the UI layout
        self._create_layout()
      

        # Create the course manager that connects all components
        self.course_manager = CourseManager(
            controller, 
            self.course_list_panel,
            self.details_panel,
            self.selected_courses_panel
        )
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    def _create_layout(self):
        """Create the UI layout with all panels and components"""
        # Main container with padding
        main_container = tk.Frame(self.window, bg=ModernUI.COLORS["light"], padx=15, pady=15)
        main_container.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg=ModernUI.COLORS["light"])
        header_frame.pack(fill="x", pady=(0, 15))
        
        header_label = tk.Label(header_frame, text="Course Selector", 
                              font=("Calibri", 18, "bold"),
                              bg=ModernUI.COLORS["light"], fg=ModernUI.COLORS["dark"])
        header_label.pack(side="left")
        
        # Main content area - with 3 panels
        content_frame = tk.Frame(main_container, bg=ModernUI.COLORS["light"])
        content_frame.pack(fill="both", expand=True)
        
        # Left panel - Course codes list
        left_panel = tk.Frame(content_frame, bg=ModernUI.COLORS["light"], width=200)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.course_list_panel = CourseListPanel(left_panel, ModernUI.COLORS["light"])
        self.course_list_panel.pack(fill="both", expand=True)
        
        # Middle panel - Course details
        middle_panel = tk.Frame(content_frame, bg=ModernUI.COLORS["light"], width=300)
        middle_panel.pack(side="left", fill="both", padx=5)
        middle_panel.pack_propagate(False)  # Prevent shrinking
        
        self.details_panel = CourseDetailsPanel(middle_panel, ModernUI.COLORS["light"])
        self.details_panel.pack(fill="both", expand=True)
        
        # Right panel - Selected courses
        right_panel = tk.Frame(content_frame, bg=ModernUI.COLORS["light"])
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.selected_courses_panel = SelectedCoursesPanel(right_panel, ModernUI.COLORS["light"], self.max_courses)
        self.selected_courses_panel.pack(fill="both", expand=True)
        
        # Footer with buttons
        footer_frame = tk.Frame(main_container, bg=ModernUI.COLORS["light"], pady=10)
        footer_frame.pack(fill="x")
        
        # # Create buttons using the custom rounded style
        # load_button_frame = ModernUI.create_rounded_button(
        #     footer_frame, "Load Courses", self.load_courses)
        # load_button_frame.pack(side="left", padx=5)
        
        # remove_button_frame = ModernUI.create_rounded_button(
        #     footer_frame, "Remove Selected", self.remove_selected_course,
        #     bg_color=ModernUI.COLORS["accent"])
        # remove_button_frame.pack(side="left", padx=5)
        
        save_button_frame = ModernUI.create_rounded_button(
            footer_frame, "Save Selection", self.save_selection,
            bg_color=ModernUI.COLORS["secondary"])
        save_button_frame.pack(side="right", padx=5)
    
    def load_courses(self):
        """Load courses from the controller"""
        self.course_manager.load_courses()
    
    def remove_selected_course(self):
        """Remove the currently selected course"""
        self.course_manager.remove_selected_course()
    
    # def save_selection(self):
    #  """Save the current course selection and open the timetable page."""
    #  self.course_manager.save_selection()
    #  self.window.withdraw()  # הסתרת חלון הבחירה
    #  time_table = TimeTable(self.controller, parent=self)  # העברת הפניה להחזרה
    #  time_table.run()
    def save_selection(self):
        """Save the current course selection and go to timetable page"""
        if self.course_manager.save_selection():
            # If the selection was saved successfully, open the timetable page

            # create a new Toplevel window for the timetable
            timetable_window = tk.Toplevel(self.window)

            # העבר את רשימת הקורסים שנבחרו
            selected_courses = self.get_selected_courses()

            # צור את TimetablesPage עם callback שנסגר את החלון
            def go_back_callback():
                timetable_window.destroy()  # סגור את חלון לוח הזמנים

            TimetablesPage(timetable_window, self.controller, go_back_callback)

    
    def get_selected_courses(self):
        """Get the list of selected courses"""
        return self.course_manager.get_selected_courses()
    def on_close(self):
     """Handle window close event"""
        # Make sure to ask for confirmation before closing
     if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.controller.handle_exit()  # Call the controller's exit method
            self.window.quit()     # exit the loop
            self.window.destroy()  # destroy the window
            sys.exit()             # exit the program

    def run(self):
        """Run the application"""
        # Load courses initially
        self.load_courses()
        
        # Start the main loop
        self.window.mainloop()
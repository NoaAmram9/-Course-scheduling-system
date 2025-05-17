import tkinter as tk
from SRC.ViewLayer.Theme.ModernUI import ModernUI

class CourseDetailsPanel(tk.Frame):
    """Panel to display detailed course information"""
    
    def __init__(self, parent, bg_color):
        super().__init__(parent, bg=bg_color, padx=10, pady=10)
        
        # Title
        self.title_label = tk.Label(self, text="Course Details", 
                                  font=("Calibri", 12, "bold"),
                                  bg=bg_color, fg=ModernUI.COLORS["dark"])
        self.title_label.pack(anchor="w", pady=(0, 5))
        
        # Content Frame with border
        content_frame = tk.Frame(self, bg=ModernUI.COLORS["white"],
                               highlightbackground=ModernUI.COLORS["gray"],
                               highlightthickness=1, bd=0)
        content_frame.pack(fill="both", expand=True)
        
        # Course details
        self.code_label = tk.Label(content_frame, text="Code: ", font=("Calibri", 10, "bold"),
                                 bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                 anchor="w")
        self.code_label.pack(fill="x", padx=10, pady=(10, 5))
        
        self.name_label = tk.Label(content_frame, text="Name: ", font=("Calibri", 10),
                                 bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                 anchor="w", wraplength=250)
        self.name_label.pack(fill="x", padx=10, pady=2)
        
        self.instructor_label = tk.Label(content_frame, text="Instructor: ", font=("Calibri", 10),
                                       bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
                                       anchor="w")
        self.instructor_label.pack(fill="x", padx=10, pady=2)
        
        # Schedule details frame
        schedule_frame = tk.Frame(content_frame, bg=ModernUI.COLORS["white"])
        schedule_frame.pack(fill="x", padx=10, pady=5)
        
        # tk.Label(schedule_frame, text="Schedule:", font=("Calibri", 10, "bold"),
        #        bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"]).pack(anchor="w")
        
        # self.lectures_label = tk.Label(schedule_frame, text="• Lectures: ", font=("Calibri", 9),
        #                              bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
        #                              anchor="w")
        # self.lectures_label.pack(fill="x", padx=(10, 0), pady=1)
        
        # self.exercises_label = tk.Label(schedule_frame, text="• Exercises: ", font=("Calibri", 9),
        #                               bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
        #                               anchor="w")
        # self.exercises_label.pack(fill="x", padx=(10, 0), pady=1)
        
        # self.labs_label = tk.Label(schedule_frame, text="• Labs: ", font=("Calibri", 9),
        #                          bg=ModernUI.COLORS["white"], fg=ModernUI.COLORS["dark"],
        #                          anchor="w")
        # self.labs_label.pack(fill="x", padx=(10, 0), pady=1)
        
        # Action button
        self.add_button_frame = ModernUI.create_rounded_button(
            self, "Add Course", self.add_course, 
            bg_color=ModernUI.COLORS["ligth_pink"], width=200)
        self.add_button_frame.pack(pady=10)
        
        # Reference to the selected course
        self.current_course = None
        
    def update_details(self, course):
        """Update the panel with course details"""
        self.current_course = course
        
        if course:
            self.code_label.config(text=f"Code: {course._code}")
            self.name_label.config(text=f"Name: {course._name}")
            self.instructor_label.config(text=f"Prof.: {course._instructor}")
            
            # self.lectures_label.config(text=f"• Lectures: {len(course._lectures)}")
            # self.exercises_label.config(text=f"• Exercises: {len(course._exercises)}")
            # self.labs_label.config(text=f"• Labs: {len(course._labs)}")
        else:
            self.code_label.config(text="Code: ")
            self.name_label.config(text="Name: ")
            self.instructor_label.config(text="Prof.: ")
            # self.lectures_label.config(text="• Lectures: ")
            # self.exercises_label.config(text="• Exercises: ")
            # self.labs_label.config(text="• Labs: ")
    
    def set_add_callback(self, callback):
        """Set the callback function for the add button"""
        self.add_callback = callback
        
    def add_course(self):
        """Add the current course to selected courses"""
        if self.current_course and hasattr(self, 'add_callback'):
            self.add_callback(self.current_course._code)
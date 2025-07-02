import os
from PyQt5.QtWidgets import QPushButton

class ModernUIQt5:
    """Modern UI styling and components for Qt5"""

    COLORS = {
        "primary": "#ecac57",
        "secondary": "#944e25",
        "accent": "#FFDAB9",
        "light": "#ecf0f1",
        "dark": "#625D5D",
        "white": "#ffffff",
        "black": "#000000",
        "gray": "#95a5a6",
        "selected": "#D9B382",
        "lecture": "#ffe4e4",
        "lab": "#ffffef",
        "exercise": "#e8ffff",
        "light_blue": "#9F9BFF",
        "light_pink": "#FFDAB9",
        "timetable_bg": "#f8f9fa",
        "timetable_header": "#e9ecef",
        "timetable_border": "#dee2e6",
        "timetable_hover": "#f1f3f4",
        "time_slot_bg": "#ffffff",
        "course_selected": "#e3f2fd",
        "success": "#28a745",
        "warning": "#ffc107",
        "danger": "#dc3545",
        "info": "#17a2b8",
    }

    @staticmethod
    def create_button(text, style="light_pink", min_width=120):
        button = QPushButton(text)
        button.setMinimumWidth(min_width)
        button.setMinimumHeight(35)

        bg_color = ModernUIQt5.COLORS.get(style, ModernUIQt5.COLORS["light_blue"])
        hover_color = "#7f8c8d" if style == "light_pink" else "#95a5a6"
        # button.setStyleSheet(f"""
        #     QPushButton {{
        #         background-color: {bg_color};
        #         color: white;
        #         border: none;
        #         border-radius: 10px;
        #         padding: 6px 12px;
        #     }}
        #     QPushButton:hover {{
        #         background-color: {hover_color};
        #         opacity: 0.85;
        #     }}
        # """)
        return button

    @staticmethod
    def get_main_stylesheet(dark=False):
        if dark:
            base = ModernUIQt5._load_stylesheet("modern_ui_base_dark.qss")
            selection = ModernUIQt5._load_stylesheet("modern_ui_selection_dark.qss")
        else:
            base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
            selection = ModernUIQt5._load_stylesheet("modern_ui_selection.qss")
        return base + "\n" + selection
    
    @staticmethod
    def get_timetable_stylesheet(dark=False):
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        timetable = ModernUIQt5._load_stylesheet("modern_ui_timetable.qss")
        navbar = ModernUIQt5._load_stylesheet("NavBars_ui.qss")
        dropdown = ModernUIQt5._load_stylesheet("dropdown.qss")
        dark_theme = ModernUIQt5._load_stylesheet("dark_theme.qss") if dark else ""
        return base + "\n" + timetable + "\n" + navbar + "\n" + dropdown + "\n" + dark_theme


    @staticmethod
    def get_manual_schedule_stylesheet(dark_mode=False): 
        """Load and combine base + manual schedule styles"""
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        selection = ModernUIQt5._load_stylesheet("modern_ui_selection.qss")
        timetable = ModernUIQt5._load_stylesheet("modern_ui_timetable.qss")
        if dark_mode:
            dark = ModernUIQt5._load_stylesheet("modern_ui_base_dark.qss")
            return base + "\n" + timetable + "\n" + selection + "\n" + dark
        # return base + "\n" + selection + "\n" + timetable
        return base + "\n" +timetable
      
    @staticmethod
    def get_navbars_stylesheet(dark=False):
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        navbar = ModernUIQt5._load_stylesheet("NavBars_ui.qss")
        dropdown = ModernUIQt5._load_stylesheet("dropdown_menu.qss")
        dark_theme = ModernUIQt5._load_stylesheet("dark_theme.qss") if dark else ""
        return base + "\n" + navbar + "\n" + dropdown + "\n" + dark_theme

    @staticmethod
    def get_dropdown_stylesheet(dark=False):
        dropdown = ModernUIQt5._load_stylesheet("dropdown.qss")
        dark_theme = ModernUIQt5._load_stylesheet("dark_theme.qss") if dark else ""
        return dropdown + "\n" + dark_theme

    @staticmethod
    def _load_stylesheet(filename):
        try:
            path = os.path.join(os.path.dirname(__file__), filename)
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
            return ""
    
    @staticmethod
    def get_Start_Page_stylesheet():
        """Load and combine base + selection styles"""
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        start = ModernUIQt5._load_stylesheet("modern_ui_start.qss")
        return base + "\n" + start
    
    @staticmethod
    def get_Add_Course_stylesheet():
        """Load and combine base + selection styles"""
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        addCourse = ModernUIQt5._load_stylesheet("add_course.qss")
        return base + "\n" + addCourse
    
    @staticmethod
    def get_login_stylesheet(): #TODO: add dark mode support
        """Load and combine base + manual schedule styles"""
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        login = ModernUIQt5._load_stylesheet("LoginStyle.qss")
       
        return base + "\n" +login
    
    @staticmethod
    def get_register_stylesheet(): #TODO: add dark mode support
        """Load and combine base + manual schedule styles"""
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        register = ModernUIQt5._load_stylesheet("RegisterStyle.qss")
        return base + "\n" +register
    
    

import os
from PyQt5.QtWidgets import QPushButton

class ModernUIQt5:
    """Modern UI styling and components for Qt5"""

    # Color palette
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
        # Timetable specific colors
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
    def create_button(text, style="primary", min_width=120):
        """Create a modern styled QPushButton with custom background"""
        button = QPushButton(text)
        button.setMinimumWidth(min_width)
        button.setMinimumHeight(35)

        bg_color = ModernUIQt5.COLORS.get(style, ModernUIQt5.COLORS["primary"])
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #944e25;
                opacity: 0.85;
            }}
        """)
        return button
    
    
    @staticmethod
    def get_main_stylesheet():
        """Load and combine base + selection styles"""
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        selection = ModernUIQt5._load_stylesheet("modern_ui_selection.qss")
        return base + "\n" + selection
    
    
    @staticmethod
    def get_timetable_stylesheet():
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        timetable = ModernUIQt5._load_stylesheet("modern_ui_timetable.qss")
        navbar = ModernUIQt5._load_stylesheet("NavBars_ui.qss")
        return base + "\n" + timetable + "\n" + navbar

    @staticmethod
    def get_navbars_stylesheet():
        """Load and combine base + selection styles"""
        base = ModernUIQt5._load_stylesheet("modern_ui_base.qss")
        navbar = ModernUIQt5._load_stylesheet("NavBars_ui.qss")
        return base + "\n" + navbar
    
    @staticmethod
    def _load_stylesheet(filename):
        """Load a QSS file from the theme folder"""
        try:
            path = os.path.join(os.path.dirname(__file__), filename)
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
            return ""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ModernUIQt5:
    """Modern UI styling and components for Qt5"""
    
    # Color palette
    COLORS = {
        "primary": "#3499FF",
        "secondary": "#36F6A9",
        "accent": "#FFDAB9",
        "light": "#ecf0f1",
        "dark": "#625D5D",
        "white": "#ffffff",
        "black": "#000000",
        "gray": "#95a5a6",
        "selected": "#d5f5e3",
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
        """Create a modern styled button"""
        button = QPushButton(text)
        button.setMinimumWidth(min_width)
        button.setMinimumHeight(35)
        
        if style == "primary":
            bg_color = ModernUIQt5.COLORS["primary"]
        elif style == "accent":
            bg_color = ModernUIQt5.COLORS["accent"]
        elif style == "secondary":
            bg_color = ModernUIQt5.COLORS["secondary"]
        elif style == "success":
            bg_color = ModernUIQt5.COLORS["success"]
        elif style == "warning":
            bg_color = ModernUIQt5.COLORS["warning"]
        elif style == "danger":
            bg_color = ModernUIQt5.COLORS["danger"]
        elif style == "info":
            bg_color = ModernUIQt5.COLORS["info"]
        else:
            bg_color = ModernUIQt5.COLORS["primary"]
            
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {ModernUIQt5.adjust_color(bg_color, -20)};
            }}
            QPushButton:pressed {{
                background-color: {ModernUIQt5.adjust_color(bg_color, -40)};
            }}
        """)
        
        return button
        
    @staticmethod
    def adjust_color(hex_color, amount):
        """Adjust a hex color by the given amount"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    @staticmethod
    def get_main_stylesheet():
        """Get the main application stylesheet"""
        return f"""
            QMainWindow {{
                background-color: {ModernUIQt5.COLORS["light"]};
            }}
            
            QLabel#headerLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {ModernUIQt5.COLORS["dark"]};
            }}
            
            QLabel#panelTitle {{
                font-size: 12px;
                font-weight: bold;
                color: {ModernUIQt5.COLORS["dark"]};
                margin-bottom: 5px;
            }}
        """
        
    @staticmethod
    def get_panel_stylesheet():
        """Get stylesheet for panels"""
        return f"""
            QWidget {{
                background-color: {ModernUIQt5.COLORS["light"]};
            }}
            
            QLineEdit#searchInput {{
                border: 2px solid {ModernUIQt5.COLORS["gray"]};
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                background-color: {ModernUIQt5.COLORS["white"]};
            }}
            
            QLineEdit#searchInput:focus {{
                border-color: {ModernUIQt5.COLORS["primary"]};
            }}
            
            QTreeWidget#courseTree, QTreeWidget#selectedTable {{
                border: 1px solid {ModernUIQt5.COLORS["gray"]};
                border-radius: 6px;
                background-color: {ModernUIQt5.COLORS["white"]};
                alternate-background-color: #f8f9fa;
                selection-background-color: {ModernUIQt5.COLORS["primary"]};
                font-size: 10px;
            }}
            
            QTreeWidget::item {{
                height: 25px;
                padding: 2px;
            }}
            
            QTreeWidget::item:selected {{
                background-color: {ModernUIQt5.COLORS["primary"]};
                color: white;
            }}
            
            QHeaderView::section {{
                background-color: {ModernUIQt5.COLORS["light"]};
                color: {ModernUIQt5.COLORS["dark"]};
                border: none;
                border-right: 1px solid {ModernUIQt5.COLORS["gray"]};
                padding: 8px;
                font-weight: bold;
                font-size: 10px;
            }}
            
            QLabel#countLabel {{
                color: {ModernUIQt5.COLORS["primary"]};
                font-weight: bold;
            }}
        """
        
    @staticmethod
    def get_details_panel_stylesheet():
        """Get stylesheet for details panel"""
        return f"""
            QWidget {{
                background-color: {ModernUIQt5.COLORS["light"]};
            }}
            
            QFrame#detailsFrame {{
                background-color: {ModernUIQt5.COLORS["white"]};
                border: 1px solid {ModernUIQt5.COLORS["gray"]};
                border-radius: 8px;
            }}
            
            QLabel#detailLabel {{
                font-size: 11px;
                color: {ModernUIQt5.COLORS["dark"]};
                margin: 2px 0px;
            }}
        """
    
    @staticmethod
    def get_timetable_stylesheet():
        """Get comprehensive stylesheet for timetable page"""
        return f"""
            /* Main Window Styling */
            QMainWindow {{
                background-color: {ModernUIQt5.COLORS["timetable_bg"]};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            /* Navigation Frame */
            QFrame#navFrame {{
                background-color: {ModernUIQt5.COLORS["white"]};
                border: 2px solid {ModernUIQt5.COLORS["timetable_border"]};
                border-radius: 12px;
                padding: 15px;
                margin: 5px;
            }}
            
            /* Navigation Buttons */
            QPushButton#backButton {{
                background-color: {ModernUIQt5.COLORS["info"]};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                padding: 10px 15px;
                min-height: 20px;
            }}
            QPushButton#backButton:hover {{
                background-color: {ModernUIQt5.adjust_color(ModernUIQt5.COLORS["info"], -20)};
                transform: translateY(-1px);
            }}
            QPushButton#backButton:pressed {{
                background-color: {ModernUIQt5.adjust_color(ModernUIQt5.COLORS["info"], -40)};
            }}
            
            QPushButton#navButton {{
                background-color: {ModernUIQt5.COLORS["primary"]};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                padding: 8px 12px;
                min-height: 20px;
            }}
            QPushButton#navButton:hover {{
                background-color: {ModernUIQt5.adjust_color(ModernUIQt5.COLORS["primary"], -20)};
            }}
            QPushButton#navButton:pressed {{
                background-color: {ModernUIQt5.adjust_color(ModernUIQt5.COLORS["primary"], -40)};
            }}
            QPushButton#navButton[disabled="true"] {{
                background-color: {ModernUIQt5.COLORS["gray"]};
                color: {ModernUIQt5.COLORS["white"]};
                opacity: 0.6;
            }}
            
            QPushButton#exportButton {{
                background-color: {ModernUIQt5.COLORS["success"]};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                padding: 8px 12px;
                min-height: 20px;
            }}
            QPushButton#exportButton:hover {{
                background-color: {ModernUIQt5.adjust_color(ModernUIQt5.COLORS["success"], -20)};
                transform: translateY(-1px);
            }}
            QPushButton#exportButton:pressed {{
                background-color: {ModernUIQt5.adjust_color(ModernUIQt5.COLORS["success"], -40)};
            }}
            
            /* Title Label */
            QLabel#titleLabel {{
                color: {ModernUIQt5.COLORS["dark"]};
                font-size: 16px;
                font-weight: bold;
                padding: 5px 10px;
                background-color: {ModernUIQt5.COLORS["timetable_header"]};
                border-radius: 6px;
                border: 1px solid {ModernUIQt5.COLORS["timetable_border"]};
            }}
            
            /* No Data Label */
            QLabel#noDataLabel {{
                color: {ModernUIQt5.COLORS["gray"]};
                font-size: 18px;
                font-weight: 500;
                padding: 40px;
                background-color: {ModernUIQt5.COLORS["white"]};
                border: 2px dashed {ModernUIQt5.COLORS["timetable_border"]};
                border-radius: 12px;
            }}
            
            /* Scroll Area */
            QScrollArea#scrollArea {{
                border: 2px solid {ModernUIQt5.COLORS["timetable_border"]};
                border-radius: 12px;
                background-color: {ModernUIQt5.COLORS["white"]};
            }}
            
            QScrollArea#scrollArea QScrollBar:vertical {{
                background-color: {ModernUIQt5.COLORS["timetable_bg"]};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollArea#scrollArea QScrollBar::handle:vertical {{
                background-color: {ModernUIQt5.COLORS["gray"]};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollArea#scrollArea QScrollBar::handle:vertical:hover {{
                background-color: {ModernUIQt5.COLORS["primary"]};
            }}
            
            /* Timetable Widget */
            QWidget#timetableWidget {{
                background-color: {ModernUIQt5.COLORS["white"]};
                border-radius: 8px;
            }}
            
            /* Timetable Grid Styling */
            QTableWidget#timetableGrid {{
                background-color: {ModernUIQt5.COLORS["white"]};
                border: 1px solid {ModernUIQt5.COLORS["timetable_border"]};
                border-radius: 8px;
                gridline-color: {ModernUIQt5.COLORS["timetable_border"]};
                font-size: 10px;
                selection-background-color: {ModernUIQt5.COLORS["course_selected"]};
            }}
            
            QTableWidget#timetableGrid::item {{
                border: 1px solid {ModernUIQt5.COLORS["timetable_border"]};
                padding: 4px;
                text-align: center;
            }}
            
            QTableWidget#timetableGrid::item:hover {{
                background-color: {ModernUIQt5.COLORS["timetable_hover"]};
            }}
            
            /* Header Styling */
            QHeaderView::section {{
                background-color: {ModernUIQt5.COLORS["timetable_header"]};
                color: {ModernUIQt5.COLORS["dark"]};
                border: 1px solid {ModernUIQt5.COLORS["timetable_border"]};
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
                text-align: center;
            }}
            
            /* Time Slot Styling */
            QLabel#timeSlot {{
                background-color: {ModernUIQt5.COLORS["time_slot_bg"]};
                color: {ModernUIQt5.COLORS["dark"]};
                border: 1px solid {ModernUIQt5.COLORS["timetable_border"]};
                padding: 8px;
                font-weight: bold;
                font-size: 10px;
                text-align: center;
            }}
            
            /* Course Cell Styling */
            QLabel#courseCell {{
                border: 1px solid {ModernUIQt5.COLORS["timetable_border"]};
                padding: 4px;
                font-size: 9px;
                font-weight: 500;
                text-align: center;
                border-radius: 4px;
            }}
            
            /* Lecture Cell */
            QLabel#lectureCell {{
                background-color: {ModernUIQt5.COLORS["lecture"]};
                color: {ModernUIQt5.COLORS["dark"]};
                border: 2px solid #ffcccc;
            }}
            
            /* Lab Cell */
            QLabel#labCell {{
                background-color: {ModernUIQt5.COLORS["lab"]};
                color: {ModernUIQt5.COLORS["dark"]};
                border: 2px solid #ffffcc;
            }}
            
            /* Exercise Cell */
            QLabel#exerciseCell {{
                background-color: {ModernUIQt5.COLORS["exercise"]};
                color: {ModernUIQt5.COLORS["dark"]};
                border: 2px solid #ccffff;
            }}
            
            /* Empty Cell */
            QLabel#emptyCell {{
                background-color: {ModernUIQt5.COLORS["white"]};
                border: 1px solid {ModernUIQt5.COLORS["timetable_border"]};
            }}
            
            /* Hover Effects */
            QLabel#courseCell:hover {{
                transform: scale(1.02);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        """
    
    @staticmethod
    def create_timetable_button(text, style="primary", icon=None):
        """Create a specialized button for timetable navigation"""
        button = QPushButton(text)
        button.setMinimumHeight(40)
        
        # Add icon if provided
        if icon:
            button.setText(f"{icon} {text}")
        
        if style == "back":
            button.setObjectName("backButton")
            button.setMinimumWidth(180)
        elif style == "nav":
            button.setObjectName("navButton")
            button.setMinimumWidth(90)
        elif style == "export":
            button.setObjectName("exportButton")
            button.setMinimumWidth(120)
        
        return button
    
    @staticmethod
    def create_timetable_label(text, label_type="default"):
        """Create a specialized label for timetable"""
        label = QLabel(text)
        
        if label_type == "title":
            label.setObjectName("titleLabel")
            label.setAlignment(Qt.AlignCenter)
        elif label_type == "no_data":
            label.setObjectName("noDataLabel")
            label.setAlignment(Qt.AlignCenter)
        elif label_type == "time_slot":
            label.setObjectName("timeSlot")
            label.setAlignment(Qt.AlignCenter)
        elif label_type == "course_cell":
            label.setObjectName("courseCell")
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
        
        return label
    
    @staticmethod
    def style_course_cell(label, course_type="lecture"):
        """Apply specific styling to course cells based on type"""
        base_id = "courseCell"
        
        if course_type.lower() == "lecture":
            label.setObjectName("lectureCell")
        elif course_type.lower() == "lab":
            label.setObjectName("labCell")
        elif course_type.lower() == "exercise":
            label.setObjectName("exerciseCell")
        else:
            label.setObjectName("emptyCell")
        
        return label
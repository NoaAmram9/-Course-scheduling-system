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
    # @staticmethod
    # def get_Land_Page_stylesheet():
    #     """Get stylesheet for Landpage"""
    #     return f"""
            
    #     """
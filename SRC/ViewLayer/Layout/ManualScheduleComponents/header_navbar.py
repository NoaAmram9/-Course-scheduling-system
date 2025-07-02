import os
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt  
class HeaderNavbar:
    def __init__(self, instance):
        """Initialize the header navigation bar."""
        self.instance = instance
        
    def create_layout(self):
        
        button_style = """
            QPushButton {
                background-color: #D8C4B6;
                border: 1px solid #D8C4B6;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D8C4BE;
                border: 1px solid #213555;
                color: #000;
            }
        """
        
        """Return a QHBoxLayout containing header elements."""
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 10)  # Top margin for header
            
         # --- First line: back button & dark mode---
        top_row = QHBoxLayout()
        top_row.setContentsMargins(10, 10, 10, 10)
        
        current_dir = os.path.dirname(__file__)
        icon_path = os.path.normpath(os.path.join(current_dir, "../../Icons/back1.png"))   
        self.go_back_button = QPushButton()
        self.go_back_button.setIcon(QIcon(QPixmap(icon_path)))
        self.go_back_button.setStyleSheet(button_style)
        self.go_back_button.setObjectName("gobackButton")
        self.go_back_button.clicked.connect(lambda: self.instance.handle_go_back_click())
        top_row.addWidget(self.go_back_button)
        
        top_row.addStretch()
        
        current_dir = os.path.dirname(__file__)
        icon_path = os.path.normpath(os.path.join(current_dir, "../../Icons/sun.png"))   
        self.dark_mode_button = QPushButton()
        self.dark_mode_button.setIcon(QIcon(QPixmap(icon_path)))
        self.dark_mode_button.setStyleSheet(button_style)
        self.dark_mode_button.setObjectName("darkModeButton")
        self.dark_mode_button.clicked.connect(lambda: self.instance.handle_dark_mode_click())
        top_row.addWidget(self.dark_mode_button)
                
        header_layout.addLayout(top_row)

        # --- שורה שנייה: כותרת + כפתורים נוספים ---
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(10, 10, 10, 10)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(lambda: self.instance.handle_reset())
        self.go_back_button.setStyleSheet(button_style)
        
        bottom_row.addWidget(self.reset_button)
            
        self.undo_button = QPushButton("Undo")
        self.undo_button.setObjectName("undoButton")
        # self.undo_button.setAlignment(Qt.AlignLeft)
        self.undo_button.clicked.connect(lambda: self.instance.undo_last_action())
        self.go_back_button.setStyleSheet(button_style)
        bottom_row.addWidget(self.undo_button)
        # self.undo_button.setVisible(False)  # Initially hidden, can be shown later if needed
        
        bottom_row.addStretch()  # Push undo button to the left
            
        self.title = QLabel("Manual Schedule")
        self.title.setObjectName("pageTitle")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #213555;")
        bottom_row.addWidget(self.title) 
        
        bottom_row.addStretch() 
        
        self.save_button = QPushButton("Save")
        self.save_button.setObjectName("saveButton")
        self.go_back_button.setStyleSheet(button_style)
        # self.undo_button.setAlignment(Qt.AlignLeft)
        self.save_button.clicked.connect(lambda: self.instance.save_schedule())
        bottom_row.addWidget(self.save_button)
        
        header_layout.addLayout(bottom_row)
        
        return header_layout
    def get_buttons(self):
        return self.save_button, self.reset_button, self.undo_button, self.dark_mode_button
    
    def change_dark_icon(self, dark_mode_enabled):
        current_dir = os.path.dirname(__file__)
        icon_name = "moon.png" if dark_mode_enabled else "sun.png"
        icon_path = os.path.normpath(os.path.join(current_dir, f"../../Icons/{icon_name}"))
        self.dark_mode_button.setIcon(QIcon(QPixmap(icon_path)))
        if dark_mode_enabled:
            self.title.setStyleSheet("font-size: 30px; font-weight: bold; color: #ffffff;")
        else:         
            self.title.setStyleSheet("font-size: 30px; font-weight: bold; color: #213555;")


        
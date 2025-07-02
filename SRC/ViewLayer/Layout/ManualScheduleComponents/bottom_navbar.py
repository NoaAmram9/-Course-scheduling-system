from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class BottomNavBar:
    def __init__(self, instance):
        self.instance = instance
        
    def create_layout(self):
        # ===== BOTTOM: LOGO ======
        
        bottom_widget = QWidget()
        bottom_widget.setObjectName("bottomNavBar")  # חשוב לשם העיצוב
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(10, 10, 10, 10)
        bottom_widget.setLayout(bottom_layout)
        
        # bottom_widget.setStyleSheet("""
        #     QWidget#bottomNavBar {
        #         border: 1px solid #3E5879;
        #         border-radius: 8px;
        #         padding: 6px;
        #     }
        # """)
        
        logo_label = QLabel()
        logo_label.setObjectName("logoLabel")
        current_dir = os.path.dirname(__file__)
        logo_pixmap = QPixmap(os.path.normpath(os.path.join(current_dir, "../../Icons/Logo.png")))
        logo_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(logo_label)
        
        return bottom_widget

    def update(self):
        # Update the bottom navigation bar if needed
        pass

    def destroy(self):
        # Clean up resources if necessary
        pass
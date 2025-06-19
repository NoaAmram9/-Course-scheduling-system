from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class BottomNavBar:
    def __init__(self, instance):
        self.instance = instance
        
    def create_layout(self):
        # ===== BOTTOM: LOGO ======
        bottom_layout = QHBoxLayout()
        
        logo_label = QLabel()
        logo_label.setObjectName("logoLabel")
        current_dir = os.path.dirname(__file__)
        logo_pixmap = QPixmap(os.path.normpath(os.path.join(current_dir, "../../Icons/Logo.jpg")))
        logo_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(logo_label)
        
        return bottom_layout

    def update(self):
        # Update the bottom navigation bar if needed
        pass

    def destroy(self):
        # Clean up resources if necessary
        pass
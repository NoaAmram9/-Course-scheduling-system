from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel 
from PyQt5.QtCore import Qt  
class HeaderNavbar:
    def __init__(self, instance):
        """Initialize the header navigation bar."""
        self.instance = instance
        
    def create_layout(self):
        """Return a QHBoxLayout containing header elements."""
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 10)  # Top margin for header
            
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(lambda: self.instance.handle_reset())
        header_layout.addWidget(self.reset_button)
        # self.undo_button.setVisible(False)  # Initially hidden, can be shown later if needed
        self.reset_button.setEnabled(False)  # Initially disabled, can be enabled later if needed
        # header_layout.addStretch()  # Push undo button to the left
            
            
        self.undo_button = QPushButton("Undo")
        self.undo_button.setObjectName("undoButton")
        # self.undo_button.setAlignment(Qt.AlignLeft)
        self.undo_button.clicked.connect(lambda: self.instance.undo_last_action())
        header_layout.addWidget(self.undo_button)
        # self.undo_button.setVisible(False)  # Initially hidden, can be shown later if needed
        header_layout.addStretch()  # Push undo button to the left
            
        self.title = QLabel("Manual Schedule")
        self.title.setObjectName("pageTitle")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFA500;")  # Example style
        header_layout.addWidget(self.title)
        header_layout.addStretch() 
        
        self.save_button = QPushButton("Save")
        self.save_button.setObjectName("saveButton")
        # self.undo_button.setAlignment(Qt.AlignLeft)
        self.save_button.clicked.connect(lambda: self.instance.save_schedule())
        header_layout.addWidget(self.save_button)
        
        return header_layout
    def get_buttons(self):
        return self.save_button, self.reset_button, self.undo_button
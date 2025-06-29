from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap

from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class StartPageView(QWidget):
    # Signals
    upload_new_file = pyqtSignal()
    continue_existing = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Course Management System")
        self.setGeometry(300, 300, 500, 300)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
       # Set window icon
        icon_path = "Data/Logo.png"
        self.setWindowIcon(QIcon(icon_path))
        logo_label = QLabel()
        logo_pixmap = QPixmap("Data/Logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("LOGO")
            logo_label.setStyleSheet("color: gray; font-size: 16px;")

        logo_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        logo_label.setObjectName("logoLabel")
    

        
        # Title
        title_label = QLabel("Course Management System")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("TitleLabel")
       
 
        # Subtitle
        subtitle_label = QLabel("Choose how you want to proceed:")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setObjectName("SubtitleLabel")
        
        # Buttons layout
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Upload new file button
        self.upload_button = QPushButton("Upload New File")
        self.upload_button.setMinimumHeight(50)
       
        
        # Continue with existing database button
        self.continue_button = QPushButton("Continue with Existing Database")
        self.continue_button.setMinimumHeight(50)
      
      
        
        # Connect buttons to signals
        self.upload_button.clicked.connect(self.upload_new_file.emit)
        self.continue_button.clicked.connect(self.continue_existing.emit)
        
        # Add widgets to layouts
        buttons_layout.addWidget(self.upload_button)
        buttons_layout.addWidget(self.continue_button)
        main_layout.addWidget(logo_label)
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addLayout(buttons_layout)
        
        # Set main layout
        self.setLayout(main_layout)
        self.setStyleSheet(ModernUIQt5.get_Start_Page_stylesheet())
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
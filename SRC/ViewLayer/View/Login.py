from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from SRC.ViewLayer.Layout.Login import LoginLayout


class LoginView(QMainWindow):
    """Login view handling UI display and user interactions"""
    
    # Signals
    login_requested = pyqtSignal(str, str, bool)  # username, password, remember_me
    register_requested = pyqtSignal()
    
    def __init__(self):
        

        super().__init__()
        
        self.init_ui()
        self.load_styles()
      
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Login - Modern App")
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Setup layout
        self.layout_manager = LoginLayout(central_widget)
        self.login_button = self.layout_manager.parent.login_button
        self.username_input = self.layout_manager.parent.username_input
        self.password_input = self.layout_manager.parent.password_input
        self.remember_checkbox = self.layout_manager.parent.remember_checkbox
        self.register_link = self.layout_manager.parent.register_link
        
        self.connect_signals()
        # Center window on screen
        self.center_on_screen()
    
    def center_on_screen(self):
        """Center the window on screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )
    
    def load_styles(self):
        """Load QSS styles for login screen"""
        try:
            with open('Theme/LoginStyle.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            # Fallback inline styles
            self.setStyleSheet(self.get_fallback_styles())
    
    def get_fallback_styles(self):
        """Fallback styles if QSS file not found"""
        return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
        }
        
        #centerFrame {
            background: transparent;
        }
        
        #loginCard {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        #titleLabel {
            color: #2c3e50;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        #subtitleLabel {
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        #fieldLabel {
            color: #2c3e50;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        #inputField {
            padding: 12px 15px;
            border: 2px solid #e0e6ed;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            min-height: 20px;
        }
        
        #inputField:focus {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        #primaryButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 15px;
            font-size: 16px;
            font-weight: bold;
            min-height: 20px;
        }
        
        #primaryButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #5a6fd8, stop:1 #6a4190);
        }
        
        #primaryButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4e63c6, stop:1 #5e3b7e);
        }
        
        #checkBox {
            color: #2c3e50;
            font-size: 12px;
        }
        
        #checkBox::indicator {
            width: 16px;
            height: 16px;
        }
        
        #checkBox::indicator:unchecked {
            border: 2px solid #bdc3c7;
            border-radius: 3px;
            background: white;
        }
        
        #checkBox::indicator:checked {
            background: #667eea;
            border: 2px solid #667eea;
            border-radius: 3px;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        }
        
        #footerLabel {
            color: #7f8c8d;
            font-size: 12px;
        }
        
        #linkButton {
            color: #667eea;
            background: transparent;
            border: none;
            font-size: 12px;
            font-weight: bold;
            text-decoration: underline;
        }
        
        #linkButton:hover {
            color: #5a6fd8;
        }
        """
    
    def connect_signals(self):
        """Connect UI signals to slots"""
        self.login_button.clicked.connect(self.on_login_clicked)
        self.register_link.clicked.connect(self.on_register_clicked)
        
        # Enter key support
        self.username_input.returnPressed.connect(self.on_login_clicked)
        self.password_input.returnPressed.connect(self.on_login_clicked)
    
    def on_login_clicked(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        remember_me = self.remember_checkbox.isChecked()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        self.login_requested.emit(username, password, remember_me)
    
    def on_register_clicked(self):
        """Handle register link click"""
        self.register_requested.emit()
    
    def show_error(self, message):
        """Show error message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Login Error")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                color: #2c3e50;
            }
            QMessageBox QPushButton {
                background: #667eea;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background: #5a6fd8;
            }
        """)
        msg_box.exec_()
    
    def show_success(self, message):
        """Show success message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                color: #2c3e50;
            }
            QMessageBox QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background: #219a52;
            }
        """)
        msg_box.exec_()
    
    def clear_form(self):
        """Clear the form fields"""
        self.username_input.clear()
        self.password_input.clear()
        self.remember_checkbox.setChecked(False)
    
    def set_loading(self, loading):
        """Set loading state"""
        self.login_button.setEnabled(not loading)
        self.login_button.setText("Signing In..." if loading else "Sign In")
        
        if loading:
            self.login_button.setStyleSheet(self.login_button.styleSheet() + """
                #primaryButton {
                    background: #bdc3c7;
                }
            """)
        else:
            self.load_styles()  # Reset styles
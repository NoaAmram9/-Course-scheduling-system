from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from SRC.ViewLayer.Layout.Login import LoginLayout
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5


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
       self.setStyleSheet(ModernUIQt5.get_login_stylesheet())
    
  
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
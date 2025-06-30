from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from SRC.ViewLayer.Layout.Register import RegisterLayout
import re
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5


class RegisterView(QMainWindow):
    """Register view handling UI display and user interactions"""
    
    # Signals
    register_requested = pyqtSignal(dict)  # user_data dict
    login_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_styles()
        
        self.setup_validators()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Register - Modern App")
        self.setFixedSize(800, 700)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Setup layout
        self.layout_manager = RegisterLayout(central_widget)
        self.register_button = self.layout_manager.parent.register_button
        self.login_link = self.layout_manager.parent.login_link
        self.first_name_input = self.layout_manager.parent.first_name_input
        self.last_name_input = self.layout_manager.parent.last_name_input
        self.username_input = self.layout_manager.parent.username_input
        self.email_input = self.layout_manager.parent.email_input
        self.password_input = self.layout_manager.parent.password_input
        self.confirm_password_input = self.layout_manager.parent.confirm_password_input
        self.terms_checkbox = self.layout_manager.parent.terms_checkbox
        self.password_strength_label = self.layout_manager.parent.password_strength_label
        
        
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
    
    def setup_validators(self):
        """Setup input validators"""
        # Username validator (alphanumeric + underscore, 3-20 chars)
        username_regex = QRegExp("^[a-zA-Z0-9_]{3,20}$")
        username_validator = QRegExpValidator(username_regex)
        self.username_input.setValidator(username_validator)
        
        # Name validators (letters, spaces, hyphens only)
        name_regex = QRegExp("^[a-zA-ZÀ-ÿ\\s\\-']{1,50}$")
        name_validator = QRegExpValidator(name_regex)
        self.first_name_input.setValidator(name_validator)
        self.last_name_input.setValidator(name_validator)
    
    def load_styles(self):
       self.setStyleSheet(ModernUIQt5.get_register_stylesheet())
    
   
    def connect_signals(self):
        """Connect UI signals to slots"""
        self.register_button.clicked.connect(self.on_register_clicked)
        self.login_link.clicked.connect(self.on_login_clicked)
        
        # Real-time validation
        self.password_input.textChanged.connect(self.check_password_strength)
        self.confirm_password_input.textChanged.connect(self.check_passwords_match)
        self.email_input.textChanged.connect(self.validate_email)
        self.username_input.textChanged.connect(self.validate_username)
        
        # Enter key support
        self.confirm_password_input.returnPressed.connect(self.on_register_clicked)
    
    def on_register_clicked(self):
        """Handle register button click"""
        # Collect data
        user_data = {
            'first_name': self.first_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'username': self.username_input.text().strip(),
            'email': self.email_input.text().strip(),
            'password': self.password_input.text(),
            'confirm_password': self.confirm_password_input.text()
        }
        
        # Validate data
        validation_result = self.validate_form(user_data)
        if not validation_result['valid']:
            self.show_error(validation_result['message'])
            return
        
        # Check terms agreement
        if not self.terms_checkbox.isChecked():
            self.show_error("You must agree to the Terms of Service and Privacy Policy")
            return
        
        # Remove confirm_password from data before sending
        del user_data['confirm_password']
        
        self.register_requested.emit(user_data)
    
    def validate_form(self, data):
        """Validate form data"""
        # Check required fields
        required_fields = ['first_name', 'last_name', 'username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                field_name = field.replace('_', ' ').title()
                return {'valid': False, 'message': f'{field_name} is required'}
        
        # Validate name fields
        if len(data['first_name']) < 2:
            return {'valid': False, 'message': 'First name must be at least 2 characters long'}
        
        if len(data['last_name']) < 2:
            return {'valid': False, 'message': 'Last name must be at least 2 characters long'}
        
        # Validate username
        if len(data['username']) < 3:
            return {'valid': False, 'message': 'Username must be at least 3 characters long'}
        
        if not re.match("^[a-zA-Z0-9_]+$", data['username']):
            return {'valid': False, 'message': 'Username can only contain letters, numbers, and underscores'}
        
        # Validate email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            return {'valid': False, 'message': 'Please enter a valid email address'}
        
        # Validate password
        if len(data['password']) < 6:
            return {'valid': False, 'message': 'Password must be at least 6 characters long'}
        
        # Check password confirmation
        if data['password'] != data['confirm_password']:
            return {'valid': False, 'message': 'Passwords do not match'}
        
        return {'valid': True}
    
    def check_password_strength(self):
        """Check password strength and update indicator"""
        password = self.password_input.text()
        
        if not password:
            self.password_strength_label.setText("")
            return
        
        strength_score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            strength_score += 1
        else:
            feedback.append("at least 8 characters")
        
        # Uppercase check
        if re.search(r'[A-Z]', password):
            strength_score += 1
        else:
            feedback.append("uppercase letter")
        
        # Lowercase check
        if re.search(r'[a-z]', password):
            strength_score += 1
        else:
            feedback.append("lowercase letter")
        
        # Number check
        if re.search(r'\d', password):
            strength_score += 1
        else:
            feedback.append("number")
        
        # Special character check
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            strength_score += 1
        else:
            feedback.append("special character")
        
        # Update label
        if strength_score <= 2:
            self.password_strength_label.setText("⚠️ Weak password")
            self.password_strength_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        elif strength_score <= 3:
            self.password_strength_label.setText("🔶 Medium password")
            self.password_strength_label.setStyleSheet("color: #f39c12; font-weight: bold;")
        elif strength_score <= 4:
            self.password_strength_label.setText("✅ Strong password")
            self.password_strength_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.password_strength_label.setText("🔒 Very strong password")
            self.password_strength_label.setStyleSheet("color: #27ae60; font-weight: bold;")
    
    def check_passwords_match(self):
        """Check if passwords match"""
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if confirm_password and password != confirm_password:
            self.confirm_password_input.setStyleSheet("""
                #inputField {
                    border-color: #e74c3c !important;
                    background: #fdf2f2 !important;
                }
            """)
        else:
            self.confirm_password_input.setStyleSheet("")
    
    def validate_email(self):
        """Validate email format in real-time"""
        email = self.email_input.text()
        
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.email_input.setStyleSheet("""
                #inputField {
                    border-color: #f39c12 !important;
                    background: #fff9e6 !important;
                }
            """)
        else:
            self.email_input.setStyleSheet("")
    
    def validate_username(self):
        """Validate username format in real-time"""
        username = self.username_input.text()
        
        if username and (len(username) < 3 or not re.match("^[a-zA-Z0-9_]+$", username)):
            self.username_input.setStyleSheet("""
                #inputField {
                    border-color: #f39c12 !important;
                    background: #fff9e6 !important;
                }
            """)
        else:
            self.username_input.setStyleSheet("")
    
    def on_login_clicked(self):
        """Handle login link click"""
        self.login_requested.emit()
    
    def show_error(self, message):
        """Show error message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Registration Error")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: white;
                color: #2c3e50;
            }
            QMessageBox QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background: #c0392b;
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
    def highlight_field(self, field_name):
        """Highlight a specific input field (e.g., email or username)"""
        if field_name == 'email':
            self.email_input.setStyleSheet("""
                #inputField {
                    border: 2px solid #e74c3c;
                    background: #fdf2f2;
                    border-radius: 8px;
                }
            """)
        elif field_name == 'username':
            self.username_input.setStyleSheet("""
                #inputField {
                    border: 2px solid #e74c3c;
                    background: #fdf2f2;
                    border-radius: 8px;
                }
            """)

    def clear_form(self):
        """Clear the form fields"""
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.terms_checkbox.setChecked(False)
        self.password_strength_label.clear()
    
    def set_loading(self, loading):
        """Set loading state"""
        self.register_button.setEnabled(not loading)
        self.register_button.setText("Creating Account..." if loading else "Create Account")
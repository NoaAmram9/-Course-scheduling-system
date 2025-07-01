from PyQt5.QtCore import QObject, QThread, pyqtSignal
from SRC.Controller.UsersController import UsersController


class Login(QThread):
    """Worker thread for login operations"""
    
    login_completed = pyqtSignal(dict)  # Login result
    
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.users_controller = UsersController()
    
    def run(self):
        """Run login operation in background thread"""
        try:
            result = self.users_controller.login_user(self.username, self.password)
            self.login_completed.emit(result)
        except Exception as e:
            error_result = {
                'success': False,
                'message': f'Connection error: {str(e)}',
                'error_code': 'CONNECTION_ERROR'
            }
            self.login_completed.emit(error_result)


class LoginController(QObject):
    """Controller for login operations"""
    
    def __init__(self, view, ui_manager):
        super().__init__()
        self.view = view
        self.ui_manager = ui_manager
        self.current_worker = None
        
        # Connect view signals
        self.view.login_requested.connect(self.handle_login)
        self.view.register_requested.connect(self.handle_register_request)
    
    def handle_login(self, username, password, remember_me):
        """Handle login request"""
        # Basic validation
        if not username.strip():
            self.view.show_error("Username cannot be empty")
            return
        
        if not password:
            self.view.show_error("Password cannot be empty")
            return
        
        if len(username.strip()) < 3:
            self.view.show_error("Username must be at least 3 characters long")
            return
        
        if len(password) < 6:
            self.view.show_error("Password must be at least 6 characters long")
            return
        
        # Set loading state
        self.view.set_loading(True)
        
        # Create and start worker thread
        self.current_worker = Login(username.strip(), password)
        self.current_worker.login_completed.connect(self.handle_login_result)
        self.current_worker.finished.connect(self.cleanup_worker)
        self.current_worker.start()
    
    def handle_login_result(self, result):
        """Handle login result from worker thread"""
        # Reset loading state
        self.view.set_loading(False)
        
        if result['success']:
            # Login successful
            self.view.show_success("Login successful! Redirecting...")
            
            # Clear form for security
            self.view.clear_form()
            
            # Navigate to start page
            user_data = result.get('user', {})
            self.ui_manager.show_start_page(user_data)
            
        else:
            # Login failed
            error_message = self.get_user_friendly_error(result)
            self.view.show_error(error_message)
    
    def get_user_friendly_error(self, result):
        """Convert error codes to user-friendly messages"""
        error_code = result.get('error_code', '')
        default_message = result.get('message', 'Login failed')
        
        error_messages = {
            'MISSING_CREDENTIALS': 'Please enter both username and password',
            'INVALID_CREDENTIALS': 'Invalid username or password. Please try again.',
            'USER_INACTIVE': 'Your account has been deactivated. Please contact support.',
            'CONNECTION_ERROR': 'Unable to connect to server. Please check your internet connection.',
            'UNEXPECTED_ERROR': 'An unexpected error occurred. Please try again later.'
        }
        
        return error_messages.get(error_code, default_message)
    
    def handle_register_request(self):
        """Handle register request"""
        self.ui_manager.show_register()
    
    def cleanup_worker(self):
        """Clean up worker thread"""
        if self.current_worker:
            self.current_worker.deleteLater()
            self.current_worker = None
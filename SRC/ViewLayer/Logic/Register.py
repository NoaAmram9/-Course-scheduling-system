from PyQt5.QtCore import QObject, QThread, pyqtSignal
from SRC.Controller.UsersController import UsersController


class RegisterWorker(QThread):
    """Worker thread for registration operations"""
    
    registration_completed = pyqtSignal(dict)  # Registration result
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.users_controller = UsersController()
    
    def run(self):
        """Run registration operation in background thread"""
        try:
            result = self.users_controller.register_user(self.user_data)
            self.registration_completed.emit(result)
        except Exception as e:
            error_result = {
                'success': False,
                'message': f'Connection error: {str(e)}',
                'error_code': 'CONNECTION_ERROR'
            }
            self.registration_completed.emit(error_result)


class RegisterController(QObject):
    """Controller for registration operations"""
    
    def __init__(self, view, ui_manager):
        super().__init__()
        self.view = view
        self.ui_manager = ui_manager
        self.current_worker = None
        
        # Connect view signals
        self.view.register_requested.connect(self.handle_registration)
        self.view.login_requested.connect(self.handle_login_request)
    
    def handle_registration(self, user_data):
        """Handle registration request"""
       
        # Additional server-side validation
        validation_result = self.validate_user_data(user_data)
        if not validation_result['valid']:
         
            self.view.show_error(validation_result['message'])
            return
        
        # Set loading state
        self.view.set_loading(True)
        
        # Create and start worker thread
        self.current_worker = RegisterWorker(user_data)
        self.current_worker.registration_completed.connect(self.handle_registration_result)
        self.current_worker.finished.connect(self.cleanup_worker)
        self.current_worker.start()
    
    def validate_user_data(self, user_data):
        """Additional validation for user data"""
        # Check for SQL injection patterns (basic check)
        dangerous_patterns = ['--', ';', '/*', '*/', 'xp_', 'sp_', 'exec', 'execute', 'drop', 'delete', 'insert', 'update']
        
        for field, value in user_data.items():
            if isinstance(value, str):
                value_lower = value.lower()
                for pattern in dangerous_patterns:
                    if pattern in value_lower:
                        return {
                            'valid': False,
                            'message': f'Invalid characters detected in {field.replace("_", " ").title()}'
                        }
        
        # Check username format more strictly
        username = user_data.get('username', '')
        if username:
            if username.startswith('_') or username.endswith('_'):
                return {
                    'valid': False,
                    'message': 'Username cannot start or end with underscore'
                }
            
            if '__' in username:
                return {
                    'valid': False,
                    'message': 'Username cannot contain consecutive underscores'
                }
            
            # Reserved usernames
            reserved_usernames = ['admin', 'administrator', 'root', 'system', 'user', 'guest', 'test', 'demo']
            if username.lower() in reserved_usernames:
                return {
                    'valid': False,
                    'message': 'This username is reserved. Please choose another one.'
                }
        
        # Check email domain (basic check)
        email = user_data.get('email', '')
        if email:
            domain = email.split('@')[-1].lower()
            # Add any blocked domains here
            blocked_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
            if domain in blocked_domains:
                return {
                    'valid': False,
                    'message': 'Please use a permanent email address'
                }
        
        # Check name fields for appropriate content (only if provided)
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        
        if first_name and not first_name.replace(' ', '').replace('-', '').replace("'", '').isalpha():
            return {
                'valid': False,
                'message': 'First name should contain only letters, spaces, hyphens, and apostrophes'
            }
        
        if last_name and not last_name.replace(' ', '').replace('-', '').replace("'", '').isalpha():
            return {
                'valid': False,
                'message': 'Last name should contain only letters, spaces, hyphens, and apostrophes'
            }
        
        # Check password strength (only if provided - controller will validate required fields)
        password = user_data.get('password', '')
        if password:
            if len(password) < 8:
                return {
                    'valid': False,
                    'message': 'Password must be at least 8 characters long'
                }
            
            if not any(c.isupper() for c in password):
                return {
                    'valid': False,
                    'message': 'Password must contain at least one uppercase letter'
                }
            
            if not any(c.islower() for c in password):
                return {
                    'valid': False,
                    'message': 'Password must contain at least one lowercase letter'
                }
            
            if not any(c.isdigit() for c in password):
                return {
                    'valid': False,
                    'message': 'Password must contain at least one number'
                }
            
            if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
                return {
                    'valid': False,
                    'message': 'Password must contain at least one special character'
                }
        
        # Check phone number format (optional field)
        phone = user_data.get('phone', '')
        if phone:  # Only validate if phone is provided
            # Remove common separators
            phone_clean = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
            if not phone_clean.isdigit() or len(phone_clean) < 10:
                return {
                    'valid': False,
                    'message': 'Please enter a valid phone number'
                }
        
        selected_type = user_data.get('type', '').lower()
            
        return {'valid': True}
    
    def handle_registration_result(self, result):
        """Handle registration result from worker thread"""
   
        
        # Stop loading state
        self.view.set_loading(False)
        
        if result['success']:
        
            
            # Show success message
            self.view.show_success(result.get('message', 'Registration successful!'))
            
            # Clear form
            self.view.clear_form()
            
            # Get user data from result
            user_data = result.get('user_data', {})
          
            
            # Navigate to start page with user data
           
            self.ui_manager.show_start_page(user_data)
            
        else:
         
            
            # Handle different error types
            error_code = result.get('error_code', 'UNKNOWN_ERROR')
            error_message = result.get('message', 'Registration failed')
            
            if error_code == 'USERNAME_EXISTS':
                self.view.highlight_field('username')
                self.view.show_error('Username already exists. Please choose another one.')
            elif error_code == 'EMAIL_EXISTS':
                self.view.highlight_field('email')
                self.view.show_error('Email already registered. Please use a different email.')
            elif error_code == 'MISSING_FIELD':
                self.view.show_error(error_message)
            elif error_code == 'CREATE_ERROR':
                self.view.show_error('Failed to create user account. Please try again.')
            elif error_code == 'UNEXPECTED_ERROR':
                self.view.show_error('An unexpected error occurred. Please try again later.')
            elif error_code == 'CONNECTION_ERROR':
                self.view.show_error('Connection error. Please check your internet connection and try again.')
            elif error_code == 'VALIDATION_ERROR':
                self.view.show_error(error_message)
            else:
                self.view.show_error(error_message)
    
    def handle_login_request(self):
        """Handle request to switch to login page"""
   
        # Fixed: Call show_login instead of show_start_page
        self.ui_manager.show_login()
    
    def cleanup_worker(self):
        """Clean up worker thread"""
        if self.current_worker:
            self.current_worker.deleteLater()
            self.current_worker = None
    
    def cancel_registration(self):
        """Cancel ongoing registration"""
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.terminate()
            self.current_worker.wait()
            self.cleanup_worker()
            self.view.set_loading(False)
    
    def __del__(self):
        """Cleanup on deletion"""
        self.cancel_registration()
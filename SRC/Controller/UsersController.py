from typing import Dict, Any, Optional
from SRC.DataBase.UsersDBManagement import UsersDBManagement
from SRC.Models.User import User

class UsersController:
    """Controller for managing user operations"""
    
    def __init__(self):
        self.db_manager = UsersDBManagement()
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Basic data validation
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'type']
            for field in required_fields:
                if not user_data.get(field):
                    return {
                        'success': False,
                        'message': f'The field {field} is required',
                        'error_code': 'MISSING_FIELD'
                    }
            
            # Check if the username already exists
            if self.db_manager.get_user_by_username(user_data['username']):
                return {
                    'success': False,
                    'message': 'Username already exists',
                    'error_code': 'USERNAME_EXISTS'
                }
            
            # Check if the email already exists
            if self.db_manager.get_user_by_email(user_data['email']):
                return {
                    'success': False,
                    'message': 'Email already exists in the system',
                    'error_code': 'EMAIL_EXISTS'
                }
            user_type = user_data.get('type', 'Student')
            # Create a new user
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                type=user_type
            )
            
            if self.db_manager.create_user(user, user_data['password']):
                return {
                    'success': True,
                    'message': 'User registered successfully',
                    'user_id': user.id
                }
            else:
                return {
                    'success': False,
                    'message': 'Error creating user',
                    'error_code': 'CREATE_ERROR'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}',
                'error_code': 'UNEXPECTED_ERROR'
            }
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """User login"""
        try:
            if not username or not password:
                return {
                    'success': False,
                    'message': 'Username and password are required',
                    'error_code': 'MISSING_CREDENTIALS'
                }
            
            user = self.db_manager.get_user_by_username(username)
            if not user:
                return {
                    'success': False,
                    'message': 'Invalid username or password',
                    'error_code': 'INVALID_CREDENTIALS'
                }
            
            if not user.is_active:
                return {
                    'success': False,
                    'message': 'User is not active',
                    'error_code': 'USER_INACTIVE'
                }
            
            if self.db_manager.verify_password(username, password):
                return {
                    'success': True,
                    'message': 'Login successful',
                    'user': user.to_dict()
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid username or password',
                    'error_code': 'INVALID_CREDENTIALS'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}',
                'error_code': 'UNEXPECTED_ERROR'
            }
    
    def get_user_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user profile"""
        user = self.db_manager.get_user_by_username(username)
        if user:
            user_dict = user.to_dict()
            # Remove password from returned data
            del user_dict['password_hash']
            return user_dict
        return None
    
    
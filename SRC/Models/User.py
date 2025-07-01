from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """Basic user class"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    first_name: str = ""
    last_name: str = ""
    type: str = ""
    created_at: Optional[datetime] = None
    is_active: bool = True
    
    def __post_init__(self):
        # Set creation time if not provided
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'type': self.type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        user = cls()
        user.id = data.get('id')
        user.username = data.get('username', '')
        user.email = data.get('email', '')
        user.password_hash = data.get('password_hash', '')
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        user.type = data.get('type', 'student')
        user.is_active = data.get('is_active', True)
        
        if data.get('created_at'):
            user.created_at = datetime.fromisoformat(data['created_at'])
        
        return user
    
    def get_full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_user_type(self) -> str:
        """Return the user's type (e.g., 'student' or 'secretary')"""
        return self.type
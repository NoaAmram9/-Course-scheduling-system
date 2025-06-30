import sqlite3
import hashlib
from typing import List, Optional
from SRC.Models.User import User

class UsersDBManagement:
    """Class for managing users in the database"""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create the users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                type TEXT DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Encrypt password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, user: User, password: str) -> bool:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            user.password_hash = self.hash_password(password)
            
            cursor.execute('''
                    INSERT INTO users (username, email, password_hash, first_name, last_name, type, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user.username, user.email, user.password_hash, 
                    user.first_name, user.last_name, user.type, user.is_active))

            
            user.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            return False
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0], username=row[1], email=row[2], password_hash=row[3],
                first_name=row[4], last_name=row[5], is_active=row[7]
            )
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0], username=row[1], email=row[2], password_hash=row[3],
                first_name=row[4], last_name=row[5], is_active=row[7]
            )
        return None
    
    def verify_password(self, username: str, password: str) -> bool:
        """Verify password"""
        user = self.get_user_by_username(username)
        if user:
            return user.password_hash == self.hash_password(password)
        return False
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE is_active = 1')
        rows = cursor.fetchall()
        conn.close()
        
        users = []
        for row in rows:
            users.append(User(
                id=row[0], username=row[1], email=row[2], password_hash=row[3],
                first_name=row[4], last_name=row[5],  type=row[6], is_active=row[8]
            ))

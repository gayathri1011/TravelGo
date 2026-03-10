"""
User model and data structures
"""
from utils.helpers import generate_uuid, get_current_timestamp

class User:
    """User data model"""
    
    def __init__(self, email, name, phone, password_hash):
        """
        Initialize User object
        
        Args:
            email (str): User email
            name (str): User full name
            phone (str): User phone number
            password_hash (str): Hashed password
        """
        self.user_id = generate_uuid()
        self.email = email
        self.name = name
        self.phone = phone
        self.password_hash = password_hash
        self.created_at = get_current_timestamp()
        self.updated_at = get_current_timestamp()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'password_hash': self.password_hash,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create User from dictionary"""
        user = User(
            email=data['email'],
            name=data['name'],
            phone=data['phone'],
            password_hash=data['password_hash']
        )
        user.user_id = data.get('user_id', user.user_id)
        user.created_at = data.get('created_at', user.created_at)
        user.updated_at = data.get('updated_at', user.updated_at)
        return user

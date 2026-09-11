"""
Authentication routes for user registration, login, and session management
"""
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from local_db import LocalDatabase
from helpers import validate_user_data, is_valid_email
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
db = LocalDatabase()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Expected JSON:
    {
        "email": "user@example.com",
        "name": "John Doe",
        "phone": "+1234567890",
        "password": "securepassword"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Validate user data
        is_valid, error_msg = validate_user_data(data)
        if not is_valid:
            return jsonify({'success': False, 'message': error_msg}), 400
        
        email = data.get('email').lower()
        
        # Check if user already exists
        if db.user_exists(email):
            return jsonify({'success': False, 'message': 'Email already registered'}), 409
        
        # Create user
        password_hash = generate_password_hash(data.get('password'))
        if db.create_user(email, data.get('name'), data.get('phone'), password_hash):
            session['user_email'] = email
            session['user_name'] = data.get('name')
            logger.info(f"New user registered: {email}")
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'user': {'email': email, 'name': data.get('name')}
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Registration failed'}), 500
    
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        email = data.get('email').lower()
        password = data.get('password')
        
        # Get user from database
        user = db.get_user(email)
        if not user:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Check password
        if not check_password_hash(user['password_hash'], password):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Set session
        session['user_email'] = email
        session['user_name'] = user['name']
        session.permanent = True
        
        logger.info(f"User logged in: {email}")
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {'email': email, 'name': user['name']}
        }), 200
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout"""
    try:
        email = session.get('user_email', 'Unknown')
        session.clear()
        logger.info(f"User logged out: {email}")
        return jsonify({'success': True, 'message': 'Logout successful'}), 200
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({'success': False, 'message': 'Logout failed'}), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get current user profile"""
    try:
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
        email = session['user_email']
        user = db.get_user(email)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Remove sensitive data
        user.pop('password_hash', None)
        
        return jsonify({'success': True, 'user': user}), 200
    
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    try:
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
        data = request.get_json()
        email = session['user_email']
        
        # Validate updateable fields
        allowed_fields = {'name', 'phone'}
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({'success': False, 'message': 'No valid fields to update'}), 400
        
        if db.update_user(email, **update_data):
            if 'name' in update_data:
                session['user_name'] = update_data['name']
            logger.info(f"User profile updated: {email}")
            return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Update failed'}), 500
    
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

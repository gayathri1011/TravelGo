"""
Admin routes for administrative operations
"""
from flask import Blueprint, render_template, session, jsonify, request
from decorators import admin_required, login_required
from services import BookingService
from validators import Validator, ValidationError
import logging

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Placeholder admin service
class AdminService:
    """Admin service for managing users and bookings"""
    
    def __init__(self, db_client):
        self.db = db_client
        self.logger = logging.getLogger(__name__)
    
    def get_all_users(self):
        """Get all users (admin only)"""
        try:
            # This would fetch from DynamoDB in production
            return {'success': True, 'users': []}
        except Exception as e:
            self.logger.error(f"Error fetching users: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_all_bookings(self, filters=None):
        """Get all bookings with optional filters"""
        try:
            # This would fetch from DynamoDB in production
            return {'success': True, 'bookings': []}
        except Exception as e:
            self.logger.error(f"Error fetching bookings: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_statistics(self):
        """Get system statistics"""
        try:
            stats = {
                'total_users': 0,
                'total_bookings': 0,
                'total_revenue': 0.0,
                'pending_bookings': 0,
                'cancelled_bookings': 0,
                'by_type': {}
            }
            return {'success': True, 'statistics': stats}
        except Exception as e:
            self.logger.error(f"Error calculating statistics: {str(e)}")
            return {'success': False, 'message': str(e)}

# ===== Admin Dashboard Pages =====

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard page"""
    # Check if user is admin
    if not session.get('is_admin', False):
        return render_template('error.html', 
                              error_code=403,
                              error_message='Admin access required'), 403
    
    return render_template('admin_dashboard.html',
                          user_name=session.get('user_name'))

@admin_bp.route('/users')
@login_required
def admin_users():
    """Manage users page"""
    if not session.get('is_admin', False):
        return render_template('error.html',
                              error_code=403,
                              error_message='Admin access required'), 403
    
    return render_template('admin_users.html')

@admin_bp.route('/bookings')
@login_required
def admin_bookings():
    """Manage bookings page"""
    if not session.get('is_admin', False):
        return render_template('error.html',
                              error_code=403,
                              error_message='Admin access required'), 403
    
    return render_template('admin_bookings.html')

# ===== Admin API Endpoints =====

@admin_bp.route('/api/users', methods=['GET'])
@login_required
def get_users():
    """Get all users (admin only)"""
    if not session.get('is_admin', False):
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Fetch users from database
        # This is a placeholder - implement actual DynamoDB query
        users = []
        total = len(users)
        
        return jsonify({
            'success': True,
            'users': users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/bookings', methods=['GET'])
@login_required
def get_bookings():
    """Get all bookings (admin only)"""
    if not session.get('is_admin', False):
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None)
        booking_type = request.args.get('type', None)
        
        # Fetch bookings from database with filters
        # This is a placeholder - implement actual DynamoDB query
        bookings = []
        total = len(bookings)
        
        return jsonify({
            'success': True,
            'bookings': bookings,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/bookings/<booking_id>', methods=['PUT'])
@login_required
def manage_booking(booking_id):
    """Update booking status (admin only)"""
    if not session.get('is_admin', False):
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        data = request.json
        action = data.get('action')
        reason = data.get('reason', '')
        
        if action == 'cancel':
            # Cancel booking
            logger.info(f"Admin {session.get('user_email')} cancelling booking {booking_id}")
            return jsonify({
                'success': True,
                'message': 'Booking cancelled successfully'
            }), 200
        
        elif action == 'confirm':
            # Confirm pending booking
            logger.info(f"Admin {session.get('user_email')} confirming booking {booking_id}")
            return jsonify({
                'success': True,
                'message': 'Booking confirmed successfully'
            }), 200
        
        else:
            return jsonify({'success': False, 'message': 'Invalid action'}), 400
    
    except Exception as e:
        logger.error(f"Error managing booking: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Get system statistics (admin only)"""
    if not session.get('is_admin', False):
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        stats = {
            'total_users': 0,
            'total_bookings': 0,
            'total_revenue': 0.0,
            'pending_bookings': 0,
            'confirmed_bookings': 0,
            'cancelled_bookings': 0,
            'by_type': {
                'Bus': 0,
                'Train': 0,
                'Flight': 0,
                'Hotel': 0
            },
            'by_month': []
        }
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/users/<email>', methods=['GET'])
@login_required
def get_user_details(email):
    """Get specific user details (admin only)"""
    if not session.get('is_admin', False):
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        # Validate email
        Validator.validate_email(email)
        
        # Fetch user details
        user = {
            'email': email,
            'name': '',
            'phone': '',
            'created_at': '',
            'total_bookings': 0,
            'total_spent': 0.0
        }
        
        return jsonify({
            'success': True,
            'user': user
        }), 200
    
    except ValidationError as e:
        return jsonify({'success': False, 'message': e.message}), 400
    except Exception as e:
        logger.error(f"Error fetching user details: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

logger.info("Admin routes registered")

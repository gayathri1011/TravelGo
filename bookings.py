"""
Booking routes for creating, retrieving, and managing bookings
"""
from flask import Blueprint, request, jsonify, session
from aws.local_db import LocalDatabase
from models.booking import Booking
from utils.helpers import validate_booking_data, generate_booking_reference
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')
db = LocalDatabase()

@bookings_bp.route('', methods=['POST'])
def create_booking():
    """
    Create a new booking
    
    Expected JSON:
    {
        "booking_type": "Bus",
        "departure_city": "Hyderabad",
        "arrival_city": "Bangalore",
        "travel_date": "2026-03-15",
        "total_price": 45.00,
        "seats_selected": ["A1", "A2"]
    }
    """
    try:
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
        data = request.get_json()
        
        # Validate booking data
        is_valid, error_msg = validate_booking_data(data)
        if not is_valid:
            return jsonify({'success': False, 'message': error_msg}), 400
        
        email = session['user_email']
        user_name = session.get('user_name', 'Traveler')
        
        # Create booking object
        booking = Booking(
            email=email,
            booking_type=data.get('booking_type'),
            departure_city=data.get('departure_city'),
            arrival_city=data.get('arrival_city'),
            travel_date=data.get('travel_date'),
            total_price=data.get('total_price'),
            user_name=user_name,
            seats_selected=data.get('seats_selected', [])
        )
        
        booking_data = booking.to_dict()
        
        # Save to database
        if db.create_booking(booking_data):
            # Note: SNS notification disabled for local testing
            # Uncomment below when AWS credentials are configured
            # sns.send_booking_confirmation(email, booking_data)
            
            logger.info(f"Booking created: {booking.booking_id}")
            return jsonify({
                'success': True,
                'message': 'Booking confirmed',
                'booking_id': booking.booking_id,
                'booking_reference': booking.booking_reference
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to create booking'}), 500
    
    except Exception as e:
        logger.error(f"Create booking error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@bookings_bp.route('/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get specific booking details"""
    try:
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
        email = session['user_email']
        booking = db.get_booking(booking_id)
        
        if not booking:
            return jsonify({'success': False, 'message': 'Booking not found'}), 404
        
        # Verify booking belongs to user
        if booking.get('email') != email:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        return jsonify({'success': True, 'booking': booking}), 200
    
    except Exception as e:
        logger.error(f"Get booking error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@bookings_bp.route('/my-bookings', methods=['GET'])
def get_my_bookings():
    """Get all bookings for logged-in user"""
    try:
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
        email = session['user_email']
        bookings = db.get_user_bookings(email)
        
        return jsonify({
            'success': True,
            'count': len(bookings),
            'bookings': bookings
        }), 200
    
    except Exception as e:
        logger.error(f"Get bookings error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@bookings_bp.route('/<booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
        email = session['user_email']
        
        # Get booking details first
        booking = db.get_booking(booking_id)
        if not booking:
            return jsonify({'success': False, 'message': 'Booking not found'}), 404
        
        # Verify booking belongs to user
        if booking.get('email') != email:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        if booking.get('status') == 'Cancelled':
            return jsonify({'success': False, 'message': 'Booking already cancelled'}), 400
        
        # Cancel booking
        if db.cancel_booking(booking_id, email):
            # Prepare cancellation data
            booking['cancelled_at'] = datetime.now().isoformat()
            
            # Note: SNS notification disabled for local testing
            # Uncomment below when AWS credentials are configured
            # sns.send_cancellation_alert(email, booking)
            
            logger.info(f"Booking cancelled: {booking_id}")
            return jsonify({
                'success': True,
                'message': 'Booking cancelled successfully'
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to cancel booking'}), 500
    
    except Exception as e:
        logger.error(f"Cancel booking error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@bookings_bp.route('/<booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """Update booking details"""
    try:
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
        email = session['user_email']
        data = request.get_json()
        
        # Get booking to verify ownership
        booking = db.get_booking(booking_id, email)
        if not booking:
            return jsonify({'success': False, 'message': 'Booking not found'}), 404
        
        if booking.get('status') != 'Confirmed':
            return jsonify({'success': False, 'message': 'Cannot update cancelled bookings'}), 400
        
        # Allow updating seats only
        allowed_fields = {'seats_selected'}
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({'success': False, 'message': 'No valid fields to update'}), 400
        
        if db.update_booking(booking_id, email, **update_data):
            logger.info(f"Booking updated: {booking_id}")
            return jsonify({
                'success': True,
                'message': 'Booking updated successfully'
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Update failed'}), 500
    
    except Exception as e:
        logger.error(f"Update booking error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

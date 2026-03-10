"""
Booking service layer for unified booking management
Handles buses, trains, flights, and hotels
"""
import uuid
import logging
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class BookingStatus(Enum):
    """Booking status enumeration"""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class BookingType(Enum):
    """Booking type enumeration"""
    BUS = "Bus"
    TRAIN = "Train"
    FLIGHT = "Flight"
    HOTEL = "Hotel"

class BookingService:
    """
    Unified service for managing all booking types
    Handles booking creation, updates, cancellation, and retrieval
    """
    
    def __init__(self, db_client, sns_client=None):
        """
        Initialize booking service
        
        Args:
            db_client: Database client (DynamoDB)
            sns_client: SNS client for notifications
        """
        self.db = db_client
        self.sns = sns_client
        self.logger = logging.getLogger(__name__)
    
    def create_booking(self, booking_data):
        """
        Create a new booking
        
        Args:
            booking_data: Dictionary containing:
                - user_email: User email
                - booking_type: Bus/Train/Flight/Hotel
                - from_city: Departure city
                - to_city: Arrival city
                - travel_date: Date of travel
                - total_price: Total booking price
                - seats_selected: List of selected seats/rooms
                - passengers: List of passenger info (optional)
        
        Returns:
            Dictionary with booking_id and confirmation details
        """
        try:
            # Generate unique booking ID
            booking_id = f"BK{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
            
            # Prepare booking record
            booking_record = {
                'booking_id': booking_id,
                'user_email': booking_data['user_email'],
                'booking_type': booking_data['booking_type'],
                'from_city': booking_data['from_city'],
                'to_city': booking_data['to_city'],
                'travel_date': booking_data['travel_date'],
                'booking_date': datetime.now().isoformat(),
                'total_price': booking_data['total_price'],
                'seats_selected': booking_data.get('seats_selected', []),
                'status': BookingStatus.CONFIRMED.value,
                'status_code': 200,
                'confirmation_number': str(uuid.uuid4()),
                'passengers': booking_data.get('passengers', []),
                'special_requests': booking_data.get('special_requests', ''),
                'payment_status': 'Completed',
                'cancellation_policy': self._get_cancellation_policy(booking_data['booking_type'])
            }
            
            # Save to database
            self.db.create_booking(booking_record)
            
            # Send confirmation notification
            if self.sns:
                self._send_confirmation_email(booking_data['user_email'], booking_record)
            
            self.logger.info(f"Booking created: {booking_id}")
            
            return {
                'success': True,
                'booking_id': booking_id,
                'confirmation_number': booking_record['confirmation_number'],
                'booking_details': booking_record
            }
        
        except Exception as e:
            self.logger.error(f"Error creating booking: {str(e)}")
            return {
                'success': False,
                'message': 'Failed to create booking',
                'error': str(e)
            }
    
    def get_booking(self, booking_id, user_email=None):
        """
        Retrieve booking details
        
        Args:
            booking_id: Booking ID to retrieve
            user_email: User email for authorization (optional)
        
        Returns:
            Booking record or None if not found
        """
        try:
            booking = self.db.get_booking(booking_id)
            
            if not booking:
                return None
            
            # Check authorization
            if user_email and booking.get('user_email') != user_email:
                self.logger.warning(f"Unauthorized access attempt for booking {booking_id}")
                return None
            
            return booking
        
        except Exception as e:
            self.logger.error(f"Error retrieving booking {booking_id}: {str(e)}")
            return None
    
    def get_user_bookings(self, user_email, status=None, booking_type=None):
        """
        Get all bookings for a user with optional filters
        
        Args:
            user_email: User email
            status: Filter by status (optional)
            booking_type: Filter by booking type (optional)
        
        Returns:
            List of booking records
        """
        try:
            bookings = self.db.get_user_bookings(user_email)
            
            # Apply filters
            if status:
                bookings = [b for b in bookings if b.get('status') == status]
            
            if booking_type:
                bookings = [b for b in bookings if b.get('booking_type') == booking_type]
            
            return bookings
        
        except Exception as e:
            self.logger.error(f"Error retrieving bookings for {user_email}: {str(e)}")
            return []
    
    def cancel_booking(self, booking_id, user_email, reason=''):
        """
        Cancel a booking
        
        Args:
            booking_id: Booking ID to cancel
            user_email: User email for authorization
            reason: Cancellation reason
        
        Returns:
            Dictionary with cancellation details
        """
        try:
            # Get current booking
            booking = self.get_booking(booking_id, user_email)
            
            if not booking:
                return {
                    'success': False,
                    'message': 'Booking not found or not authorized'
                }
            
            # Check if already cancelled
            if booking.get('status') == BookingStatus.CANCELLED.value:
                return {
                    'success': False,
                    'message': 'Booking is already cancelled'
                }
            
            # Check cancellation policy
            if not self._can_cancel_booking(booking):
                return {
                    'success': False,
                    'message': 'Booking cannot be cancelled (too close to travel date)'
                }
            
            # Update booking status
            refund_amount = self._calculate_refund(booking, reason)
            
            booking['status'] = BookingStatus.CANCELLED.value
            booking['cancellation_date'] = datetime.now().isoformat()
            booking['cancellation_reason'] = reason
            booking['refund_amount'] = refund_amount
            
            self.db.update_booking(booking)
            
            # Send cancellation email
            if self.sns:
                self._send_cancellation_email(user_email, booking)
            
            self.logger.info(f"Booking {booking_id} cancelled by {user_email}")
            
            return {
                'success': True,
                'message': 'Booking cancelled successfully',
                'refund_amount': refund_amount,
                'booking': booking
            }
        
        except Exception as e:
            self.logger.error(f"Error cancelling booking {booking_id}: {str(e)}")
            return {
                'success': False,
                'message': 'Failed to cancel booking',
                'error': str(e)
            }
    
    def get_booking_statistics(self, user_email):
        """
        Get booking statistics for a user
        
        Args:
            user_email: User email
        
        Returns:
            Dictionary with booking statistics
        """
        try:
            bookings = self.db.get_user_bookings(user_email)
            
            stats = {
                'total_bookings': len(bookings),
                'confirmed': len([b for b in bookings if b.get('status') == BookingStatus.CONFIRMED.value]),
                'cancelled': len([b for b in bookings if b.get('status') == BookingStatus.CANCELLED.value]),
                'total_spent': sum(float(b.get('total_price', 0)) for b in bookings),
                'by_type': {}
            }
            
            # Count by type
            for booking_type in BookingType:
                count = len([b for b in bookings if b.get('booking_type') == booking_type.value])
                if count > 0:
                    stats['by_type'][booking_type.value] = count
            
            return stats
        
        except Exception as e:
            self.logger.error(f"Error calculating statistics for {user_email}: {str(e)}")
            return {
                'total_bookings': 0,
                'confirmed': 0,
                'cancelled': 0,
                'total_spent': 0,
                'by_type': {}
            }
    
    def _get_cancellation_policy(self, booking_type):
        """Get cancellation policy for booking type"""
        policies = {
            'Bus': 'Full refund if cancelled 24 hours before departure',
            'Train': 'Full refund if cancelled 48 hours before departure',
            'Flight': 'Full refund if cancelled 7 days before departure',
            'Hotel': 'Full refund if cancelled 3 days before check-in'
        }
        return policies.get(booking_type, 'Standard cancellation policy applies')
    
    def _can_cancel_booking(self, booking):
        """Check if booking can be cancelled based on policy"""
        from datetime import datetime, timedelta
        
        travel_date = datetime.strptime(booking.get('travel_date', ''), '%Y-%m-%d')
        current_date = datetime.now()
        days_until = (travel_date - current_date).days
        
        booking_type = booking.get('booking_type')
        min_days = {
            'Bus': 1,
            'Train': 2,
            'Flight': 7,
            'Hotel': 3
        }
        
        required_days = min_days.get(booking_type, 1)
        return days_until >= required_days
    
    def _calculate_refund(self, booking, reason):
        """Calculate refund amount based on cancellation policy"""
        total_price = float(booking.get('total_price', 0))
        
        # Full refund if cancelled within policy window
        if self._can_cancel_booking(booking):
            return total_price
        
        # Partial refund (50%) if cancelled too close to date
        return total_price * 0.5
    
    def _send_confirmation_email(self, email, booking):
        """Send confirmation email via SNS"""
        try:
            message = self._format_confirmation_message(booking)
            subject = f"Booking Confirmation - {booking['booking_id']}"
            # self.sns.publish_email(email, subject, message)
        except Exception as e:
            self.logger.warning(f"Failed to send confirmation email: {str(e)}")
    
    def _send_cancellation_email(self, email, booking):
        """Send cancellation email via SNS"""
        try:
            message = self._format_cancellation_message(booking)
            subject = f"Booking Cancelled - {booking['booking_id']}"
            # self.sns.publish_email(email, subject, message)
        except Exception as e:
            self.logger.warning(f"Failed to send cancellation email: {str(e)}")
    
    def _format_confirmation_message(self, booking):
        """Format confirmation email message"""
        return f"""
        Booking Confirmation
        
        Booking ID: {booking['booking_id']}
        Confirmation #: {booking['confirmation_number']}
        
        From: {booking['from_city']} → To: {booking['to_city']}
        Date: {booking['travel_date']}
        Type: {booking['booking_type']}
        Price: ${booking['total_price']}
        Status: {booking['status']}
        
        Thank you for booking with TravelGo!
        """
    
    def _format_cancellation_message(self, booking):
        """Format cancellation email message"""
        return f"""
        Booking Cancellation Confirmation
        
        Booking ID: {booking['booking_id']}
        Refund Amount: ${booking.get('refund_amount', 0)}
        
        Your booking has been cancelled successfully.
        Refund will be processed within 5-7 business days.
        
        Thank you for using TravelGo!
        """

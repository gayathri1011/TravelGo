"""
Booking model and data structures
"""
from utils.helpers import generate_uuid, generate_booking_reference, get_current_timestamp

class Booking:
    """Booking data model"""
    
    def __init__(self, email, booking_type, departure_city, arrival_city, 
                 travel_date, total_price, user_name, seats_selected=None):
        """
        Initialize Booking object
        
        Args:
            email (str): User email
            booking_type (str): Type of booking (Bus/Train/Flight/Hotel)
            departure_city (str): Departure city
            arrival_city (str): Arrival city
            travel_date (str): Travel date in ISO format
            total_price (float): Total price
            user_name (str): User's name
            seats_selected (list): Selected seats/rooms
        """
        self.booking_id = generate_uuid()
        self.booking_reference = generate_booking_reference()
        self.email = email
        self.booking_type = booking_type
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.travel_date = travel_date
        self.total_price = float(total_price)
        self.user_name = user_name
        self.seats_selected = seats_selected or []
        self.status = 'Confirmed'
        self.created_at = get_current_timestamp()
        self.updated_at = get_current_timestamp()
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'booking_id': self.booking_id,
            'booking_reference': self.booking_reference,
            'email': self.email,
            'booking_type': self.booking_type,
            'departure_city': self.departure_city,
            'arrival_city': self.arrival_city,
            'travel_date': self.travel_date,
            'total_price': self.total_price,
            'user_name': self.user_name,
            'seats_selected': self.seats_selected,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create Booking from dictionary"""
        booking = Booking(
            email=data['email'],
            booking_type=data['booking_type'],
            departure_city=data['departure_city'],
            arrival_city=data['arrival_city'],
            travel_date=data['travel_date'],
            total_price=data['total_price'],
            user_name=data['user_name'],
            seats_selected=data.get('seats_selected', [])
        )
        booking.booking_id = data.get('booking_id', booking.booking_id)
        booking.booking_reference = data.get('booking_reference', booking.booking_reference)
        booking.status = data.get('status', booking.status)
        booking.created_at = data.get('created_at', booking.created_at)
        booking.updated_at = data.get('updated_at', booking.updated_at)
        return booking

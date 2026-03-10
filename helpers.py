"""
Helper functions for TravelGo application
"""
import uuid
from datetime import datetime
import re

def generate_booking_reference():
    """
    Generate unique booking reference
    Format: TG-YYYYMMDD-XXXXXXXX
    """
    date_str = datetime.now().strftime('%Y%m%d')
    unique_str = str(uuid.uuid4())[:8].upper()
    return f"TG-{date_str}-{unique_str}"

def generate_uuid():
    """Generate UUID for booking ID"""
    return str(uuid.uuid4())

def is_valid_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number
        
    Returns:
        bool: True if phone is valid, False otherwise
    """
    pattern = r'^[+]?[0-9]{10,15}$'
    return re.match(pattern, phone) is not None

def format_price(price):
    """
    Format price to 2 decimal places
    
    Args:
        price (float): Price amount
        
    Returns:
        str: Formatted price
    """
    return f"${float(price):.2f}"

def parse_date(date_str):
    """
    Parse date string
    
    Args:
        date_str (str): Date in ISO format (YYYY-MM-DD)
        
    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return None

def get_current_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def validate_booking_data(booking_data):
    """
    Validate booking data
    
    Args:
        booking_data (dict): Booking information
        
    Returns:
        tuple: (bool: is_valid, str: error_message)
    """
    required_fields = ['booking_type', 'departure_city', 'arrival_city', 
                       'travel_date', 'total_price']
    
    for field in required_fields:
        if field not in booking_data or not booking_data[field]:
            return False, f"Missing required field: {field}"
    
    valid_types = ['Bus', 'Train', 'Flight', 'Hotel']
    if booking_data['booking_type'] not in valid_types:
        return False, "Invalid booking type"
    
    try:
        price = float(booking_data['total_price'])
        if price <= 0:
            return False, "Price must be greater than 0"
    except ValueError:
        return False, "Invalid price format"
    
    return True, ""

def validate_user_data(user_data):
    """
    Validate user registration data
    
    Args:
        user_data (dict): User information
        
    Returns:
        tuple: (bool: is_valid, str: error_message)
    """
    required_fields = ['email', 'name', 'phone', 'password']
    
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            return False, f"Missing required field: {field}"
    
    if not is_valid_email(user_data['email']):
        return False, "Invalid email format"
    
    if not is_valid_phone(user_data['phone']):
        return False, "Invalid phone number format"
    
    if len(user_data['password']) < 6:
        return False, "Password must be at least 6 characters long"
    
    return True, ""

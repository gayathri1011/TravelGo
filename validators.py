"""
Input validators for form and API data
"""
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class Validator:
    """Base validator class"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            raise ValidationError('email', 'Email is required')
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError('email', 'Invalid email format')
        
        return True
    
    @staticmethod
    def validate_password(password, min_length=8):
        """
        Validate password strength
        Requirements: min 8 chars, at least one uppercase, one lowercase, one number
        """
        if not password:
            raise ValidationError('password', 'Password is required')
        
        if len(password) < min_length:
            raise ValidationError('password', f'Password must be at least {min_length} characters')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('password', 'Password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('password', 'Password must contain at least one lowercase letter')
        
        if not re.search(r'[0-9]', password):
            raise ValidationError('password', 'Password must contain at least one number')
        
        return True
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        if not phone:
            raise ValidationError('phone', 'Phone number is required')
        
        # Remove common separators
        cleaned = re.sub(r'[\s\-\+\(\)]+', '', phone)
        
        if not re.match(r'^[0-9]{10,15}$', cleaned):
            raise ValidationError('phone', 'Invalid phone number format')
        
        return True
    
    @staticmethod
    def validate_name(name, field_name='name'):
        """Validate name field"""
        if not name:
            raise ValidationError(field_name, f'{field_name.title()} is required')
        
        if len(name.strip()) < 2:
            raise ValidationError(field_name, f'{field_name.title()} must be at least 2 characters')
        
        if len(name) > 100:
            raise ValidationError(field_name, f'{field_name.title()} is too long')
        
        # Allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError(field_name, f'{field_name.title()} contains invalid characters')
        
        return True
    
    @staticmethod
    def validate_city(city):
        """Validate city name"""
        if not city:
            raise ValidationError('city', 'City is required')
        
        if len(city.strip()) < 2:
            raise ValidationError('city', 'City must be at least 2 characters')
        
        if len(city) > 50:
            raise ValidationError('city', 'City name is too long')
        
        return True
    
    @staticmethod
    def validate_date(date_str, must_be_future=True):
        """Validate date format and optionally check if it's in the future"""
        if not date_str:
            raise ValidationError('date', 'Date is required')
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError('date', 'Invalid date format (use YYYY-MM-DD)')
        
        if must_be_future:
            from datetime import date
            if date_obj < date.today():
                raise ValidationError('date', 'Date must be in the future')
        
        return date_obj
    
    @staticmethod
    def validate_price(price):
        """Validate price field"""
        try:
            price_float = float(price)
            if price_float < 0:
                raise ValidationError('price', 'Price cannot be negative')
            return price_float
        except (ValueError, TypeError):
            raise ValidationError('price', 'Invalid price format')
    
    @staticmethod
    def validate_integer(value, field_name, min_val=None, max_val=None):
        """Validate integer field with optional min/max bounds"""
        try:
            int_value = int(value)
            if min_val is not None and int_value < min_val:
                raise ValidationError(field_name, f'{field_name} must be at least {min_val}')
            if max_val is not None and int_value > max_val:
                raise ValidationError(field_name, f'{field_name} cannot exceed {max_val}')
            return int_value
        except (ValueError, TypeError):
            raise ValidationError(field_name, f'Invalid {field_name} format')
    
    @staticmethod
    def validate_enum(value, valid_values, field_name):
        """Validate that value is in allowed enumeration"""
        if value not in valid_values:
            raise ValidationError(field_name, f'{field_name} must be one of: {", ".join(valid_values)}')
        return value


class BookingValidator(Validator):
    """Specific validators for booking data"""
    
    @staticmethod
    def validate_booking_data(data):
        """Validate complete booking data"""
        errors = {}
        
        try:
            Validator.validate_city(data.get('from_city', ''))
        except ValidationError as e:
            errors['from_city'] = e.message
        
        try:
            Validator.validate_city(data.get('to_city', ''))
        except ValidationError as e:
            errors['to_city'] = e.message
        
        try:
            Validator.validate_date(data.get('travel_date', ''))
        except ValidationError as e:
            errors['travel_date'] = e.message
        
        try:
            Validator.validate_enum(
                data.get('booking_type', ''),
                ['Bus', 'Train', 'Flight', 'Hotel'],
                'booking_type'
            )
        except ValidationError as e:
            errors['booking_type'] = e.message
        
        return errors if errors else None


class SearchValidator(Validator):
    """Validators for search parameters"""
    
    @staticmethod
    def validate_search_params(params):
        """Validate search parameters"""
        errors = {}
        
        try:
            Validator.validate_city(params.get('from', ''))
        except ValidationError as e:
            errors['from'] = e.message
        
        try:
            Validator.validate_city(params.get('to', ''))
        except ValidationError as e:
            errors['to'] = e.message
        
        try:
            Validator.validate_date(params.get('date', ''))
        except ValidationError as e:
            errors['date'] = e.message
        
        try:
            Validator.validate_enum(
                params.get('mode', ''),
                ['Bus', 'Train', 'Flight', 'Hotel'],
                'mode'
            )
        except ValidationError as e:
            errors['mode'] = e.message
        
        return errors if errors else None

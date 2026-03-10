"""
DynamoDB client for interacting with AWS DynamoDB tables
Handles user and booking operations
"""
import boto3
from config import Config
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class DynamoDBClient:
    """AWS DynamoDB operations for TravelGo"""
    
    def __init__(self):
        """Initialize DynamoDB client"""
        try:
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=Config.AWS_REGION,
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
            )
            self.users_table = self.dynamodb.Table(Config.USERS_TABLE)
            self.bookings_table = self.dynamodb.Table(Config.BOOKINGS_TABLE)
            logger.info("DynamoDB client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing DynamoDB client: {e}")
            raise
    
    # ===== User Operations =====
    def create_user(self, email, name, phone, password_hash):
        """
        Create a new user in DynamoDB
        
        Args:
            email (str): User email
            name (str): User full name
            phone (str): User phone number
            password_hash (str): Hashed password
            
        Returns:
            bool: True if user created successfully, False otherwise
        """
        try:
            user_id = str(uuid.uuid4())
            self.users_table.put_item(
                Item={
                    'email': email,
                    'user_id': user_id,
                    'name': name,
                    'phone': phone,
                    'password_hash': password_hash,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
            )
            logger.info(f"User created successfully: {email}")
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def get_user(self, email):
        """
        Retrieve user by email
        
        Args:
            email (str): User email
            
        Returns:
            dict: User data if found, None otherwise
        """
        try:
            response = self.users_table.get_item(Key={'email': email})
            user = response.get('Item')
            if user:
                logger.info(f"User retrieved: {email}")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return None
    
    def user_exists(self, email):
        """
        Check if user exists
        
        Args:
            email (str): User email
            
        Returns:
            bool: True if user exists, False otherwise
        """
        return self.get_user(email) is not None
    
    def update_user(self, email, **kwargs):
        """
        Update user information
        
        Args:
            email (str): User email
            **kwargs: Fields to update
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            update_expr = "SET "
            expr_attrs = {}
            expr_names = {}
            
            for idx, (key, value) in enumerate(kwargs.items()):
                if idx > 0:
                    update_expr += ", "
                update_expr += f"#{key} = :{key}"
                expr_names[f"#{key}"] = key
                expr_attrs[f":{key}"] = value
            
            update_expr += ", updated_at = :timestamp"
            expr_attrs[":timestamp"] = datetime.now().isoformat()
            
            self.users_table.update_item(
                Key={'email': email},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_attrs
            )
            logger.info(f"User updated: {email}")
            return True
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
    
    # ===== Booking Operations =====
    def create_booking(self, booking_data):
        """
        Create a new booking
        
        Args:
            booking_data (dict): Booking information
            
        Returns:
            bool: True if booking created successfully, False otherwise
        """
        try:
            booking_data['created_at'] = datetime.now().isoformat()
            booking_data['updated_at'] = datetime.now().isoformat()
            self.bookings_table.put_item(Item=booking_data)
            logger.info(f"Booking created: {booking_data.get('booking_id')}")
            return True
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            return False
    
    def get_booking(self, booking_id, email):
        """
        Get a specific booking by ID and email
        
        Args:
            booking_id (str): Booking ID
            email (str): User email
            
        Returns:
            dict: Booking data if found, None otherwise
        """
        try:
            response = self.bookings_table.get_item(
                Key={'booking_id': booking_id, 'email': email}
            )
            return response.get('Item')
        except Exception as e:
            logger.error(f"Error retrieving booking: {e}")
            return None
    
    def get_user_bookings(self, email):
        """
        Get all bookings for a specific user
        
        Args:
            email (str): User email
            
        Returns:
            list: List of bookings
        """
        try:
            response = self.bookings_table.query(
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            bookings = response.get('Items', [])
            logger.info(f"Retrieved {len(bookings)} bookings for user: {email}")
            return bookings
        except Exception as e:
            logger.error(f"Error retrieving bookings: {e}")
            return []
    
    def cancel_booking(self, booking_id, email):
        """
        Cancel a booking by updating status
        
        Args:
            booking_id (str): Booking ID
            email (str): User email
            
        Returns:
            bool: True if cancellation successful, False otherwise
        """
        try:
            self.bookings_table.update_item(
                Key={'booking_id': booking_id, 'email': email},
                UpdateExpression='SET #status = :status, updated_at = :timestamp',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': 'Cancelled',
                    ':timestamp': datetime.now().isoformat()
                }
            )
            logger.info(f"Booking cancelled: {booking_id}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling booking: {e}")
            return False
    
    def update_booking(self, booking_id, email, **kwargs):
        """
        Update booking details
        
        Args:
            booking_id (str): Booking ID
            email (str): User email
            **kwargs: Fields to update
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            update_expr = "SET "
            expr_attrs = {}
            expr_names = {}
            
            for idx, (key, value) in enumerate(kwargs.items()):
                if idx > 0:
                    update_expr += ", "
                update_expr += f"#{key} = :{key}"
                expr_names[f"#{key}"] = key
                expr_attrs[f":{key}"] = value
            
            update_expr += ", updated_at = :timestamp"
            expr_attrs[":timestamp"] = datetime.now().isoformat()
            
            self.bookings_table.update_item(
                Key={'booking_id': booking_id, 'email': email},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_attrs
            )
            logger.info(f"Booking updated: {booking_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating booking: {e}")
            return False

"""
SNS client for sending email notifications via AWS Simple Notification Service
Handles booking confirmations and cancellation alerts
"""
import boto3
from config import Config
import logging

logger = logging.getLogger(__name__)

class SNSClient:
    """AWS SNS operations for TravelGo notifications"""
    
    def __init__(self):
        """Initialize SNS client"""
        try:
            self.sns = boto3.client(
                'sns',
                region_name=Config.AWS_REGION,
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
            )
            self.topic_arn = Config.SNS_TOPIC_ARN
            logger.info("SNS client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing SNS client: {e}")
            raise
    
    def send_booking_confirmation(self, email, booking_data):
        """
        Send booking confirmation email via SNS
        
        Args:
            email (str): User email address
            booking_data (dict): Booking details
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            message = self._format_booking_confirmation(booking_data)
            
            self.sns.publish(
                TopicArn=self.topic_arn,
                Subject='✅ TravelGo Booking Confirmation',
                Message=message
            )
            logger.info(f"Booking confirmation sent to: {email}")
            return True
        except Exception as e:
            logger.error(f"Error sending booking confirmation: {e}")
            return False
    
    def send_cancellation_alert(self, email, booking_data):
        """
        Send booking cancellation alert email
        
        Args:
            email (str): User email address
            booking_data (dict): Booking details
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            message = self._format_cancellation_alert(booking_data)
            
            self.sns.publish(
                TopicArn=self.topic_arn,
                Subject='❌ TravelGo Booking Cancelled',
                Message=message
            )
            logger.info(f"Cancellation alert sent to: {email}")
            return True
        except Exception as e:
            logger.error(f"Error sending cancellation alert: {e}")
            return False
    
    def send_admin_notification(self, subject, message):
        """
        Send admin notification
        
        Args:
            subject (str): Email subject
            message (str): Email message
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            self.sns.publish(
                TopicArn=self.topic_arn,
                Subject=f"[ADMIN] {subject}",
                Message=message
            )
            logger.info("Admin notification sent")
            return True
        except Exception as e:
            logger.error(f"Error sending admin notification: {e}")
            return False
    
    @staticmethod
    def _format_booking_confirmation(booking_data):
        """Format booking confirmation message"""
        message = f"""
================================
    TravelGo Booking Confirmation
================================

Dear {booking_data.get('user_name', 'Traveler')},

Your booking has been confirmed! Here are your booking details:

Booking Reference: {booking_data.get('booking_reference')}
Booking Type: {booking_data.get('booking_type')}

Route Information:
  From: {booking_data.get('departure_city')}
  To: {booking_data.get('arrival_city')}
  Date: {booking_data.get('travel_date')}

Price Details:
  Total Amount: ${booking_data.get('total_price', 0):.2f}

Status: {booking_data.get('status', 'Confirmed')}

Important Information:
- Please arrive at least 2 hours before departure for flights
- Keep your booking reference for check-in
- You can cancel your booking from the dashboard anytime

Thank you for choosing TravelGo!
For support, visit: https://travelgo.example.com/support

Best regards,
TravelGo Team
================================
"""
        return message
    
    @staticmethod
    def _format_cancellation_alert(booking_data):
        """Format cancellation alert message"""
        message = f"""
================================
    TravelGo Booking Cancelled
================================

Dear {booking_data.get('user_name', 'Traveler')},

Your booking has been successfully cancelled.

Booking Reference: {booking_data.get('booking_reference')}
Booking Type: {booking_data.get('booking_type')}

Route Information:
  From: {booking_data.get('departure_city')}
  To: {booking_data.get('arrival_city')}
  Original Date: {booking_data.get('travel_date')}

Refund Information:
- Refund Amount: ${booking_data.get('total_price', 0):.2f}
- Refund Status: Processing (usually within 5-7 business days)
- Refund Method: Original payment method

Cancellation Date: {booking_data.get('cancelled_at', 'N/A')}

If you have any questions about your refund, please contact our support team.

Thank you for using TravelGo!
For support, visit: https://travelgo.example.com/support

Best regards,
TravelGo Team
================================
"""
        return message

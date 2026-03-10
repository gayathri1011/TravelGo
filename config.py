import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base Flask configuration settings"""
    # Flask core
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # DynamoDB Tables
    DYNAMODB_USERS_TABLE = os.getenv('DYNAMODB_USERS_TABLE', 'TravelGo_Users')
    DYNAMODB_BOOKINGS_TABLE = os.getenv('DYNAMODB_BOOKINGS_TABLE', 'TravelGo_Bookings')
    DYNAMODB_VEHICLES_TABLE = os.getenv('DYNAMODB_VEHICLES_TABLE', 'TravelGo_Vehicles')
    
    # SNS Configuration
    SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')
    SNS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    # Security
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    BCRYPT_LOG_ROUNDS = 12
    
    # Email
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'noreply@travelgo.com')
    APP_NAME = os.getenv('APP_NAME', 'TravelGo')
    APP_VERSION = os.getenv('APP_VERSION', '2.0.0')
    
    # Admin
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@travelgo.com')
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

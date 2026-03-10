"""
Error handling and response utilities
"""
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base application error"""
    def __init__(self, message, status_code=500, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
    
    def to_dict(self):
        """Convert error to dictionary"""
        rv = dict(self.payload)
        rv['message'] = self.message
        rv['success'] = False
        return rv

class ValidationError(AppError):
    """Validation error"""
    def __init__(self, message, field=None):
        super().__init__(message, status_code=400)
        self.field = field

class AuthenticationError(AppError):
    """Authentication error"""
    def __init__(self, message='Authentication failed'):
        super().__init__(message, status_code=401)

class AuthorizationError(AppError):
    """Authorization error"""
    def __init__(self, message='Access denied'):
        super().__init__(message, status_code=403)

class NotFoundError(AppError):
    """Resource not found error"""
    def __init__(self, resource='Resource'):
        super().__init__(f'{resource} not found', status_code=404)

class ConflictError(AppError):
    """Conflict error (e.g., duplicate resource)"""
    def __init__(self, message='Resource already exists'):
        super().__init__(message, status_code=409)

class ServiceError(AppError):
    """External service error"""
    def __init__(self, message='External service error'):
        super().__init__(message, status_code=503)

def success_response(data=None, message='Success', status_code=200):
    """Create a success JSON response"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(error, status_code=None):
    """Create an error JSON response"""
    if isinstance(error, AppError):
        logger.error(f"App Error: {error.message}")
        return jsonify(error.to_dict()), error.status_code
    else:
        logger.error(f"Unexpected Error: {str(error)}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred',
            'error': str(error)
        }), status_code or 500

def paginated_response(items, page, per_page, total):
    """Create a paginated JSON response"""
    return jsonify({
        'success': True,
        'data': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }), 200

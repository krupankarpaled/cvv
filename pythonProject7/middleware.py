"""Security and performance middleware for the application."""
import logging
from functools import wraps
from flask import request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge

logger = logging.getLogger(__name__)


def add_security_headers(response):
    """Add security headers to response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; "
        "img-src 'self' data: blob:; "
        "media-src 'self' blob:; "
        "connect-src 'self';"
    )
    return response


def validate_content_type(f):
    """Validate request content type for POST/PUT requests."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Content-Type must be application/json'
                }), 415
        return f(*args, **kwargs)
    return decorated_function


def sanitize_input(data):
    """Sanitize user input to prevent XSS and injection attacks."""
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '`', '|', '*']
        sanitized = data
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    return data


class SecurityMiddleware:
    """Security middleware for request validation."""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        """Process request through security checks."""
        # Add security headers to all responses
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('X-Content-Type-Options', 'nosniff'))
            headers.append(('X-Frame-Options', 'DENY'))
            headers.append(('X-XSS-Protection', '1; mode=block'))
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response)

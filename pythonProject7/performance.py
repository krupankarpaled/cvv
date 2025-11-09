"""Performance optimization utilities."""
import time
import logging
from functools import wraps
from flask import request, g

logger = logging.getLogger(__name__)


def measure_performance(f):
    """Decorator to measure endpoint performance."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        logger.info(
            f"Performance: {request.method} {request.path} "
            f"completed in {duration:.2f}ms"
        )
        return result
    return decorated_function


def cache_response(timeout=300):
    """Simple in-memory cache decorator (use Redis for production)."""
    cache = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{request.path}:{str(request.args)}"
            
            if cache_key in cache:
                cached_data, cached_time = cache[cache_key]
                if time.time() - cached_time < timeout:
                    logger.debug(f"Cache hit: {cache_key}")
                    return cached_data
            
            result = f(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            logger.debug(f"Cache miss: {cache_key}")
            return result
        return decorated_function
    return decorator


def before_request_handler():
    """Handler for before each request."""
    g.start_time = time.time()


def after_request_handler(response):
    """Handler for after each request."""
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        response.headers['X-Response-Time'] = f"{elapsed * 1000:.2f}ms"
    return response


def optimize_image_size(image_data, max_size=(1920, 1080)):
    """Optimize image size for processing."""
    from PIL import Image
    from io import BytesIO
    import base64
    
    try:
        # Decode base64
        img_data = base64.b64decode(image_data.split(',')[1])
        img = Image.open(BytesIO(img_data))
        
        # Resize if too large
        if img.width > max_size[0] or img.height > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Re-encode
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            optimized = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/jpeg;base64,{optimized}"
        
        return image_data
    except Exception as e:
        logger.error(f"Image optimization error: {str(e)}")
        return image_data

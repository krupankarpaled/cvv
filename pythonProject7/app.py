"""Production-ready Color Detector Application."""
import os
import sys
import logging
import uuid
from datetime import datetime

from flask import Flask, render_template, session, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config
from models import db
from routes import api
from middleware import add_security_headers
from performance import before_request_handler, after_request_handler

# Initialize Flask app
app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'production')
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
CORS(app, origins=app.config['CORS_ORIGINS'])
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[f"{app.config['RATE_LIMIT_PER_MINUTE']}/minute"]
)

# Register blueprints
app.register_blueprint(api)

# Register middleware
app.before_request(before_request_handler)
app.after_request(after_request_handler)
app.after_request(add_security_headers)

# Configure logging
logging.basicConfig(
    level=getattr(logging, app.config['LOG_LEVEL']),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(app.config['LOG_FILE']),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create database tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")


@app.before_request
def ensure_session():
    """Ensure user has a session ID."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        logger.info(f"New session created: {session['session_id']}")


@app.route('/')
def index():
    """Render main page."""
    return render_template('index_enhanced.html')


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0.0'
    })


@app.route('/api/info')
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'Color Detector API',
        'version': '2.0.0',
        'endpoints': {
            'POST /api/detect': 'Detect color from image',
            'GET /api/history': 'Get color history',
            'DELETE /api/history/<id>': 'Delete history item',
            'DELETE /api/history/clear': 'Clear all history',
            'POST /api/analyze': 'Analyze color by hex code',
            'GET /api/palettes': 'Get saved palettes',
            'POST /api/palettes': 'Create new palette',
            'PUT /api/palettes/<id>': 'Update palette',
            'DELETE /api/palettes/<id>': 'Delete palette'
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limit errors."""
    return jsonify({
        'success': False,
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.'
    }), 429


if __name__ == '__main__':
    port = app.config['PORT']
    debug = app.config['DEBUG']
    logger.info(f"Starting Color Detector App on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)

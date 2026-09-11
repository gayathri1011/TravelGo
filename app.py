"""
Main Flask application for TravelGo
"""

from flask import Flask, render_template, session, redirect, url_for
from config import DevelopmentConfig, ProductionConfig
import os
import logging
from datetime import timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')

if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Session configuration
# Using Flask's built-in signed-cookie sessions.
# This works better with Vercel's serverless environment.
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# Register blueprints
from auth import auth_bp
from bookings import bookings_bp
from search import search_bp

app.register_blueprint(auth_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(search_bp)


# ===== Template Routes =====

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/register')
def register_page():
    """Registration page"""
    if 'user_email' in session:
        return redirect(url_for('dashboard_page'))

    return render_template('register.html')


@app.route('/login')
def login_page():
    """Login page"""
    if 'user_email' in session:
        return redirect(url_for('dashboard_page'))

    return render_template('login.html')


@app.route('/search')
def search_page():
    """Search page"""
    if 'user_email' not in session:
        return redirect(url_for('login_page'))

    return render_template('search.html')


@app.route('/dashboard')
def dashboard_page():
    """Dashboard page"""
    if 'user_email' not in session:
        return redirect(url_for('login_page'))

    return render_template(
        'dashboard.html',
        user_name=session.get('user_name', 'Traveler'),
        user_email=session.get('user_email')
    )


@app.route('/booking/<booking_id>')
def booking_details_page(booking_id):
    """Booking details page"""
    if 'user_email' not in session:
        return redirect(url_for('login_page'))

    return render_template(
        'booking_details.html',
        booking_id=booking_id
    )


# ===== Error Handlers =====

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template(
        'error.html',
        error_code=404,
        error_message='Page not found'
    ), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")

    return render_template(
        'error.html',
        error_code=500,
        error_message='Internal server error'
    ), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return render_template(
        'error.html',
        error_code=403,
        error_message='Access forbidden'
    ), 403


# ===== Context Processors =====

@app.context_processor
def inject_user():
    """Inject user info into all templates"""
    return {
        'user_email': session.get('user_email'),
        'user_name': session.get('user_name')
    }


# ===== Health Check =====

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'TravelGo API'
    }, 200


# ===== Run Application =====

if __name__ == '__main__':
    logger.info("Starting TravelGo Flask Application")

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
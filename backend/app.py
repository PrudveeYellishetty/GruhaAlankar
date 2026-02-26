"""Flask application entry point."""
from flask import Flask
from flask_cors import CORS
from config.settings import Config
from services.supabase_service import SupabaseService
from routes import furniture_bp, ai_bp
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, origins=Config.ALLOWED_ORIGINS)
    
    # Initialize Supabase
    try:
        SupabaseService.initialize(
            supabase_url=Config.SUPABASE_URL,
            supabase_key=Config.SUPABASE_SERVICE_ROLE_KEY
        )
        logger.info("Supabase initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}")
        logger.warning("Running without Supabase - some features will not work")
    
    # Register blueprints
    app.register_blueprint(furniture_bp)
    app.register_blueprint(ai_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'GruhaAlankar API',
            'version': '1.0.0',
            'status': 'running',
            'database': 'Supabase PostgreSQL',
            'endpoints': {
                'furniture_list': '/api/furniture',
                'furniture_detail': '/api/furniture/<id>',
                'analyze_room': '/api/analyze-room',
                'redesign_room': '/api/redesign',
                'health': '/api/health'
            }
        }
    
    logger.info("Flask application created successfully")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )

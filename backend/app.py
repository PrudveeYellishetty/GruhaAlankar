"""Flask application entry point — serves API + React frontend."""
from flask import Flask, send_from_directory
from flask_cors import CORS
from config.settings import Config
from services.data_service import DataService
from routes import furniture_bp, ai_bp, assets_bp
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Frontend build directory
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'static', 'frontend')


def create_app():
    """Application factory pattern."""
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB upload limit

    # Enable CORS (for Flutter app and any external access)
    CORS(app, origins=Config.ALLOWED_ORIGINS)

    # Initialize local data service
    DataService.initialize()

    # Register API blueprints
    app.register_blueprint(furniture_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(assets_bp)

    # Health check
    @app.route('/api/health')
    def health():
        return {
            'service': 'GruhaAlankar API',
            'status': 'healthy',
            'success': True,
            'furniture_count': len(DataService.get_furniture_list())
        }

    # ---- Serve React Frontend ----
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        """Serve React app — API routes handled by blueprints above."""
        if path and os.path.exists(os.path.join(FRONTEND_DIR, path)):
            return send_from_directory(FRONTEND_DIR, path)
        return send_from_directory(FRONTEND_DIR, 'index.html')

    logger.info("Flask application created successfully")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)

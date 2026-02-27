"""API routes package."""

from .furniture_routes import furniture_bp
from .ai_routes import ai_bp
from .asset_routes import assets_bp

__all__ = ['furniture_bp', 'ai_bp', 'assets_bp']

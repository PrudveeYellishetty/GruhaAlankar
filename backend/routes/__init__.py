"""API routes package."""

from .furniture_routes import furniture_bp
from .ai_routes import ai_bp
from .asset_routes import assets_bp
from .room_analysis_routes import room_analysis_bp

__all__ = ['furniture_bp', 'ai_bp', 'assets_bp', 'room_analysis_bp']

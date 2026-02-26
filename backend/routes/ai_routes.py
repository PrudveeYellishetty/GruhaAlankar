"""AI-powered room analysis and redesign endpoints."""
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from services.supabase_service import SupabaseService
from services.ai_service import AIService
from config.settings import Config
import os
import logging
import uuid

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__, url_prefix='/api')


@ai_bp.route('/analyze-room', methods=['POST'])
def analyze_room():
    """
    POST /api/analyze-room
    
    Multipart form data:
        - image: Room image file
    
    Returns:
        Unified JSON response with AI recommendations mapped to asset IDs
        {
            "mode": "recommendation",
            "assets": [
                {
                    "asset_id": "sofa_001",
                    "color": "#808080",
                    "reason": "...",
                    "confidence": 0.85
                }
            ],
            "generated_images": [],
            "analysis": {...}
        }
    """
    try:
        # Validate file upload
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Empty filename'
            }), 400
        
        if not Config.allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Allowed: png, jpg, jpeg, webp'
            }), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = os.path.join(
            current_app.root_path, 
            Config.UPLOAD_FOLDER
        )
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Initialize AI service
        ai_service = AIService(
            api_key=Config.OPENAI_API_KEY,
            provider='openai'
        )
        
        # Analyze room
        analysis = ai_service.analyze_room(file_path)
        
        # Get all available furniture
        available_furniture = SupabaseService.get_furniture_list()
        
        # Map AI recommendations to actual asset IDs
        mapped_assets = ai_service.map_recommendations_to_assets(
            recommendations=analysis.get('recommendations', []),
            available_furniture=available_furniture
        )
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        # Return unified response
        return jsonify({
            'success': True,
            'mode': 'recommendation',
            'assets': mapped_assets,
            'generated_images': [],
            'analysis': {
                'room_type': analysis.get('room_type'),
                'style': analysis.get('style'),
                'color_scheme': analysis.get('color_scheme'),
                'empty_spaces': analysis.get('empty_spaces'),
                'confidence': analysis.get('confidence')
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error in analyze_room: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/redesign', methods=['POST'])
def redesign_room():
    """
    POST /api/redesign
    
    Multipart form data:
        - image: Room image file
        - style: Preferred style (optional, default: 'modern')
        - color_scheme: Preferred colors (optional, default: 'neutral')
        - furniture_focus: Focus area (optional, default: 'overall ambiance')
    
    Returns:
        Unified JSON response with generated images
        {
            "mode": "redesign",
            "assets": [...],
            "generated_images": ["url1", "url2"],
            "style": "modern",
            "prompt_used": "..."
        }
    """
    try:
        # Validate file upload
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '' or not Config.allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file'
            }), 400
        
        # Get preferences
        preferences = {
            'style': request.form.get('style', 'modern'),
            'color_scheme': request.form.get('color_scheme', 'neutral'),
            'furniture_focus': request.form.get('furniture_focus', 'overall ambiance')
        }
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = os.path.join(
            current_app.root_path,
            Config.UPLOAD_FOLDER
        )
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Initialize AI service
        ai_service = AIService(
            api_key=Config.OPENAI_API_KEY,
            provider='openai'
        )
        
        # Generate redesign
        redesign_result = ai_service.redesign_room(file_path, preferences)
        
        # Optionally analyze the redesigned image to suggest matching furniture
        # For MVP, we can skip this and let users browse manually
        
        # Clean up
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'mode': 'redesign',
            'assets': redesign_result.get('furniture_suggestions', []),
            'generated_images': redesign_result.get('generated_images', []),
            'style': redesign_result.get('style'),
            'prompt_used': redesign_result.get('prompt_used')
        }), 200
    
    except Exception as e:
        logger.error(f"Error in redesign_room: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'GruhaAlankar API'
    }), 200

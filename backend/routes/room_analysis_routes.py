"""Routes for room analysis and AI recommendations."""
import logging
from flask import Blueprint, request, jsonify
from services.room_analysis_service import RoomAnalysisService
from services.data_service import DataService

logger = logging.getLogger(__name__)

room_analysis_bp = Blueprint('room_analysis', __name__)


@room_analysis_bp.route('/analyze-room', methods=['POST'])
def analyze_room():
    """
    Analyze a room image and get furniture recommendations.
    Expects multipart/form-data with 'image' file.
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, webp'}), 400
        
        # Read image data
        image_data = file.read()
        
        # Validate file size (max 10MB)
        if len(image_data) > 10 * 1024 * 1024:
            return jsonify({'error': 'File too large. Maximum size: 10MB'}), 400
        
        logger.info(f"Analyzing room image: {file.filename} ({len(image_data)} bytes)")
        
        # Analyze the room
        room_analysis = RoomAnalysisService.analyze_room_image(image_data)
        
        # Get furniture catalog
        furniture_catalog = DataService.get_furniture_list()
        
        # Match furniture
        matched_furniture = RoomAnalysisService.match_furniture(
            room_analysis, 
            furniture_catalog
        )
        
        # Generate detailed recommendations
        recommendations = RoomAnalysisService.generate_detailed_recommendations(
            room_analysis,
            matched_furniture
        )
        
        response_data = {
            'success': True,
            'analysis': room_analysis,
            'recommendations': recommendations,
            'furniture': matched_furniture
        }
        
        logger.info(f"Room analysis complete: {len(matched_furniture)} recommendations")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Room analysis error: {e}", exc_info=True)
        return jsonify({
            'error': 'Failed to analyze room',
            'message': str(e)
        }), 500


@room_analysis_bp.route('/analyze-room/test', methods=['GET'])
def test_analysis():
    """Test endpoint to verify the service is working."""
    try:
        furniture_count = len(DataService.get_furniture_list())
        return jsonify({
            'success': True,
            'message': 'Room analysis service is ready',
            'furniture_items': furniture_count
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

"""Furniture API endpoints."""
from flask import Blueprint, jsonify, request
from services.supabase_service import SupabaseService
import logging

logger = logging.getLogger(__name__)

furniture_bp = Blueprint('furniture', __name__, url_prefix='/api/furniture')


@furniture_bp.route('', methods=['GET'])
def get_furniture_list():
    """
    GET /api/furniture
    Query params:
        - category: Filter by category (optional)
        - style: Filter by style (optional)
    
    Returns:
        JSON list of furniture items
    """
    try:
        category = request.args.get('category')
        style = request.args.get('style')
        
        furniture_list = SupabaseService.get_furniture_list(
            category=category,
            style=style
        )
        
        return jsonify({
            'success': True,
            'count': len(furniture_list),
            'data': furniture_list
        }), 200
    
    except Exception as e:
        logger.error(f"Error in get_furniture_list: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@furniture_bp.route('/<furniture_id>', methods=['GET'])
def get_furniture_detail(furniture_id):
    """
    GET /api/furniture/<id>
    
    Returns:
        JSON object with furniture details
    """
    try:
        furniture = SupabaseService.get_furniture_by_id(furniture_id)
        
        if furniture:
            return jsonify({
                'success': True,
                'data': furniture
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Furniture not found'
            }), 404
    
    except Exception as e:
        logger.error(f"Error in get_furniture_detail: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@furniture_bp.route('/batch', methods=['POST'])
def get_furniture_batch():
    """
    POST /api/furniture/batch
    Body:
        {
            "ids": ["sofa_001", "table_002"]
        }
    
    Returns:
        JSON list of furniture items matching the IDs
    """
    try:
        data = request.get_json()
        furniture_ids = data.get('ids', [])
        
        if not furniture_ids:
            return jsonify({
                'success': False,
                'error': 'No furniture IDs provided'
            }), 400
        
        furniture_list = SupabaseService.get_furniture_by_ids(furniture_ids)
        
        return jsonify({
            'success': True,
            'count': len(furniture_list),
            'data': furniture_list
        }), 200
    
    except Exception as e:
        logger.error(f"Error in get_furniture_batch: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

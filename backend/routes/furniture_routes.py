"""Furniture API endpoints — uses local DataService."""
from flask import Blueprint, jsonify, request
from services.data_service import DataService
import logging

logger = logging.getLogger(__name__)

furniture_bp = Blueprint('furniture', __name__, url_prefix='/api/furniture')


@furniture_bp.route('', methods=['GET'])
def get_furniture_list():
    """GET /api/furniture — list all furniture with optional filtering."""
    category = request.args.get('category')
    style = request.args.get('style')

    furniture_list = DataService.get_furniture_list(category=category, style=style)

    return jsonify({
        'success': True, 'count': len(furniture_list), 'data': furniture_list
    }), 200


@furniture_bp.route('/<furniture_id>', methods=['GET'])
def get_furniture_detail(furniture_id):
    """GET /api/furniture/<id> — single furniture details."""
    furniture = DataService.get_furniture_by_id(furniture_id)

    if furniture:
        return jsonify({'success': True, 'data': furniture}), 200
    else:
        return jsonify({'success': False, 'error': 'Furniture not found'}), 404


@furniture_bp.route('/batch', methods=['POST'])
def get_furniture_batch():
    """POST /api/furniture/batch — batch lookup by IDs."""
    data = request.get_json()
    furniture_ids = data.get('ids', [])

    if not furniture_ids:
        return jsonify({'success': False, 'error': 'No furniture IDs provided'}), 400

    furniture_list = DataService.get_furniture_by_ids(furniture_ids)

    return jsonify({
        'success': True, 'count': len(furniture_list), 'data': furniture_list
    }), 200

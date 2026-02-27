"""Static asset management routes - serves 3D models locally."""
from flask import Blueprint, jsonify, request, current_app, send_from_directory
import os
import logging

logger = logging.getLogger(__name__)

assets_bp = Blueprint('assets', __name__, url_prefix='/api/assets')

ALLOWED_MODEL_EXTENSIONS = {'.glb', '.gltf'}
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


@assets_bp.route('/models', methods=['GET'])
def list_models():
    """List all locally stored 3D models."""
    static_dir = current_app.static_folder
    models_dir = os.path.join(static_dir, 'models')
    
    if not os.path.exists(models_dir):
        return jsonify({'success': True, 'data': [], 'count': 0})
    
    models = []
    for root, dirs, files in os.walk(models_dir):
        for f in files:
            if os.path.splitext(f)[1].lower() in ALLOWED_MODEL_EXTENSIONS:
                rel_path = os.path.relpath(os.path.join(root, f), static_dir)
                models.append({
                    'filename': f,
                    'path': f'/static/{rel_path}',
                    'size_mb': round(os.path.getsize(os.path.join(root, f)) / (1024 * 1024), 2),
                    'category': os.path.relpath(root, models_dir) if root != models_dir else 'uncategorized'
                })
    
    return jsonify({'success': True, 'data': models, 'count': len(models)})


@assets_bp.route('/upload-model', methods=['POST'])
def upload_model():
    """Upload a 3D model file."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    category = request.form.get('category', 'uncategorized')
    
    if not file.filename:
        return jsonify({'success': False, 'error': 'No filename'}), 400
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_MODEL_EXTENSIONS:
        return jsonify({'success': False, 'error': f'Invalid file type. Allowed: {ALLOWED_MODEL_EXTENSIONS}'}), 400
    
    # Save to static/models/<category>/
    static_dir = current_app.static_folder
    save_dir = os.path.join(static_dir, 'models', category)
    os.makedirs(save_dir, exist_ok=True)
    
    filepath = os.path.join(save_dir, file.filename)
    file.save(filepath)
    
    model_url = f'/static/models/{category}/{file.filename}'
    size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
    
    logger.info(f"Model uploaded: {file.filename} ({size_mb}MB) to {model_url}")
    
    return jsonify({
        'success': True,
        'data': {
            'filename': file.filename,
            'path': model_url,
            'size_mb': size_mb,
            'category': category
        }
    }), 201


@assets_bp.route('/upload-thumbnail', methods=['POST'])
def upload_thumbnail():
    """Upload a thumbnail image."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if not file.filename:
        return jsonify({'success': False, 'error': 'No filename'}), 400
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({'success': False, 'error': f'Invalid file type. Allowed: {ALLOWED_IMAGE_EXTENSIONS}'}), 400
    
    static_dir = current_app.static_folder
    save_dir = os.path.join(static_dir, 'thumbnails')
    os.makedirs(save_dir, exist_ok=True)
    
    filepath = os.path.join(save_dir, file.filename)
    file.save(filepath)
    
    thumbnail_url = f'/static/thumbnails/{file.filename}'
    logger.info(f"Thumbnail uploaded: {file.filename} to {thumbnail_url}")
    
    return jsonify({
        'success': True,
        'data': {
            'filename': file.filename,
            'path': thumbnail_url
        }
    }), 201

"""Local JSON-based data service — replaces Supabase."""
import json
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models.json')


class DataService:
    """In-memory data service backed by models.json file."""

    _data: List[Dict] = []
    _loaded = False

    @classmethod
    def initialize(cls):
        """Load furniture data from models.json."""
        cls._load()
        logger.info(f"DataService initialized with {len(cls._data)} items")

    @classmethod
    def _load(cls):
        """Read data from JSON file."""
        try:
            with open(DATA_FILE, 'r') as f:
                raw = json.load(f)
            # Convert model_path to model_url
            for item in raw:
                if 'model_path' in item:
                    item['model_url'] = f"/static/models/{item.pop('model_path')}"
            cls._data = raw
            cls._loaded = True
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            cls._data = []

    @classmethod
    def _save(cls):
        """Write data back to JSON file (for mutations)."""
        try:
            # Convert model_url back to model_path for storage
            to_save = []
            for item in cls._data:
                copy = dict(item)
                if 'model_url' in copy:
                    url = copy.pop('model_url')
                    copy['model_path'] = url.replace('/static/models/', '')
                to_save.append(copy)
            with open(DATA_FILE, 'w') as f:
                json.dump(to_save, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save data: {e}")

    @classmethod
    def get_furniture_list(cls, category: Optional[str] = None,
                           style: Optional[str] = None) -> List[Dict]:
        """Get furniture list with optional filtering."""
        if not cls._loaded:
            cls._load()

        result = cls._data
        if category:
            result = [f for f in result if f.get('category') == category]
        if style:
            result = [f for f in result if f.get('style') == style]

        logger.info(f"Retrieved {len(result)} furniture items")
        return result

    @classmethod
    def get_furniture_by_id(cls, furniture_id: str) -> Optional[Dict]:
        """Get single furniture item by ID."""
        if not cls._loaded:
            cls._load()

        item = next((f for f in cls._data if f['id'] == furniture_id), None)
        if item:
            logger.info(f"Retrieved furniture: {furniture_id}")
        else:
            logger.warning(f"Furniture not found: {furniture_id}")
        return item

    @classmethod
    def get_furniture_by_ids(cls, furniture_ids: List[str]) -> List[Dict]:
        """Get multiple furniture items by IDs."""
        if not cls._loaded:
            cls._load()

        ids_set = set(furniture_ids)
        result = [f for f in cls._data if f['id'] in ids_set]
        logger.info(f"Retrieved {len(result)} furniture items by IDs")
        return result

    @classmethod
    def create_furniture(cls, furniture_data: Dict) -> str:
        """Add a new furniture item."""
        if not cls._loaded:
            cls._load()

        cls._data.append(furniture_data)
        cls._save()
        logger.info(f"Created furniture: {furniture_data.get('id')}")
        return furniture_data.get('id', '')

    @classmethod
    def update_furniture(cls, furniture_id: str, updates: Dict) -> bool:
        """Update an existing furniture item."""
        if not cls._loaded:
            cls._load()

        for i, item in enumerate(cls._data):
            if item['id'] == furniture_id:
                cls._data[i].update(updates)
                cls._save()
                logger.info(f"Updated furniture: {furniture_id}")
                return True
        return False

    @classmethod
    def delete_furniture(cls, furniture_id: str) -> bool:
        """Delete a furniture item."""
        if not cls._loaded:
            cls._load()

        before = len(cls._data)
        cls._data = [f for f in cls._data if f['id'] != furniture_id]
        if len(cls._data) < before:
            cls._save()
            logger.info(f"Deleted furniture: {furniture_id}")
            return True
        return False

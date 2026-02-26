"""Supabase service for PostgreSQL database and Storage operations."""
from typing import List, Dict, Optional
from urllib.parse import quote
import logging
import os
import httpx

logger = logging.getLogger(__name__)


class SupabaseService:
    """Handles all Supabase database and storage operations."""
    
    _initialized = False
    _base_url: Optional[str] = None
    _rest_url: Optional[str] = None
    _storage_url: Optional[str] = None
    _headers: Optional[Dict[str, str]] = None
    _http_client: Optional[httpx.Client] = None
    
    @classmethod
    def initialize(cls, supabase_url: str, supabase_key: str):
        """Initialize Supabase client."""
        if cls._initialized:
            logger.info("Supabase already initialized")
            return
        
        try:
            cls._base_url = supabase_url.rstrip("/")
            cls._rest_url = f"{cls._base_url}/rest/v1"
            cls._storage_url = f"{cls._base_url}/storage/v1"
            cls._headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
            }
            verify_ssl = os.getenv("SUPABASE_SSL_VERIFY", "true").lower() != "false"
            cls._http_client = httpx.Client(
                http2=False,
                timeout=httpx.Timeout(30.0),
                verify=verify_ssl,
                trust_env=False,
                follow_redirects=True,
            )
            cls._initialized = True
            logger.info("Supabase initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            raise
    
    @classmethod
    def get_furniture_list(cls, category: Optional[str] = None, 
                          style: Optional[str] = None) -> List[Dict]:
        """
        Retrieve furniture items from PostgreSQL.
        
        Args:
            category: Filter by category (e.g., 'living', 'bedroom')
            style: Filter by style (e.g., 'minimal', 'modern')
        
        Returns:
            List of furniture dictionaries
        """
        try:
            params = {"select": "*"}

            if category:
                params["category"] = f"eq.{category}"
            if style:
                params["style"] = f"eq.{style}"

            response = cls._http_client.get(
                f"{cls._rest_url}/furniture",
                headers=cls._headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            furniture_list = response.json()
            
            logger.info(f"Retrieved {len(furniture_list)} furniture items")
            return furniture_list
        
        except Exception as e:
            logger.error(f"Error retrieving furniture list: {e}")
            raise
    
    @classmethod
    def get_furniture_by_id(cls, furniture_id: str) -> Optional[Dict]:
        """
        Retrieve a single furniture item by ID.
        
        Args:
            furniture_id: The furniture ID
        
        Returns:
            Furniture dictionary or None if not found
        """
        try:
            response = cls._http_client.get(
                f"{cls._rest_url}/furniture",
                headers=cls._headers,
                params={"select": "*", "id": f"eq.{furniture_id}"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data:
                logger.info(f"Retrieved furniture: {furniture_id}")
                return data[0]
            else:
                logger.warning(f"Furniture not found: {furniture_id}")
                return None
        
        except Exception as e:
            logger.error(f"Error retrieving furniture {furniture_id}: {e}")
            raise
    
    @classmethod
    def get_furniture_by_ids(cls, furniture_ids: List[str]) -> List[Dict]:
        """
        Retrieve multiple furniture items by IDs.
        
        Args:
            furniture_ids: List of furniture IDs
        
        Returns:
            List of furniture dictionaries
        """
        try:
            if not furniture_ids:
                return []

            ids_csv = ",".join(furniture_ids)
            response = cls._http_client.get(
                f"{cls._rest_url}/furniture",
                headers=cls._headers,
                params={"select": "*", "id": f"in.({ids_csv})"},
                timeout=10,
            )
            response.raise_for_status()
            furniture_list = response.json()
            logger.info(f"Retrieved {len(furniture_list)} furniture items")
            return furniture_list
        except Exception as e:
            logger.error(f"Error retrieving furniture by IDs: {e}")
            raise
    
    @classmethod
    def upload_file(cls, file_path: str, bucket: str, destination_path: str) -> str:
        """
        Upload a file to Supabase Storage.
        
        Args:
            file_path: Local file path
            bucket: Storage bucket name
            destination_path: Destination path in bucket
        
        Returns:
            Public URL of the uploaded file
        """
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()

            headers = {
                **cls._headers,
                "Content-Type": cls._get_content_type(file_path),
                "x-upsert": "true",
            }
            encoded_path = quote(destination_path, safe="/")
            response = cls._http_client.post(
                f"{cls._storage_url}/object/{bucket}/{encoded_path}",
                headers=headers,
                data=file_data,
                timeout=60,
            )
            response.raise_for_status()

            logger.info(f"Uploaded {file_path} to {bucket}/{destination_path}")
            return cls.get_public_url(bucket, destination_path)
        
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise
    
    @classmethod
    def _get_content_type(cls, file_path: str) -> str:
        """Determine content type from file extension."""
        ext = file_path.rsplit('.', 1)[-1].lower()
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'webp': 'image/webp',
            'glb': 'model/gltf-binary',
            'gltf': 'model/gltf+json'
        }
        return content_types.get(ext, 'application/octet-stream')
    
    @classmethod
    def create_furniture(cls, furniture_data: Dict) -> str:
        """
        Create a new furniture record in PostgreSQL.
        
        Args:
            furniture_data: Dictionary containing furniture data
        
        Returns:
            ID of created furniture
        """
        try:
            headers = {
                **cls._headers,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            response = cls._http_client.post(
                f"{cls._rest_url}/furniture",
                headers=headers,
                json=furniture_data,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            furniture_id = data[0]['id'] if data else furniture_data.get('id')
            logger.info(f"Created furniture: {furniture_id}")
            return furniture_id
        
        except Exception as e:
            logger.error(f"Error creating furniture: {e}")
            raise
    
    @classmethod
    def update_furniture(cls, furniture_id: str, furniture_data: Dict) -> bool:
        """
        Update an existing furniture record.
        
        Args:
            furniture_id: Furniture ID
            furniture_data: Updated data
        
        Returns:
            True if successful
        """
        try:
            headers = {
                **cls._headers,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            response = cls._http_client.patch(
                f"{cls._rest_url}/furniture",
                headers=headers,
                params={"id": f"eq.{furniture_id}"},
                json=furniture_data,
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"Updated furniture: {furniture_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating furniture {furniture_id}: {e}")
            raise
    
    @classmethod
    def delete_furniture(cls, furniture_id: str) -> bool:
        """
        Delete a furniture record.
        
        Args:
            furniture_id: Furniture ID
        
        Returns:
            True if successful
        """
        try:
            headers = {
                **cls._headers,
                "Prefer": "return=representation",
            }
            response = cls._http_client.delete(
                f"{cls._rest_url}/furniture",
                headers=headers,
                params={"id": f"eq.{furniture_id}"},
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"Deleted furniture: {furniture_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting furniture {furniture_id}: {e}")
            raise
    
    @classmethod
    def get_public_url(cls, bucket: str, file_path: str) -> str:
        """
        Get public URL for a file in storage.
        
        Args:
            bucket: Storage bucket name
            file_path: File path in bucket
        
        Returns:
            Public URL
        """
        try:
            return f"{cls._base_url}/storage/v1/object/public/{bucket}/{file_path}"
        except Exception as e:
            logger.error(f"Error getting public URL: {e}")
            raise

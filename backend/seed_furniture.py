"""
Seed script to populate Supabase PostgreSQL with sample furniture data.
Run this once to initialize your furniture table.

Prerequisites:
1. Create 'furniture' table in Supabase with the following SQL:

CREATE TABLE furniture (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    style TEXT NOT NULL,
    model_url TEXT NOT NULL,
    thumbnail_url TEXT NOT NULL,
    available_colors TEXT[] NOT NULL,
    dimensions JSONB NOT NULL,
    description TEXT,
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

2. Create storage buckets: 'models', 'thumbnails', 'uploads', 'redesigns'
3. Make 'models' and 'thumbnails' public
"""
from services.supabase_service import SupabaseService
from config.settings import Config
import os

# Sample furniture data
SAMPLE_FURNITURE = [
    {
        "id": "sofa_001",
        "name": "Modern Minimalist Sofa",
        "category": "living",
        "style": "minimal",
        "model_url": "https://your-project.supabase.co/storage/v1/object/public/models/sofa_001.glb",
        "thumbnail_url": "https://your-project.supabase.co/storage/v1/object/public/thumbnails/sofa_001.jpg",
        "available_colors": ["#FFFFFF", "#808080", "#2C2C2C"],
        "dimensions": {
            "width": 2.4,
            "depth": 1.2,
            "height": 0.8
        },
        "description": "Clean lines, comfortable seating for modern living rooms",
        "tags": ["sofa", "seating", "modern", "minimal"]
    },
    {
        "id": "table_001",
        "name": "Scandinavian Coffee Table",
        "category": "living",
        "style": "scandinavian",
        "model_url": "https://your-project.supabase.co/storage/v1/object/public/models/table_001.glb",
        "thumbnail_url": "https://your-project.supabase.co/storage/v1/object/public/thumbnails/table_001.jpg",
        "available_colors": ["#D4A574", "#8B7355"],
        "dimensions": {
            "width": 1.2,
            "depth": 0.6,
            "height": 0.45
        },
        "description": "Natural wood finish, perfect for nordic-style interiors",
        "tags": ["table", "coffee table", "scandinavian", "wood"]
    },
    {
        "id": "chair_001",
        "name": "Eames-Style Dining Chair",
        "category": "dining",
        "style": "modern",
        "model_url": "https://your-project.supabase.co/storage/v1/object/public/models/chair_001.glb",
        "thumbnail_url": "https://your-project.supabase.co/storage/v1/object/public/thumbnails/chair_001.jpg",
        "available_colors": ["#FFFFFF", "#333333", "#FF6B6B"],
        "dimensions": {
            "width": 0.5,
            "depth": 0.5,
            "height": 0.85
        },
        "description": "Iconic mid-century modern design with molded plastic shell",
        "tags": ["chair", "dining", "modern", "plastic"]
    },
    {
        "id": "bed_001",
        "name": "Platform Bed Frame",
        "category": "bedroom",
        "style": "minimal",
        "model_url": "https://your-project.supabase.co/storage/v1/object/public/models/bed_001.glb",
        "thumbnail_url": "https://your-project.supabase.co/storage/v1/object/public/thumbnails/bed_001.jpg",
        "available_colors": ["#4A4A4A", "#8B7355"],
        "dimensions": {
            "width": 2.0,
            "depth": 2.2,
            "height": 0.5
        },
        "description": "Low-profile platform bed with clean aesthetic",
        "tags": ["bed", "bedroom", "minimal", "platform"]
    },
    {
        "id": "lamp_001",
        "name": "Arc Floor Lamp",
        "category": "living",
        "style": "modern",
        "model_url": "https://your-project.supabase.co/storage/v1/object/public/models/lamp_001.glb",
        "thumbnail_url": "https://your-project.supabase.co/storage/v1/object/public/thumbnails/lamp_001.jpg",
        "available_colors": ["#C0C0C0", "#8B7355", "#2C2C2C"],
        "dimensions": {
            "width": 0.4,
            "depth": 0.4,
            "height": 2.0
        },
        "description": "Elegant arcing floor lamp with adjustable shade",
        "tags": ["lamp", "lighting", "modern", "floor lamp"]
    },
    {
        "id": "cabinet_001",
        "name": "Industrial Storage Cabinet",
        "category": "living",
        "style": "industrial",
        "model_url": "https://your-project.supabase.co/storage/v1/object/public/models/cabinet_001.glb",
        "thumbnail_url": "https://your-project.supabase.co/storage/v1/object/public/thumbnails/cabinet_001.jpg",
        "available_colors": ["#2C2C2C", "#4A4A4A"],
        "dimensions": {
            "width": 1.2,
            "depth": 0.45,
            "height": 1.8
        },
        "description": "Metal and wood cabinet with urban industrial aesthetic",
        "tags": ["cabinet", "storage", "industrial", "metal"]
    }
]


def seed_furniture():
    """Seed the Supabase database with sample furniture."""
    try:
        # Initialize Supabase
        SupabaseService.initialize(
            supabase_url=Config.SUPABASE_URL,
            supabase_key=Config.SUPABASE_SERVICE_ROLE_KEY
        )
        
        print("🌱 Starting furniture seeding...")
        
        for item in SAMPLE_FURNITURE:
            furniture_id = item['id']
            
            # Check if already exists
            existing = SupabaseService.get_furniture_by_id(furniture_id)
            
            if existing:
                print(f"⏭️  Skipping {furniture_id} (already exists)")
                continue
            
            # Create furniture record
            SupabaseService.create_furniture(item)
            print(f"✅ Created {furniture_id}: {item['name']}")
        
        print("\n🎉 Seeding completed successfully!")
        print(f"Total furniture items: {len(SAMPLE_FURNITURE)}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        raise


if __name__ == '__main__':
    seed_furniture()

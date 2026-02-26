-- Supabase PostgreSQL Schema for GruhaAlankar
-- Run this SQL in your Supabase SQL Editor to set up the database

-- Create furniture table
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

-- Create indexes for common queries
CREATE INDEX idx_furniture_category ON furniture(category);
CREATE INDEX idx_furniture_style ON furniture(style);
CREATE INDEX idx_furniture_category_style ON furniture(category, style);

-- Enable Row Level Security (RLS)
ALTER TABLE furniture ENABLE ROW LEVEL SECURITY;

-- Create policy to allow read access to all users
CREATE POLICY "Allow public read access"
ON furniture FOR SELECT
USING (true);

-- Create policy to allow insert/update/delete only with service role
-- (Backend will use service role key for write operations)
CREATE POLICY "Allow service role write access"
ON furniture FOR ALL
USING (auth.role() = 'service_role');

-- Storage Buckets Setup:
-- Run these commands in Supabase Dashboard > Storage:
--
-- 1. Create buckets:
--    - models (for GLB 3D models)
--    - thumbnails (for furniture preview images)
--    - uploads (for user-uploaded room images)
--    - redesigns (for AI-generated redesign images)
--
-- 2. Make 'models' and 'thumbnails' public:
--    - Go to bucket settings
--    - Set "Public bucket" to ON
--
-- 3. Set appropriate file size limits and allowed MIME types:
--    - models: 50MB max, model/gltf-binary
--    - thumbnails: 5MB max, image/jpeg, image/png, image/webp
--    - uploads: 10MB max, image/jpeg, image/png, image/webp
--    - redesigns: 10MB max, image/jpeg, image/png, image/webp

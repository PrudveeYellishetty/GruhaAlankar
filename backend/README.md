# GruhaAlankar Backend

Flask-based REST API for AI-powered AR interior design platform.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Set up Supabase:**
   - Create a Supabase project at https://supabase.com
   - Run `supabase_schema.sql` in your Supabase SQL Editor
   - Copy your project URL and service role key to `.env`

4. **Run the server:**
   ```bash
   python app.py
   ```

   Or with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
   ```

## API Endpoints

### Furniture

- `GET /api/furniture` - List all furniture
  - Query params: `category`, `style`
  
- `GET /api/furniture/<id>` - Get furniture details

- `POST /api/furniture/batch` - Get multiple furniture items
  - Body: `{"ids": ["sofa_001", "table_002"]}`

### AI Features

- `POST /api/analyze-room` - Analyze room and get AI recommendations
  - Multipart form: `image` file

- `POST /api/redesign` - Generate redesigned room images
  - Multipart form: `image`, `style`, `color_scheme`, `furniture_focus`

- `GET /api/health` - Health check

## Architecture

```
backend/
├── app.py              # Flask application
├── config/             # Configuration
├── routes/             # API endpoints
├── services/           # Business logic
│   ├── supabase_service.py
│   └── ai_service.py
├── requirements.txt
├── supabase_schema.sql
└── .env
```

## Response Format

All AI endpoints return unified format:

```json
{
  "success": true,
  "mode": "recommendation|redesign|manual",
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
```

## Development

- Never commit credentials
- Follow clean architecture principles
- Keep services modular
- Log all errors
- Validate all inputs

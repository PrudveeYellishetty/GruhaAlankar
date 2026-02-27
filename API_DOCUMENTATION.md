# GruhaAlankar API Documentation

**Version**: 1.0  
**Last Updated**: February 27, 2026  
**Base URL**: `http://localhost:5000` (Development) | `https://production-url.com` (Production)

---

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

---

## Overview

GruhaAlankar is an AR-powered furniture shopping application. The API provides endpoints for:
- Browsing furniture catalog
- Room analysis with AI recommendations
- Fetching detailed product information
- Asset management for 3D models

### Technology Stack
- **Backend**: Flask (Python)
- **AI Engine**: Google Gemini Flash
- **3D Models**: GLB format
- **Thumbnails**: PNG images

---

## Authentication

Currently **no authentication required**. All endpoints are publicly accessible.

**Future Implementation**: Token-based authentication (JWT) will be added for user-specific features.

---

## Endpoints

### 1. Health Check
Get API status and available furniture count.

```
GET /api/health
```

**Response** (200 OK):
```json
{
  "service": "GruhaAlankar API",
  "status": "healthy",
  "success": true,
  "message": "API is running",
  "version": "1.0"
}
```

---

### 2. Get All Furniture

Fetch all furniture with optional filtering.

```
GET /api/furniture
```

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | No | Filter by category: `bedroom` or `living` |
| `style` | string | No | Filter by style: `modern`, `traditional`, `scandinavian`, `minimal`, `industrial` |
| `search` | string | No | Search by furniture name |

**Response** (200 OK):
```json
{
  "success": true,
  "count": 22,
  "data": [
    {
      "id": "bed_001",
      "name": "Classic Wooden Bed",
      "category": "bedroom",
      "style": "traditional",
      "model_url": "/static/models/bedroom/bed1.glb",
      "thumbnail_url": "/static/thumbnails/bed_001.png",
      "description": "Elegant wooden bed with a classic design...",
      "dimensions": {
        "width": 2.0,
        "depth": 1.8,
        "height": 1.2
      },
      "available_colors": ["#8B4513", "#D2691E", "#F5DEB3"],
      "tags": ["bed", "bedroom", "wooden", "traditional"]
    }
    // ... more items
  ]
}
```

**Example Requests**:
```bash
# Get all furniture
curl http://localhost:5000/api/furniture

# Filter by category
curl http://localhost:5000/api/furniture?category=bedroom

# Filter by style
curl http://localhost:5000/api/furniture?style=modern

# Search
curl http://localhost:5000/api/furniture?search=bed
```

---

### 3. Get Furniture by Category

Get furniture filtered by category.

```
GET /api/furniture/category/{category}
```

**Path Parameters**:
- `category` (string): `bedroom` or `living`

**Response** (200 OK):
```json
{
  "success": true,
  "category": "bedroom",
  "count": 10,
  "data": [ /* furniture items */ ]
}
```

**Example**:
```bash
curl http://localhost:5000/api/furniture/category/bedroom
```

---

### 4. Get Furniture Details

Get detailed information for a specific furniture item.

```
GET /api/furniture/{furnitureId}
```

**Path Parameters**:
- `furnitureId` (string): The furniture ID (e.g., `bed_001`, `chair_005`)

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "bed_001",
    "name": "Classic Wooden Bed",
    "category": "bedroom",
    "style": "traditional",
    "model_url": "/static/models/bedroom/bed1.glb",
    "thumbnail_url": "/static/thumbnails/bed_001.png",
    "description": "Elegant wooden bed with a classic design, perfect for traditional bedrooms.",
    "dimensions": {
      "width": 2.0,
      "depth": 1.8,
      "height": 1.2
    },
    "available_colors": [
      "#8B4513",
      "#D2691E",
      "#F5DEB3"
    ],
    "tags": ["bed", "bedroom", "wooden", "traditional"]
  }
}
```

**Example**:
```bash
curl http://localhost:5000/api/furniture/bed_001
```

---

### 5. Get Furniture by Multiple IDs

Fetch multiple furniture items by their IDs (useful for wishlists).

```
GET /api/furniture/ids
```

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ids` | string | Yes | Comma-separated furniture IDs (e.g., `bed_001,chair_005,sofa_001`) |

**Response** (200 OK):
```json
{
  "success": true,
  "count": 3,
  "data": [
    { /* bed_001 */ },
    { /* chair_005 */ },
    { /* sofa_001 */ }
  ]
}
```

**Example**:
```bash
curl "http://localhost:5000/api/furniture/ids?ids=bed_001,chair_005,sofa_001"
```

---

### 6. Room Analysis with AI Recommendations

Analyze a room image and get AI-powered furniture recommendations.

```
POST /api/analyze-room
```

**Request** (multipart/form-data):
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file | Yes | Room image (PNG, JPG, JPEG) - Max 10MB |

**Response** (200 OK):
```json
{
  "success": true,
  "analysis": {
    "room_type": "bedroom",
    "style": "modern",
    "colors": ["white", "gray", "wood"],
    "space_size": "medium",
    "lighting": "natural",
    "color_scheme": "cool neutral",
    "existing_furniture": ["bed", "wardrobe"],
    "suggestions": "Add accent lighting and complementary seating..."
  },
  "furniture": [
    {
      "id": "chair_001",
      "name": "Modern Accent Chair",
      "category": "living",
      "style": "modern",
      "thumbnail_url": "/static/thumbnails/chair_001.png",
      "model_url": "/static/models/living/singlechair/chair1.glb",
      "recommendation_score": 85,
      "reasons": [
        "Matches your detected modern style",
        "Perfect size for medium bedroom",
        "Complements neutral color scheme"
      ],
      "dimensions": { "width": 0.7, "depth": 0.7, "height": 0.85 },
      "available_colors": ["#FF6347", "#4682B4", "#808080"]
    }
    // ... more recommendations
  ]
}
```

**Error Response** (400):
```json
{
  "success": false,
  "error": "No image file provided"
}
```

**Error Response** (500):
```json
{
  "success": false,
  "error": "Failed to analyze room",
  "message": "Detailed error message"
}
```

**Example (cURL)**:
```bash
curl -X POST -F "image=@room.jpg" http://localhost:5000/api/analyze-room
```

**Example (Flutter)**:
```dart
var request = http.MultipartRequest(
  'POST',
  Uri.parse('http://localhost:5000/api/analyze-room')
);
request.files.add(await http.MultipartFile.fromPath('image', imagePath));
var response = await request.send();
var responseBody = await response.stream.bytesToString();
var result = jsonDecode(responseBody);
```

---

### 7. Test Room Analysis Endpoint

Quick test to verify room analysis service is working.

```
GET /api/analyze-room/test
```

**Response** (200 OK):
```json
{
  "status": "ready",
  "message": "Room analysis service is ready",
  "furniture_count": 22
}
```

**Example**:
```bash
curl http://localhost:5000/api/analyze-room/test
```

---

## Data Models

### Furniture Object

```json
{
  "id": "bed_001",
  "name": "Classic Wooden Bed",
  "category": "bedroom",
  "style": "traditional",
  "description": "Elegant wooden bed with a classic design...",
  "model_path": "bedroom/bed1.glb",
  "model_url": "/static/models/bedroom/bed1.glb",
  "thumbnail_url": "/static/thumbnails/bed_001.png",
  "dimensions": {
    "width": 2.0,
    "depth": 1.8,
    "height": 1.2
  },
  "available_colors": [
    "#8B4513",
    "#D2691E",
    "#F5DEB3"
  ],
  "tags": [
    "bed",
    "bedroom",
    "wooden",
    "traditional"
  ]
}
```

### Room Analysis Response

```json
{
  "analysis": {
    "room_type": "string (bedroom|living|dining|office)",
    "style": "string (modern|traditional|scandinavian|minimal|industrial)",
    "colors": ["string", "string"],
    "space_size": "string (small|medium|large)",
    "lighting": "string (bright|natural|dim|artificial)",
    "color_scheme": "string (warm|cool|neutral)",
    "existing_furniture": ["string"],
    "suggestions": "string"
  },
  "furniture": [
    {
      "id": "string",
      "name": "string",
      "category": "string",
      "style": "string",
      "thumbnail_url": "string",
      "model_url": "string",
      "recommendation_score": "number (0-100)",
      "reasons": ["string"],
      "dimensions": {
        "width": "number",
        "depth": "number",
        "height": "number"
      },
      "available_colors": ["string (hex color)"]
    }
  ]
}
```

---

## Error Handling

### Standard Error Response

```json
{
  "success": false,
  "error": "Error message",
  "message": "Detailed error message (if applicable)"
}
```

### HTTP Status Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Missing/invalid parameters |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | Server down or maintenance |

**Examples**:

**404 - Item Not Found**:
```json
{
  "success": false,
  "error": "Furniture not found"
}
```

**400 - Missing Image**:
```json
{
  "success": false,
  "error": "No image file provided"
}
```

---

## Filtering Options

### Categories
- `bedroom` - Bedroom furniture (10 items)
- `living` - Living room furniture (12 items)

### Styles
- `modern` - Contemporary design
- `traditional` - Classic design
- `scandinavian` - Nordic/light design
- `minimal` - Minimalist design
- `industrial` - Raw industrial design

### Room Types (from AI Analysis)
- `bedroom`
- `living`
- `dining`
- `office`

---

## Rate Limiting

**Current**: No rate limiting (development mode)

**Recommended for Production**:
- 100 requests per minute per IP
- 10 room analysis requests per hour per IP

---

## CORS Configuration

**Allowed Origins**: `*` (all origins)

**Allowed Methods**: `GET`, `POST`, `OPTIONS`

**Allowed Headers**: `Content-Type`, `Authorization`

---

## Deployment URLs

### Development
- **Laptop**: `http://localhost:3000`
- **Local IP**: `http://192.168.0.26:3000`
- **API**: `http://localhost:5000`

### Production (Mobile)
- **Ngrok Tunnel**: `https://74a4-2406-b400-b5-182d-3e3c-4334-a87e-c8b9.ngrok-free.app`
- **API Base**: `https://74a4-2406-b400-b5-182d-3e3c-4334-a87e-c8b9.ngrok-free.app/api`

*Note: Ngrok URL shows security interstitial page first time. Click "Visit Site" to proceed.*

---

## Examples

### Flutter Implementation Examples

#### 1. Fetch All Furniture

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<Furniture>> fetchFurniture() async {
  final response = await http.get(
    Uri.parse('http://192.168.0.26:5000/api/furniture'),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    final List<dynamic> furnitureList = data['data'];
    return furnitureList
        .map((item) => Furniture.fromJson(item))
        .toList();
  } else {
    throw Exception('Failed to load furniture');
  }
}
```

#### 2. Get Furniture Details

```dart
Future<Furniture> getFurnitureDetail(String id) async {
  final response = await http.get(
    Uri.parse('http://192.168.0.26:5000/api/furniture/$id'),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return Furniture.fromJson(data['data']);
  } else {
    throw Exception('Failed to load furniture details');
  }
}
```

#### 3. Analyze Room with Image

```dart
Future<RoomAnalysis> analyzeRoom(File imageFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('http://192.168.0.26:5000/api/analyze-room'),
  );

  request.files.add(
    await http.MultipartFile.fromPath('image', imageFile.path),
  );

  var response = await request.send();
  var responseBody = await response.stream.bytesToString();

  if (response.statusCode == 200) {
    final data = jsonDecode(responseBody);
    return RoomAnalysis.fromJson(data);
  } else {
    throw Exception('Failed to analyze room');
  }
}
```

#### 4. Filter Furniture by Category

```dart
Future<List<Furniture>> getFurnitureByCategory(String category) async {
  final response = await http.get(
    Uri.parse('http://192.168.0.26:5000/api/furniture?category=$category'),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    final List<dynamic> furnitureList = data['data'];
    return furnitureList
        .map((item) => Furniture.fromJson(item))
        .toList();
  } else {
    throw Exception('Failed to load furniture');
  }
}
```

#### 5. Fetch Multiple Furniture by IDs (Wishlist)

```dart
Future<List<Furniture>> getFurnitureByIds(List<String> ids) async {
  final idsString = ids.join(',');
  final response = await http.get(
    Uri.parse('http://192.168.0.26:5000/api/furniture/ids?ids=$idsString'),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    final List<dynamic> furnitureList = data['data'];
    return furnitureList
        .map((item) => Furniture.fromJson(item))
        .toList();
  } else {
    throw Exception('Failed to load furniture');
  }
}
```

### Model Classes (Dart)

```dart
class Furniture {
  final String id;
  final String name;
  final String category;
  final String style;
  final String description;
  final String modelUrl;
  final String thumbnailUrl;
  final Dimensions dimensions;
  final List<String> availableColors;
  final List<String> tags;

  Furniture({
    required this.id,
    required this.name,
    required this.category,
    required this.style,
    required this.description,
    required this.modelUrl,
    required this.thumbnailUrl,
    required this.dimensions,
    required this.availableColors,
    required this.tags,
  });

  factory Furniture.fromJson(Map<String, dynamic> json) {
    return Furniture(
      id: json['id'],
      name: json['name'],
      category: json['category'],
      style: json['style'],
      description: json['description'],
      modelUrl: json['model_url'],
      thumbnailUrl: json['thumbnail_url'],
      dimensions: Dimensions.fromJson(json['dimensions']),
      availableColors: List<String>.from(json['available_colors']),
      tags: List<String>.from(json['tags']),
    );
  }
}

class Dimensions {
  final double width;
  final double depth;
  final double height;

  Dimensions({
    required this.width,
    required this.depth,
    required this.height,
  });

  factory Dimensions.fromJson(Map<String, dynamic> json) {
    return Dimensions(
      width: json['width'].toDouble(),
      depth: json['depth'].toDouble(),
      height: json['height'].toDouble(),
    );
  }
}

class RoomAnalysis {
  final Analysis analysis;
  final List<Furniture> furniture;

  RoomAnalysis({
    required this.analysis,
    required this.furniture,
  });

  factory RoomAnalysis.fromJson(Map<String, dynamic> json) {
    return RoomAnalysis(
      analysis: Analysis.fromJson(json['analysis']),
      furniture: (json['furniture'] as List)
          .map((item) => Furniture.fromJson(item))
          .toList(),
    );
  }
}

class Analysis {
  final String roomType;
  final String style;
  final List<String> colors;
  final String spaceSize;
  final String lighting;
  final String colorScheme;
  final List<String> existingFurniture;
  final String suggestions;

  Analysis({
    required this.roomType,
    required this.style,
    required this.colors,
    required this.spaceSize,
    required this.lighting,
    required this.colorScheme,
    required this.existingFurniture,
    required this.suggestions,
  });

  factory Analysis.fromJson(Map<String, dynamic> json) {
    return Analysis(
      roomType: json['room_type'],
      style: json['style'],
      colors: List<String>.from(json['colors']),
      spaceSize: json['space_size'],
      lighting: json['lighting'],
      colorScheme: json['color_scheme'],
      existingFurniture: List<String>.from(json['existing_furniture']),
      suggestions: json['suggestions'],
    );
  }
}
```

---

## Implementation Checklist for Flutter

- [ ] Setup HTTP client
- [ ] Create model classes (Furniture, RoomAnalysis, etc.)
- [ ] Implement furniture list screen with API call
- [ ] Add category/style filtering
- [ ] Implement furniture detail page
- [ ] Add room analysis feature with image picker
- [ ] Display AI recommendations
- [ ] Implement 3D model viewer (model-viewer or three.js)
- [ ] Setup wishlist with local storage (Hive/Sqflite)
- [ ] Add error handling and loading states
- [ ] Implement pagination if needed
- [ ] Add caching for API responses

---

## Support & Debugging

**Common Issues**:

1. **API not responding**
   - Check if backend is running: `docker ps`
   - Verify base URL and port (5000)

2. **CORS errors**
   - Ensure Flutter app is making correct headers
   - Check allowed origins in backend config

3. **Image upload fails**
   - Check file size (max 10MB)
   - Verify file format (PNG, JPG, JPEG)
   - Use `http.MultipartRequest` for file upload

4. **AI analysis takes long**
   - Gemini API can take 30-60 seconds for first request
   - Add loading indicator in UI
   - Consider timeout of 120 seconds

**Backend Logs**:
```bash
docker logs gruhaalankar-app-1
```

**API Testing**:
```bash
# Test with curl
curl http://localhost:5000/api/health
```

---

**Last Updated**: February 27, 2026  
**API Version**: 1.0  
**Maintained by**: GruhaAlankar Development Team

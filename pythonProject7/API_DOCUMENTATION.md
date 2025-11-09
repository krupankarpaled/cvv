# 📡 Color Detector Pro - Complete API Documentation

## Overview

The Color Detector Pro API provides comprehensive color analysis, palette generation, and color history management capabilities.

**Base URL**: `http://localhost:10000/api`

**Rate Limiting**: 60 requests per minute (configurable)

**Authentication**: Session-based (automatic)

---

## Table of Contents

1. [System Endpoints](#system-endpoints)
2. [Color Detection](#color-detection)
3. [Color Analysis](#color-analysis)
4. [History Management](#history-management)
5. [Palette Management](#palette-management)
6. [Error Handling](#error-handling)
7. [Response Formats](#response-formats)

---

## System Endpoints

### Health Check
```http
GET /health
```

**Description**: Check if the service is running

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "version": "2.0.0"
}
```

### API Information
```http
GET /api/info
```

**Description**: Get API metadata and available endpoints

**Response**:
```json
{
  "name": "Color Detector API",
  "version": "2.0.0",
  "endpoints": { ... }
}
```

---

## Color Detection

### Detect Color from Image

```http
POST /api/detect
Content-Type: application/json
```

**Description**: Detect and analyze color from a base64-encoded image

**Request Body**:
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA...",
  "x": 320,  // Optional: X coordinate (default: center)
  "y": 240   // Optional: Y coordinate (default: center)
}
```

**Response**:
```json
{
  "success": true,
  "color": {
    "hex": "#3b82f6",
    "name": "Blue",
    "rgb": {
      "r": 59,
      "g": 130,
      "b": 246
    },
    "hsl": {
      "h": 217.2,
      "s": 91.2,
      "l": 59.8
    },
    "hsv": {
      "h": 217.2,
      "s": 76.0,
      "v": 96.5
    },
    "cmyk": {
      "c": 76.0,
      "m": 47.2,
      "y": 0.0,
      "k": 3.5
    },
    "temperature": {
      "temperature": "cool",
      "warmth_value": -187,
      "description": "This color has cool tones"
    },
    "accessibility": {
      "white_background": {
        "ratio": 3.94,
        "aa_normal": false,
        "aa_large": true,
        "aaa_normal": false,
        "aaa_large": false
      },
      "black_background": {
        "ratio": 5.33,
        "aa_normal": true,
        "aa_large": true,
        "aaa_normal": false,
        "aaa_large": true
      }
    }
  },
  "schemes": {
    "monochromatic": [
      { "hex": "#1a4d99", "name": "DarkBlue" },
      { "hex": "#3b82f6", "name": "Blue" },
      { "hex": "#93c5fd", "name": "LightBlue" }
    ],
    "complementary": [
      { "hex": "#f6a03b", "name": "Orange" }
    ],
    "analogous": [
      { "hex": "#3bf6d9", "name": "Cyan" },
      { "hex": "#3b59f6", "name": "Indigo" }
    ],
    "triadic": [
      { "hex": "#f63b82", "name": "Pink" },
      { "hex": "#82f63b", "name": "LimeGreen" }
    ],
    "tetradic": [
      { "hex": "#f6a03b", "name": "Orange" },
      { "hex": "#f63b82", "name": "Pink" },
      { "hex": "#3bf6a0", "name": "SpringGreen" }
    ],
    "split_complementary": [
      { "hex": "#f6d93b", "name": "Gold" },
      { "hex": "#f6593b", "name": "Coral" }
    ],
    "shades": [
      { "hex": "#2c66c4", "name": "DarkBlue" },
      { "hex": "#1d4a92", "name": "Navy" },
      { "hex": "#0e2e60", "name": "MidnightBlue" }
    ],
    "tints": [
      { "hex": "#5c9bf8", "name": "LightBlue" },
      { "hex": "#7db4fa", "name": "SkyBlue" },
      { "hex": "#9ecdfc", "name": "PaleSkyBlue" }
    ]
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Rate Limit**: 30 requests/minute

**Errors**:
- `400`: Invalid image data
- `429`: Rate limit exceeded
- `500`: Server error

---

## Color Analysis

### Analyze Color by Hex Code

```http
POST /api/analyze
Content-Type: application/json
```

**Description**: Analyze a color without image upload

**Request Body**:
```json
{
  "hex": "#3b82f6"  // With or without # prefix
}
```

**Response**: Same structure as `/api/detect` (color object only)

**Rate Limit**: 20 requests/minute

---

## History Management

### Get Color History

```http
GET /api/history?limit=20
```

**Description**: Retrieve color detection history for current session

**Query Parameters**:
- `limit` (optional): Number of items to return (max: 100, default: 20)

**Response**:
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "hex_code": "#3b82f6",
      "color_name": "Blue",
      "rgb": {
        "r": 59,
        "g": 130,
        "b": 246
      },
      "created_at": "2024-01-01T12:00:00.000Z"
    }
  ],
  "count": 1
}
```

### Delete History Item

```http
DELETE /api/history/{id}
```

**Description**: Delete a specific history item

**URL Parameters**:
- `id`: History item ID

**Response**:
```json
{
  "success": true,
  "message": "History item deleted"
}
```

### Clear All History

```http
DELETE /api/history/clear
```

**Description**: Clear all history for current session

**Response**:
```json
{
  "success": true,
  "message": "History cleared"
}
```

---

## Palette Management

### Get All Palettes

```http
GET /api/palettes
```

**Description**: Get all saved color palettes

**Response**:
```json
{
  "success": true,
  "palettes": [
    {
      "id": 1,
      "name": "Ocean Blues",
      "description": "Cool ocean-inspired palette",
      "colors": ["#1e3a8a", "#3b82f6", "#60a5fa", "#93c5fd"],
      "is_favorite": true,
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:00:00.000Z"
    }
  ],
  "count": 1
}
```

### Create Palette

```http
POST /api/palettes
Content-Type: application/json
```

**Description**: Create a new color palette

**Request Body**:
```json
{
  "name": "Ocean Blues",
  "description": "Cool ocean-inspired palette",
  "colors": ["#1e3a8a", "#3b82f6", "#60a5fa", "#93c5fd"],
  "is_favorite": false
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "palette": { /* palette object */ }
}
```

### Update Palette

```http
PUT /api/palettes/{id}
Content-Type: application/json
```

**Description**: Update an existing palette

**URL Parameters**:
- `id`: Palette ID

**Request Body** (all fields optional):
```json
{
  "name": "Updated Name",
  "description": "New description",
  "colors": ["#000000", "#ffffff"],
  "is_favorite": true
}
```

**Response**:
```json
{
  "success": true,
  "palette": { /* updated palette object */ }
}
```

### Delete Palette

```http
DELETE /api/palettes/{id}
```

**Description**: Delete a palette

**URL Parameters**:
- `id`: Palette ID

**Response**:
```json
{
  "success": true,
  "message": "Palette deleted"
}
```

---

## Error Handling

All errors follow this format:

```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Common Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Something went wrong |

---

## Response Formats

### Color Object

```typescript
{
  hex: string,              // "#rrggbb"
  name: string,             // Nearest color name
  rgb: {
    r: number,              // 0-255
    g: number,              // 0-255
    b: number               // 0-255
  },
  hsl: {
    h: number,              // 0-360 degrees
    s: number,              // 0-100 percent
    l: number               // 0-100 percent
  },
  hsv: {
    h: number,              // 0-360 degrees
    s: number,              // 0-100 percent
    v: number               // 0-100 percent
  },
  cmyk: {
    c: number,              // 0-100 percent
    m: number,              // 0-100 percent
    y: number,              // 0-100 percent
    k: number               // 0-100 percent
  },
  temperature: {
    temperature: string,     // "warm" | "cool" | "neutral"
    warmth_value: number,
    description: string
  },
  accessibility: {
    white_background: AccessibilityInfo,
    black_background: AccessibilityInfo
  }
}
```

### Accessibility Info

```typescript
{
  ratio: number,            // Contrast ratio (1-21)
  aa_normal: boolean,       // WCAG AA normal text (4.5:1)
  aa_large: boolean,        // WCAG AA large text (3:1)
  aaa_normal: boolean,      // WCAG AAA normal text (7:1)
  aaa_large: boolean        // WCAG AAA large text (4.5:1)
}
```

---

## Usage Examples

### JavaScript/Fetch

```javascript
// Detect color from canvas
const canvas = document.getElementById('myCanvas');
const imageData = canvas.toDataURL('image/jpeg');

const response = await fetch('/api/detect', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ image: imageData })
});

const data = await response.json();
console.log('Detected color:', data.color.hex);
```

### Python/Requests

```python
import requests
import base64

# Read image and encode
with open('image.jpg', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode()

# Detect color
response = requests.post(
    'http://localhost:10000/api/detect',
    json={'image': f'data:image/jpeg;base64,{img_data}'}
)

data = response.json()
print(f"Detected: {data['color']['name']} ({data['color']['hex']})")
```

### cURL

```bash
# Analyze hex color
curl -X POST http://localhost:10000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"hex": "#3b82f6"}'

# Get history
curl http://localhost:10000/api/history?limit=5
```

---

## Rate Limits

Default rate limits (configurable via environment):

| Endpoint | Limit |
|----------|-------|
| `/api/detect` | 30/minute |
| `/api/analyze` | 20/minute |
| All others | 60/minute |

When rate limit is exceeded:
```json
{
  "success": false,
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later."
}
```

---

## Best Practices

1. **Image Size**: Keep images under 5MB for best performance
2. **Error Handling**: Always check `success` field in responses
3. **Rate Limits**: Implement exponential backoff for retries
4. **Session Management**: Browser automatically handles sessions
5. **Caching**: Consider caching color analysis results

---

## Support

For issues or questions:
- GitHub Issues: [Your repo URL]
- Email: [Your email]
- Documentation: [Your docs URL]

---

Last updated: 2024-01-01

# 🎨 Color Detector Pro - Production-Ready Color Analysis Tool

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**Advanced color detection, analysis, and palette generation tool with modern UI**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Documentation](#api-documentation) • [Deployment](#deployment)

</div>

---

## ✨ Features

### 🎯 Core Features
- **Real-time Color Detection** - Capture colors from your webcam or uploaded images
- **Advanced Color Analysis** - Get detailed information including RGB, HSL, HSV, CMYK values
- **Multiple Color Schemes** - Generate 8 different color harmony schemes:
  - Monochromatic
  - Complementary
  - Analogous
  - Triadic
  - Tetradic
  - Split Complementary
  - Shades & Tints

### ♿ Accessibility
- **WCAG Compliance Checker** - Test colors against AA and AAA standards
- **Contrast Ratio Calculator** - Ensure readable text colors
- **Accessibility Ratings** - For both light and dark backgrounds

### 🎨 Design Features
- **Modern UI/UX** - Beautiful, responsive design
- **Dark Mode** - Eye-friendly theme switching
- **Smooth Animations** - Polished user experience
- **Mobile Responsive** - Works perfectly on all devices

### 💾 Data Management
- **Color History** - Track all detected colors
- **Palette Saving** - Save and manage custom palettes
- **Export Options** - Export to JSON, CSS, or copy to clipboard

### 🔧 Technical Features
- **RESTful API** - Well-documented endpoints
- **SQLite Database** - Persistent storage
- **Rate Limiting** - API protection
- **CORS Support** - Cross-origin requests
- **Comprehensive Logging** - Debug and monitor easily
- **Error Handling** - Graceful error management
- **Docker Ready** - Easy deployment

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager
- (Optional) Docker for containerized deployment

### Method 1: Local Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd pythonProject7
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example environment file
copy .env.example .env

# Edit .env with your settings
# Set SECRET_KEY to a random string
```

5. **Initialize database**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. **Run the application**
```bash
# Development
python app.py

# Production
gunicorn --bind 0.0.0.0:10000 --workers 4 app:app
```

### Method 2: Docker Installation

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Or build manually**
```bash
# Build image
docker build -t color-detector .

# Run container
docker run -p 10000:10000 -e SECRET_KEY=your-secret-key color-detector
```

---

## 📖 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:10000`
2. Allow camera access when prompted
3. Point camera at any color you want to detect
4. Click "Detect Color" to analyze
5. Explore different color schemes, accessibility info, and history

### Camera Controls
- **Detect Color**: Capture and analyze the color in the center box
- **Switch Camera**: Toggle between front and rear cameras
- **Theme Toggle**: Switch between light and dark modes

### Features Usage

#### Color Schemes
- Click on scheme buttons to view different harmonies
- Click any color swatch to copy its hex code
- Explore complementary, analogous, triadic, and more!

#### Accessibility Checker
- View WCAG AA and AAA compliance
- Check contrast ratios
- Ensure your colors are accessible

#### History
- View all detected colors
- Delete individual items
- Clear entire history

#### Export
- **Copy Hex**: Quick copy to clipboard
- **Export JSON**: Download complete color data
- **Export CSS**: Get CSS variables for your project

---

## 🔌 API Documentation

### Base URL
```
http://localhost:10000/api
```

### Endpoints

#### Health Check
```http
GET /health
```
Returns application health status.

#### Detect Color
```http
POST /api/detect
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,..."
}
```
Detects color from base64 encoded image.

**Response:**
```json
{
  "success": true,
  "color": {
    "hex": "#ff0000",
    "name": "Red",
    "rgb": { "r": 255, "g": 0, "b": 0 },
    "hsl": { "h": 0, "s": 100, "l": 50 },
    "hsv": { "h": 0, "s": 100, "v": 100 },
    "cmyk": { "c": 0, "m": 100, "y": 100, "k": 0 },
    "temperature": {
      "temperature": "warm",
      "warmth_value": 255,
      "description": "This color has warm tones"
    },
    "accessibility": { ... }
  },
  "schemes": {
    "monochromatic": [...],
    "complementary": [...],
    "analogous": [...],
    "triadic": [...],
    "tetradic": [...],
    "split_complementary": [...],
    "shades": [...],
    "tints": [...]
  }
}
```

#### Analyze Color by Hex
```http
POST /api/analyze
Content-Type: application/json

{
  "hex": "#ff0000"
}
```

#### Get History
```http
GET /api/history?limit=20
```

#### Delete History Item
```http
DELETE /api/history/{id}
```

#### Clear All History
```http
DELETE /api/history/clear
```

#### Get Palettes
```http
GET /api/palettes
```

#### Create Palette
```http
POST /api/palettes
Content-Type: application/json

{
  "name": "My Palette",
  "description": "Beautiful colors",
  "colors": ["#ff0000", "#00ff00", "#0000ff"],
  "is_favorite": false
}
```

#### Update Palette
```http
PUT /api/palettes/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "is_favorite": true
}
```

#### Delete Palette
```http
DELETE /api/palettes/{id}
```

---

## 🌐 Deployment

### Deploy to Render.com

1. Push code to GitHub
2. Go to [Render.com](https://render.com) and create a new Web Service
3. Connect your repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: Set `SECRET_KEY`

### Deploy with Docker

```bash
# Build
docker build -t color-detector .

# Push to registry
docker tag color-detector your-registry/color-detector
docker push your-registry/color-detector

# Deploy on server
docker pull your-registry/color-detector
docker run -d -p 80:10000 -e SECRET_KEY=xxx your-registry/color-detector
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask secret key | (required) |
| `DEBUG` | Debug mode | `False` |
| `PORT` | Server port | `10000` |
| `DATABASE_URL` | Database connection | `sqlite:///color_detector.db` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | `60` |

---

## 🧪 Testing

Run tests:
```bash
# All tests
python -m pytest tests/

# Specific test file
python -m pytest tests/test_color_utils.py

# With coverage
python -m pytest --cov=. tests/
```

---

## 🛠️ Technology Stack

- **Backend**: Flask 3.0, Python 3.11+
- **Database**: SQLAlchemy with SQLite
- **Image Processing**: OpenCV, Pillow, NumPy
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Custom CSS with CSS Variables
- **Icons**: Font Awesome 6
- **Deployment**: Gunicorn, Docker

---

## 📊 Project Structure

```
pythonProject7/
├── app.py                 # Main application
├── config.py              # Configuration
├── models.py              # Database models
├── routes.py              # API routes
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
├── utils/
│   ├── __init__.py
│   ├── color_utils.py    # Color processing
│   └── image_processing.py # Image handling
├── templates/
│   └── index.html        # Main HTML
├── static/
│   ├── styles.css        # Styles
│   └── app.js           # Frontend JavaScript
└── tests/
    ├── __init__.py
    ├── test_color_utils.py
    └── test_api.py
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

Created with ❤️ by [Your Name]

---

## 🙏 Acknowledgments

- Color theory algorithms based on standard color harmony principles
- WCAG accessibility guidelines
- Flask and Python community

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

</div>

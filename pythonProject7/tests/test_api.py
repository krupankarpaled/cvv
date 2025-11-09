"""Tests for API endpoints."""
import unittest
import json
import base64
from io import BytesIO
from PIL import Image

from app import app
from models import db


class TestAPI(unittest.TestCase):
    """Test cases for API endpoints."""

    def setUp(self):
        """Set up test client and database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after tests."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_image(self, color=(255, 0, 0)):
        """Create a test image with specified color."""
        img = Image.new('RGB', (100, 100), color)
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f'data:image/jpeg;base64,{img_str}'

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_api_info(self):
        """Test API info endpoint."""
        response = self.app.get('/api/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('endpoints', data)

    def test_detect_color(self):
        """Test color detection endpoint."""
        image_data = self.create_test_image()
        response = self.app.post(
            '/api/detect',
            data=json.dumps({'image': image_data}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('color', data)
        self.assertIn('schemes', data)

    def test_detect_invalid_data(self):
        """Test detection with invalid data."""
        response = self.app.post(
            '/api/detect',
            data=json.dumps({'invalid': 'data'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_get_history(self):
        """Test getting color history."""
        response = self.app.get('/api/history')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('history', data)

    def test_analyze_color(self):
        """Test color analysis endpoint."""
        response = self.app.post(
            '/api/analyze',
            data=json.dumps({'hex': '#ff0000'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('color', data)

    def test_get_palettes(self):
        """Test getting palettes."""
        response = self.app.get('/api/palettes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])


if __name__ == '__main__':
    unittest.main()

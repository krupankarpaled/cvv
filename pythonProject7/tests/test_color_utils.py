"""Tests for color utility functions."""
import unittest
from utils.color_utils import (
    bgr_to_hex, hex_to_rgb, rgb_to_hex, rgb_to_hsl, rgb_to_hsv,
    rgb_to_cmyk, nearest_color_name, get_complementary_color,
    get_analogous_colors, get_triadic_colors, calculate_contrast_ratio
)


class TestColorUtils(unittest.TestCase):
    """Test cases for color utility functions."""

    def test_rgb_to_hex(self):
        """Test RGB to hex conversion."""
        self.assertEqual(rgb_to_hex((255, 0, 0)), '#ff0000')
        self.assertEqual(rgb_to_hex((0, 255, 0)), '#00ff00')
        self.assertEqual(rgb_to_hex((0, 0, 255)), '#0000ff')
        self.assertEqual(rgb_to_hex((255, 255, 255)), '#ffffff')
        self.assertEqual(rgb_to_hex((0, 0, 0)), '#000000')

    def test_hex_to_rgb(self):
        """Test hex to RGB conversion."""
        self.assertEqual(hex_to_rgb('#ff0000'), (255, 0, 0))
        self.assertEqual(hex_to_rgb('#00ff00'), (0, 255, 0))
        self.assertEqual(hex_to_rgb('#0000ff'), (0, 0, 255))
        self.assertEqual(hex_to_rgb('ffffff'), (255, 255, 255))

    def test_rgb_to_hsl(self):
        """Test RGB to HSL conversion."""
        result = rgb_to_hsl((255, 0, 0))
        self.assertEqual(result['h'], 0)
        self.assertEqual(result['s'], 100)
        self.assertEqual(result['l'], 50)

    def test_rgb_to_hsv(self):
        """Test RGB to HSV conversion."""
        result = rgb_to_hsv((255, 0, 0))
        self.assertEqual(result['h'], 0)
        self.assertEqual(result['s'], 100)
        self.assertEqual(result['v'], 100)

    def test_rgb_to_cmyk(self):
        """Test RGB to CMYK conversion."""
        result = rgb_to_cmyk((255, 0, 0))
        self.assertEqual(result['c'], 0)
        self.assertEqual(result['m'], 100)
        self.assertEqual(result['y'], 100)
        self.assertEqual(result['k'], 0)

    def test_nearest_color_name(self):
        """Test finding nearest color name."""
        name, hex_code = nearest_color_name((255, 0, 0))
        self.assertEqual(name, 'Red')

    def test_complementary_color(self):
        """Test complementary color generation."""
        complementary = get_complementary_color((255, 0, 0))
        self.assertEqual(len(complementary), 3)
        self.assertTrue(all(0 <= c <= 255 for c in complementary))

    def test_analogous_colors(self):
        """Test analogous colors generation."""
        colors = get_analogous_colors((255, 0, 0), 2)
        self.assertEqual(len(colors), 4)
        for color in colors:
            self.assertEqual(len(color), 3)
            self.assertTrue(all(0 <= c <= 255 for c in color))

    def test_triadic_colors(self):
        """Test triadic colors generation."""
        colors = get_triadic_colors((255, 0, 0))
        self.assertEqual(len(colors), 2)
        for color in colors:
            self.assertEqual(len(color), 3)

    def test_contrast_ratio(self):
        """Test WCAG contrast ratio calculation."""
        ratio = calculate_contrast_ratio((0, 0, 0), (255, 255, 255))
        self.assertEqual(ratio, 21.0)  # Maximum contrast
        
        ratio = calculate_contrast_ratio((255, 255, 255), (255, 255, 255))
        self.assertEqual(ratio, 1.0)  # No contrast


if __name__ == '__main__':
    unittest.main()

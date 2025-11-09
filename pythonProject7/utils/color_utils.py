"""Advanced color utility functions for color detection and manipulation."""
import colorsys
import numpy as np
from typing import List, Dict, Tuple, Optional


# Extended color database
COLOR_DB = {
    "Black": "#000000", "White": "#FFFFFF", "Beige": "#F5F5DC", "Gray": "#808080",
    "Navy": "#000080", "Denim": "#1560BD", "Coral": "#FF7F50", "Mustard": "#FFDB58",
    "Olive": "#808000", "Emerald": "#50C878", "Plum": "#8E4585", "Teal": "#008080",
    "Maroon": "#800000", "Gold": "#FFD700", "Tan": "#D2B48C", "Cream": "#FFFDD0",
    "Rust": "#B7410E", "Blush": "#DE5D83", "Sky Blue": "#87CEEB", "Khaki": "#C3B091",
    "AliceBlue": "#F0F8FF", "AntiqueWhite": "#FAEBD7", "Aqua": "#00FFFF", "Aquamarine": "#7FFFD4",
    "Azure": "#F0FFFF", "Bisque": "#FFE4C4", "BlanchedAlmond": "#FFEBCD", "Blue": "#0000FF",
    "BlueViolet": "#8A2BE2", "Brown": "#A52A2A", "BurlyWood": "#DEB887", "CadetBlue": "#5F9EA0",
    "Chartreuse": "#7FFF00", "Chocolate": "#D2691E", "CornflowerBlue": "#6495ED",
    "Crimson": "#DC143C", "Cyan": "#00FFFF", "DarkBlue": "#00008B", "DarkCyan": "#008B8B",
    "DarkGoldenRod": "#B8860B", "DarkGray": "#A9A9A9", "DarkGreen": "#006400",
    "DarkKhaki": "#BDB76B", "DarkMagenta": "#8B008B", "DarkOliveGreen": "#556B2F",
    "DarkOrange": "#FF8C00", "DarkOrchid": "#9932CC", "DarkRed": "#8B0000", "DarkSalmon": "#E9967A",
    "DarkSeaGreen": "#8FBC8F", "DarkSlateBlue": "#483D8B", "DarkSlateGray": "#2F4F4F",
    "DarkTurquoise": "#00CED1", "DarkViolet": "#9400D3", "DeepPink": "#FF1493",
    "DeepSkyBlue": "#00BFFF", "DimGray": "#696969", "DodgerBlue": "#1E90FF", "FireBrick": "#B22222",
    "ForestGreen": "#228B22", "Fuchsia": "#FF00FF", "Gainsboro": "#DCDCDC", "GhostWhite": "#F8F8FF",
    "GoldenRod": "#DAA520", "Green": "#008000", "GreenYellow": "#ADFF2F", "HoneyDew": "#F0FFF0",
    "HotPink": "#FF69B4", "IndianRed": "#CD5C5C", "Indigo": "#4B0082", "Ivory": "#FFFFF0",
    "Lavender": "#E6E6FA", "LavenderBlush": "#FFF0F5", "LawnGreen": "#7CFC00",
    "LemonChiffon": "#FFFACD", "LightBlue": "#ADD8E6", "LightCoral": "#F08080",
    "LightCyan": "#E0FFFF", "LightGoldenRodYellow": "#FAFAD2", "LightGray": "#D3D3D3",
    "LightGreen": "#90EE90", "LightPink": "#FFB6C1", "LightSalmon": "#FFA07A",
    "LightSeaGreen": "#20B2AA", "LightSkyBlue": "#87CEFA", "LightSlateGray": "#778899",
    "LightSteelBlue": "#B0C4DE", "LightYellow": "#FFFFE0", "Lime": "#00FF00",
    "LimeGreen": "#32CD32", "Linen": "#FAF0E6", "Magenta": "#FF00FF", "MediumAquaMarine": "#66CDAA",
    "MediumBlue": "#0000CD", "MediumOrchid": "#BA55D3", "MediumPurple": "#9370DB",
    "MediumSeaGreen": "#3CB371", "MediumSlateBlue": "#7B68EE", "MediumSpringGreen": "#00FA9A",
    "MediumTurquoise": "#48D1CC", "MediumVioletRed": "#C71585", "MidnightBlue": "#191970",
    "MintCream": "#F5FFFA", "MistyRose": "#FFE4E1", "Moccasin": "#FFE4B5", "NavajoWhite": "#FFDEAD",
    "OldLace": "#FDF5E6", "OliveDrab": "#6B8E23", "Orange": "#FFA500", "OrangeRed": "#FF4500",
    "Orchid": "#DA70D6", "PaleGoldenRod": "#EEE8AA", "PaleGreen": "#98FB98",
    "PaleTurquoise": "#AFEEEE", "PaleVioletRed": "#DB7093", "PapayaWhip": "#FFEFD5",
    "PeachPuff": "#FFDAB9", "Peru": "#CD853F", "Pink": "#FFC0CB", "PowderBlue": "#B0E0E6",
    "Purple": "#800080", "RebeccaPurple": "#663399", "Red": "#FF0000", "RosyBrown": "#BC8F8F",
    "RoyalBlue": "#4169E1", "SaddleBrown": "#8B4513", "Salmon": "#FA8072", "SandyBrown": "#F4A460",
    "SeaGreen": "#2E8B57", "SeaShell": "#FFF5EE", "Sienna": "#A0522D", "Silver": "#C0C0C0",
    "SlateBlue": "#6A5ACD", "SlateGray": "#708090", "Snow": "#FFFAFA", "SpringGreen": "#00FF7F",
    "SteelBlue": "#4682B4", "Thistle": "#D8BFD8", "Tomato": "#FF6347", "Turquoise": "#40E0D0",
    "Violet": "#EE82EE", "Wheat": "#F5DEB3", "Yellow": "#FFFF00", "YellowGreen": "#9ACD32"
}


def bgr_to_hex(bgr: Tuple[int, int, int]) -> str:
    """Convert BGR color to hex string."""
    b, g, r = map(int, bgr)
    return '#%02x%02x%02x' % (r, g, b)


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    h = hex_code.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex string."""
    r, g, b = map(int, rgb)
    return '#%02x%02x%02x' % (r, g, b)


def rgb_to_hsl(rgb: Tuple[int, int, int]) -> Dict[str, float]:
    """Convert RGB to HSL."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return {
        'h': round(h * 360, 1),
        's': round(s * 100, 1),
        'l': round(l * 100, 1)
    }


def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Dict[str, float]:
    """Convert RGB to HSV."""
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return {
        'h': round(h * 360, 1),
        's': round(s * 100, 1),
        'v': round(v * 100, 1)
    }


def rgb_to_cmyk(rgb: Tuple[int, int, int]) -> Dict[str, float]:
    """Convert RGB to CMYK."""
    r, g, b = [x / 255.0 for x in rgb]
    k = 1 - max(r, g, b)
    if k == 1:
        return {'c': 0, 'm': 0, 'y': 0, 'k': 100}
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return {
        'c': round(c * 100, 1),
        'm': round(m * 100, 1),
        'y': round(y * 100, 1),
        'k': round(k * 100, 1)
    }


def nearest_color_name(rgb: Tuple[int, int, int]) -> Tuple[str, str]:
    """Find nearest color name from COLOR_DB by Euclidean distance."""
    r0, g0, b0 = rgb
    best = (None, None, float('inf'))
    
    for name, hex_code in COLOR_DB.items():
        r1, g1, b1 = hex_to_rgb(hex_code)
        distance = (r0 - r1)**2 + (g0 - g1)**2 + (b0 - b1)**2
        if distance < best[2]:
            best = (name, hex_code, distance)
    
    return best[0], best[1]


def get_complementary_color(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """Get complementary color (opposite on color wheel)."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + 0.5) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def get_analogous_colors(rgb: Tuple[int, int, int], count: int = 2) -> List[Tuple[int, int, int]]:
    """Get analogous colors (adjacent on color wheel)."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    colors = []
    step = 30 / 360  # 30 degrees
    for i in range(1, count + 1):
        h1 = (h + step * i) % 1.0
        h2 = (h - step * i) % 1.0
        
        r1, g1, b1 = colorsys.hls_to_rgb(h1, l, s)
        colors.append((int(r1 * 255), int(g1 * 255), int(b1 * 255)))
        
        if len(colors) < count * 2:
            r2, g2, b2 = colorsys.hls_to_rgb(h2, l, s)
            colors.append((int(r2 * 255), int(g2 * 255), int(b2 * 255)))
    
    return colors[:count * 2]


def get_triadic_colors(rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Get triadic colors (120 degrees apart on color wheel)."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    colors = []
    for offset in [120, 240]:
        h_new = (h + offset / 360) % 1.0
        r_new, g_new, b_new = colorsys.hls_to_rgb(h_new, l, s)
        colors.append((int(r_new * 255), int(g_new * 255), int(b_new * 255)))
    
    return colors


def get_tetradic_colors(rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Get tetradic/square colors (90 degrees apart on color wheel)."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    colors = []
    for offset in [90, 180, 270]:
        h_new = (h + offset / 360) % 1.0
        r_new, g_new, b_new = colorsys.hls_to_rgb(h_new, l, s)
        colors.append((int(r_new * 255), int(g_new * 255), int(b_new * 255)))
    
    return colors


def get_monochromatic_palette(rgb: Tuple[int, int, int], count: int = 5) -> List[Tuple[int, int, int]]:
    """Generate monochromatic palette by varying lightness."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    palette = []
    for i in range(count):
        l_new = (i + 1) / (count + 1)
        r_new, g_new, b_new = colorsys.hls_to_rgb(h, l_new, s)
        palette.append((int(r_new * 255), int(g_new * 255), int(b_new * 255)))
    
    return palette


def get_shades_and_tints(rgb: Tuple[int, int, int], count: int = 3) -> Dict[str, List[Tuple[int, int, int]]]:
    """Get shades (darker) and tints (lighter) of a color."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    shades = []
    tints = []
    
    for i in range(1, count + 1):
        # Shades - decrease lightness
        l_shade = max(0, l - (i * 0.15))
        r_s, g_s, b_s = colorsys.hls_to_rgb(h, l_shade, s)
        shades.append((int(r_s * 255), int(g_s * 255), int(b_s * 255)))
        
        # Tints - increase lightness
        l_tint = min(1, l + (i * 0.15))
        r_t, g_t, b_t = colorsys.hls_to_rgb(h, l_tint, s)
        tints.append((int(r_t * 255), int(g_t * 255), int(b_t * 255)))
    
    return {'shades': shades, 'tints': tints}


def get_split_complementary(rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Get split complementary colors."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    colors = []
    for offset in [150, 210]:
        h_new = (h + offset / 360) % 1.0
        r_new, g_new, b_new = colorsys.hls_to_rgb(h_new, l, s)
        colors.append((int(r_new * 255), int(g_new * 255), int(b_new * 255)))
    
    return colors


def calculate_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    def relative_luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return round((lighter + 0.05) / (darker + 0.05), 2)


def get_accessibility_info(rgb: Tuple[int, int, int]) -> Dict:
    """Get WCAG accessibility information for a color against white and black."""
    white_ratio = calculate_contrast_ratio(rgb, (255, 255, 255))
    black_ratio = calculate_contrast_ratio(rgb, (0, 0, 0))
    
    return {
        'white_background': {
            'ratio': white_ratio,
            'aa_normal': white_ratio >= 4.5,
            'aa_large': white_ratio >= 3,
            'aaa_normal': white_ratio >= 7,
            'aaa_large': white_ratio >= 4.5
        },
        'black_background': {
            'ratio': black_ratio,
            'aa_normal': black_ratio >= 4.5,
            'aa_large': black_ratio >= 3,
            'aaa_normal': black_ratio >= 7,
            'aaa_large': black_ratio >= 4.5
        }
    }


def get_color_temperature(rgb: Tuple[int, int, int]) -> Dict:
    """Determine if a color is warm or cool."""
    r, g, b = rgb
    
    # Simple heuristic based on red vs blue
    warmth = r - b
    
    if warmth > 50:
        temp = "warm"
        description = "This color has warm tones"
    elif warmth < -50:
        temp = "cool"
        description = "This color has cool tones"
    else:
        temp = "neutral"
        description = "This color is neutral in temperature"
    
    return {
        'temperature': temp,
        'warmth_value': warmth,
        'description': description
    }


def format_color_info(rgb: Tuple[int, int, int], hex_code: str, name: str) -> Dict:
    """Format comprehensive color information."""
    return {
        'hex': hex_code,
        'name': name,
        'rgb': {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]},
        'hsl': rgb_to_hsl(rgb),
        'hsv': rgb_to_hsv(rgb),
        'cmyk': rgb_to_cmyk(rgb),
        'temperature': get_color_temperature(rgb),
        'accessibility': get_accessibility_info(rgb)
    }

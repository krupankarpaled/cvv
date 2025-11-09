"""Gradient generation utilities."""
import colorsys
from typing import List, Dict, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}".upper()


def interpolate_colors(color1: str, color2: str, steps: int = 10, method: str = 'rgb') -> List[Dict]:
    """
    Interpolate between two colors.
    
    Args:
        color1: Start color (hex)
        color2: End color (hex)
        steps: Number of intermediate colors
        method: 'rgb', 'hsl', or 'hsv'
    
    Returns:
        List of interpolated colors
    """
    colors = []
    
    if method == 'rgb':
        colors = _interpolate_rgb(color1, color2, steps)
    elif method == 'hsl':
        colors = _interpolate_hsl(color1, color2, steps)
    elif method == 'hsv':
        colors = _interpolate_hsv(color1, color2, steps)
    else:
        colors = _interpolate_rgb(color1, color2, steps)
    
    return colors


def _interpolate_rgb(color1: str, color2: str, steps: int) -> List[Dict]:
    """Interpolate in RGB color space."""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    colors = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        r = rgb1[0] + (rgb2[0] - rgb1[0]) * t
        g = rgb1[1] + (rgb2[1] - rgb1[1]) * t
        b = rgb1[2] + (rgb2[2] - rgb1[2]) * t
        
        hex_color = rgb_to_hex(r, g, b)
        colors.append({
            "hex": hex_color,
            "rgb": {"r": int(r), "g": int(g), "b": int(b)},
            "position": round(t * 100, 1)
        })
    
    return colors


def _interpolate_hsl(color1: str, color2: str, steps: int) -> List[Dict]:
    """Interpolate in HSL color space."""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    # Convert to HSL
    h1, l1, s1 = colorsys.rgb_to_hls(rgb1[0]/255, rgb1[1]/255, rgb1[2]/255)
    h2, l2, s2 = colorsys.rgb_to_hls(rgb2[0]/255, rgb2[1]/255, rgb2[2]/255)
    
    colors = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        
        # Interpolate HSL values
        h = h1 + (h2 - h1) * t
        l = l1 + (l2 - l1) * t
        s = s1 + (s2 - s1) * t
        
        # Convert back to RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        hex_color = rgb_to_hex(r, g, b)
        colors.append({
            "hex": hex_color,
            "rgb": {"r": r, "g": g, "b": b},
            "position": round(t * 100, 1)
        })
    
    return colors


def _interpolate_hsv(color1: str, color2: str, steps: int) -> List[Dict]:
    """Interpolate in HSV color space."""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    # Convert to HSV
    h1, s1, v1 = colorsys.rgb_to_hsv(rgb1[0]/255, rgb1[1]/255, rgb1[2]/255)
    h2, s2, v2 = colorsys.rgb_to_hsv(rgb2[0]/255, rgb2[1]/255, rgb2[2]/255)
    
    colors = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        
        # Interpolate HSV values
        h = h1 + (h2 - h1) * t
        s = s1 + (s2 - s1) * t
        v = v1 + (v2 - v1) * t
        
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        hex_color = rgb_to_hex(r, g, b)
        colors.append({
            "hex": hex_color,
            "rgb": {"r": r, "g": g, "b": b},
            "position": round(t * 100, 1)
        })
    
    return colors


def generate_gradient(colors: List[str], steps: int = 10, method: str = 'rgb') -> Dict:
    """
    Generate a gradient through multiple colors.
    
    Args:
        colors: List of hex colors
        steps: Total number of gradient stops
        method: Interpolation method
    
    Returns:
        Gradient data with colors and CSS
    """
    if len(colors) < 2:
        return {"error": "Need at least 2 colors"}
    
    # Calculate steps between each pair of colors
    segments = len(colors) - 1
    steps_per_segment = max(2, steps // segments)
    
    gradient_colors = []
    
    for i in range(segments):
        segment_colors = interpolate_colors(
            colors[i], 
            colors[i + 1], 
            steps_per_segment,
            method
        )
        
        # Avoid duplicates at segment boundaries
        if i > 0:
            segment_colors = segment_colors[1:]
        
        gradient_colors.extend(segment_colors)
    
    # Generate CSS
    css = generate_gradient_css(gradient_colors, 'linear', 90)
    
    return {
        "success": True,
        "colors": gradient_colors,
        "css": css,
        "method": method
    }


def generate_gradient_css(colors: List[Dict], gradient_type: str = 'linear', 
                         angle: int = 90, center_x: int = 50, center_y: int = 50) -> Dict:
    """
    Generate CSS for gradients.
    
    Args:
        colors: List of color dictionaries with hex and position
        gradient_type: 'linear', 'radial', or 'conic'
        angle: Angle for linear gradient (degrees)
        center_x: X position for radial/conic (percentage)
        center_y: Y position for radial/conic (percentage)
    
    Returns:
        Dictionary with CSS code
    """
    color_stops = [f"{c['hex']} {c['position']}%" for c in colors]
    
    if gradient_type == 'linear':
        css = f"linear-gradient({angle}deg, {', '.join(color_stops)})"
        
    elif gradient_type == 'radial':
        css = f"radial-gradient(circle at {center_x}% {center_y}%, {', '.join(color_stops)})"
        
    elif gradient_type == 'conic':
        css = f"conic-gradient(from {angle}deg at {center_x}% {center_y}%, {', '.join(color_stops)})"
    else:
        css = f"linear-gradient({angle}deg, {', '.join(color_stops)})"
    
    return {
        "background": css,
        "background_image": css,
        "full_css": f"background: {css};",
        "type": gradient_type
    }


def generate_preset_gradients() -> List[Dict]:
    """Generate preset beautiful gradients."""
    presets = [
        {
            "name": "Sunset",
            "colors": ["#FF6B6B", "#FFD93D", "#6BCF7F"]
        },
        {
            "name": "Ocean",
            "colors": ["#667EEA", "#764BA2", "#F093FB"]
        },
        {
            "name": "Forest",
            "colors": ["#134E5E", "#71B280"]
        },
        {
            "name": "Fire",
            "colors": ["#FF0000", "#FF7F00", "#FFFF00"]
        },
        {
            "name": "Purple Dream",
            "colors": ["#C471F5", "#FA71CD"]
        },
        {
            "name": "Cool Blues",
            "colors": ["#2196F3", "#00BCD4", "#009688"]
        },
        {
            "name": "Warm Sunset",
            "colors": ["#F2994A", "#F2C94C", "#EB5757"]
        },
        {
            "name": "Green Grass",
            "colors": ["#56AB2F", "#A8E063"]
        },
        {
            "name": "Royal",
            "colors": ["#141E30", "#243B55"]
        },
        {
            "name": "Cherry",
            "colors": ["#EB3349", "#F45C43"]
        }
    ]
    
    result = []
    for preset in presets:
        gradient_data = generate_gradient(preset["colors"], steps=20, method='rgb')
        if gradient_data.get("success"):
            result.append({
                "name": preset["name"],
                "colors": preset["colors"],
                "gradient": gradient_data["colors"],
                "css": gradient_data["css"]
            })
    
    return result


def generate_custom_gradient(start_color: str, end_color: str, steps: int = 10,
                            gradient_type: str = 'linear', angle: int = 90) -> Dict:
    """Generate a custom gradient with CSS output."""
    colors = interpolate_colors(start_color, end_color, steps, method='rgb')
    css = generate_gradient_css(colors, gradient_type, angle)
    
    return {
        "success": True,
        "colors": colors,
        "css": css,
        "start": start_color,
        "end": end_color,
        "steps": steps
    }

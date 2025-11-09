"""Color mixing utilities - simulate physical paint mixing."""
import numpy as np
import colorsys
from typing import Dict, List, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}".upper()


def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
    """Convert RGB to CMYK."""
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 100
    
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    k = 1 - max(r_norm, g_norm, b_norm)
    c = (1 - r_norm - k) / (1 - k) if k < 1 else 0
    m = (1 - g_norm - k) / (1 - k) if k < 1 else 0
    y = (1 - b_norm - k) / (1 - k) if k < 1 else 0
    
    return c * 100, m * 100, y * 100, k * 100


def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
    """Convert CMYK to RGB."""
    c = c / 100.0
    m = m / 100.0
    y = y / 100.0
    k = k / 100.0
    
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    
    return int(r), int(g), int(b)


def mix_colors_rgb(colors: List[str], ratios: List[float] = None) -> Dict:
    """
    Mix colors in RGB space (simple averaging).
    
    Args:
        colors: List of hex colors
        ratios: Optional mixing ratios (must sum to 1.0)
    
    Returns:
        Mixed color information
    """
    if not colors:
        return {"success": False, "error": "No colors provided"}
    
    # Default to equal ratios
    if ratios is None:
        ratios = [1.0 / len(colors)] * len(colors)
    
    # Normalize ratios
    total = sum(ratios)
    ratios = [r / total for r in ratios]
    
    # Convert to RGB
    rgb_colors = [hex_to_rgb(c) for c in colors]
    
    # Mix
    mixed_r = sum(rgb[0] * ratio for rgb, ratio in zip(rgb_colors, ratios))
    mixed_g = sum(rgb[1] * ratio for rgb, ratio in zip(rgb_colors, ratios))
    mixed_b = sum(rgb[2] * ratio for rgb, ratio in zip(rgb_colors, ratios))
    
    mixed_hex = rgb_to_hex(mixed_r, mixed_g, mixed_b)
    
    return {
        "success": True,
        "method": "rgb",
        "mixed_color": {
            "hex": mixed_hex,
            "rgb": {"r": int(mixed_r), "g": int(mixed_g), "b": int(mixed_b)}
        },
        "input_colors": colors,
        "ratios": ratios
    }


def mix_colors_cmyk(colors: List[str], ratios: List[float] = None) -> Dict:
    """
    Mix colors in CMYK space (more like physical paint mixing).
    
    Args:
        colors: List of hex colors
        ratios: Optional mixing ratios
    
    Returns:
        Mixed color information
    """
    if not colors:
        return {"success": False, "error": "No colors provided"}
    
    if ratios is None:
        ratios = [1.0 / len(colors)] * len(colors)
    
    # Normalize ratios
    total = sum(ratios)
    ratios = [r / total for r in ratios]
    
    # Convert to CMYK
    cmyk_colors = [rgb_to_cmyk(*hex_to_rgb(c)) for c in colors]
    
    # Mix in CMYK space
    mixed_c = sum(cmyk[0] * ratio for cmyk, ratio in zip(cmyk_colors, ratios))
    mixed_m = sum(cmyk[1] * ratio for cmyk, ratio in zip(cmyk_colors, ratios))
    mixed_y = sum(cmyk[2] * ratio for cmyk, ratio in zip(cmyk_colors, ratios))
    mixed_k = sum(cmyk[3] * ratio for cmyk, ratio in zip(cmyk_colors, ratios))
    
    # Convert back to RGB
    mixed_rgb = cmyk_to_rgb(mixed_c, mixed_m, mixed_y, mixed_k)
    mixed_hex = rgb_to_hex(*mixed_rgb)
    
    return {
        "success": True,
        "method": "cmyk",
        "mixed_color": {
            "hex": mixed_hex,
            "rgb": {"r": mixed_rgb[0], "g": mixed_rgb[1], "b": mixed_rgb[2]},
            "cmyk": {"c": round(mixed_c, 1), "m": round(mixed_m, 1), 
                    "y": round(mixed_y, 1), "k": round(mixed_k, 1)}
        },
        "input_colors": colors,
        "ratios": ratios
    }


def mix_colors_hsl(colors: List[str], ratios: List[float] = None) -> Dict:
    """
    Mix colors in HSL space.
    
    Args:
        colors: List of hex colors
        ratios: Optional mixing ratios
    
    Returns:
        Mixed color information
    """
    if not colors:
        return {"success": False, "error": "No colors provided"}
    
    if ratios is None:
        ratios = [1.0 / len(colors)] * len(colors)
    
    # Normalize ratios
    total = sum(ratios)
    ratios = [r / total for r in ratios]
    
    # Convert to HSL
    hsl_colors = []
    for color in colors:
        rgb = hex_to_rgb(color)
        h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        hsl_colors.append((h, s, l))
    
    # Mix in HSL space
    mixed_h = sum(hsl[0] * ratio for hsl, ratio in zip(hsl_colors, ratios))
    mixed_s = sum(hsl[1] * ratio for hsl, ratio in zip(hsl_colors, ratios))
    mixed_l = sum(hsl[2] * ratio for hsl, ratio in zip(hsl_colors, ratios))
    
    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(mixed_h, mixed_l, mixed_s)
    mixed_rgb = (int(r * 255), int(g * 255), int(b * 255))
    mixed_hex = rgb_to_hex(*mixed_rgb)
    
    return {
        "success": True,
        "method": "hsl",
        "mixed_color": {
            "hex": mixed_hex,
            "rgb": {"r": mixed_rgb[0], "g": mixed_rgb[1], "b": mixed_rgb[2]},
            "hsl": {
                "h": round(mixed_h * 360, 1),
                "s": round(mixed_s * 100, 1),
                "l": round(mixed_l * 100, 1)
            }
        },
        "input_colors": colors,
        "ratios": ratios
    }


def mix_colors_subtractive(colors: List[str], ratios: List[float] = None) -> Dict:
    """
    Subtractive color mixing (like physical paint).
    Uses Kubelka-Munk theory approximation.
    
    Args:
        colors: List of hex colors
        ratios: Optional mixing ratios
    
    Returns:
        Mixed color information
    """
    if not colors:
        return {"success": False, "error": "No colors provided"}
    
    if ratios is None:
        ratios = [1.0 / len(colors)] * len(colors)
    
    # Normalize ratios
    total = sum(ratios)
    ratios = [r / total for r in ratios]
    
    # Convert to reflectance (simplified Kubelka-Munk)
    rgb_colors = [hex_to_rgb(c) for c in colors]
    
    # Calculate weighted reflectance
    mixed_r = 0
    mixed_g = 0
    mixed_b = 0
    
    for rgb, ratio in zip(rgb_colors, ratios):
        # Approximate reflectance
        r_reflect = (rgb[0] / 255.0) ** 2
        g_reflect = (rgb[1] / 255.0) ** 2
        b_reflect = (rgb[2] / 255.0) ** 2
        
        mixed_r += r_reflect * ratio
        mixed_g += g_reflect * ratio
        mixed_b += b_reflect * ratio
    
    # Convert back to RGB
    mixed_r = int(np.sqrt(mixed_r) * 255)
    mixed_g = int(np.sqrt(mixed_g) * 255)
    mixed_b = int(np.sqrt(mixed_b) * 255)
    
    mixed_hex = rgb_to_hex(mixed_r, mixed_g, mixed_b)
    
    return {
        "success": True,
        "method": "subtractive",
        "mixed_color": {
            "hex": mixed_hex,
            "rgb": {"r": mixed_r, "g": mixed_g, "b": mixed_b}
        },
        "input_colors": colors,
        "ratios": ratios,
        "description": "Physical paint-like mixing"
    }


def mix_two_colors_interactive(color1: str, color2: str, ratio: float = 0.5) -> Dict:
    """
    Mix two colors with variable ratio (0 = all color1, 1 = all color2).
    Provides results for all mixing methods.
    
    Args:
        color1: First hex color
        color2: Second hex color
        ratio: Mix ratio (0.0 to 1.0)
    
    Returns:
        Mixed colors using different methods
    """
    ratio = max(0, min(1, ratio))  # Clamp to 0-1
    colors = [color1, color2]
    ratios = [1 - ratio, ratio]
    
    return {
        "success": True,
        "color1": color1.upper(),
        "color2": color2.upper(),
        "ratio": ratio,
        "results": {
            "rgb": mix_colors_rgb(colors, ratios),
            "cmyk": mix_colors_cmyk(colors, ratios),
            "hsl": mix_colors_hsl(colors, ratios),
            "subtractive": mix_colors_subtractive(colors, ratios)
        },
        "recommendation": "Use 'subtractive' or 'cmyk' for realistic paint mixing"
    }


def create_color_palette_mix(base_colors: List[str], variations: int = 5) -> Dict:
    """
    Create a palette by mixing base colors in various ratios.
    
    Args:
        base_colors: List of base hex colors
        variations: Number of variations to generate
    
    Returns:
        Generated palette
    """
    if len(base_colors) < 2:
        return {"success": False, "error": "Need at least 2 base colors"}
    
    palette = []
    
    # Generate variations by mixing pairs
    for i in range(len(base_colors)):
        for j in range(i + 1, len(base_colors)):
            color1 = base_colors[i]
            color2 = base_colors[j]
            
            for k in range(variations):
                ratio = k / (variations - 1) if variations > 1 else 0.5
                result = mix_colors_subtractive([color1, color2], [1 - ratio, ratio])
                
                if result.get("success"):
                    palette.append({
                        "hex": result["mixed_color"]["hex"],
                        "rgb": result["mixed_color"]["rgb"],
                        "from": [color1, color2],
                        "ratio": round(ratio, 2)
                    })
    
    return {
        "success": True,
        "base_colors": base_colors,
        "palette": palette,
        "count": len(palette)
    }

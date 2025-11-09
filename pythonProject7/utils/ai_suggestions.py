"""AI-powered color suggestions and recommendations."""
import colorsys
import numpy as np
from typing import List, Dict, Tuple
import random


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}".upper()


# Industry-specific color palettes
INDUSTRY_PALETTES = {
    "tech": {
        "colors": ["#0066CC", "#00D4FF", "#6C63FF", "#1E1E1E", "#FFFFFF"],
        "description": "Modern, clean, professional tech colors",
        "keywords": ["innovation", "trust", "digital"]
    },
    "healthcare": {
        "colors": ["#00A896", "#02C39A", "#05668D", "#F0F3BD", "#FFFFFF"],
        "description": "Calm, trustworthy, clean medical colors",
        "keywords": ["health", "care", "trust", "clean"]
    },
    "finance": {
        "colors": ["#003F5C", "#2F4B7C", "#665191", "#A05195", "#D45087"],
        "description": "Professional, stable, trustworthy",
        "keywords": ["trust", "stability", "professional"]
    },
    "food": {
        "colors": ["#FF6B6B", "#FFA500", "#FFDD00", "#7FBA00", "#00B159"],
        "description": "Appetizing, fresh, vibrant",
        "keywords": ["fresh", "appetizing", "natural"]
    },
    "fashion": {
        "colors": ["#1A1A1D", "#4E4E50", "#6F2232", "#950740", "#C3073F"],
        "description": "Bold, elegant, sophisticated",
        "keywords": ["elegant", "bold", "style"]
    },
    "education": {
        "colors": ["#F4A261", "#E76F51", "#2A9D8F", "#264653", "#E9C46A"],
        "description": "Friendly, engaging, warm",
        "keywords": ["learning", "growth", "friendly"]
    },
    "eco": {
        "colors": ["#2D6A4F", "#40916C", "#52B788", "#74C69D", "#95D5B2"],
        "description": "Natural, sustainable, organic",
        "keywords": ["nature", "eco", "sustainable"]
    },
    "luxury": {
        "colors": ["#000000", "#1C1C1C", "#C9A961", "#8B7355", "#FFFFFF"],
        "description": "Premium, exclusive, elegant",
        "keywords": ["luxury", "premium", "exclusive"]
    },
    "creative": {
        "colors": ["#F72585", "#7209B7", "#3A0CA3", "#4361EE", "#4CC9F0"],
        "description": "Bold, vibrant, artistic",
        "keywords": ["creative", "artistic", "bold"]
    },
    "corporate": {
        "colors": ["#003049", "#D62828", "#F77F00", "#FCBF49", "#EAE2B7"],
        "description": "Professional, reliable, established",
        "keywords": ["professional", "corporate", "reliable"]
    }
}


# Mood-based color palettes
MOOD_PALETTES = {
    "calm": {
        "colors": ["#A8DADC", "#457B9D", "#1D3557", "#F1FAEE", "#E63946"],
        "description": "Peaceful and serene",
        "emotions": ["peaceful", "serene", "relaxed"]
    },
    "energetic": {
        "colors": ["#FF006E", "#FB5607", "#FFBE0B", "#8338EC", "#3A86FF"],
        "description": "Vibrant and dynamic",
        "emotions": ["energetic", "dynamic", "exciting"]
    },
    "professional": {
        "colors": ["#14213D", "#FCA311", "#E5E5E5", "#FFFFFF", "#000000"],
        "description": "Serious and trustworthy",
        "emotions": ["professional", "trustworthy", "serious"]
    },
    "playful": {
        "colors": ["#FFB5E8", "#FF9CEE", "#FFCCF9", "#FCC2FF", "#F6A6FF"],
        "description": "Fun and lighthearted",
        "emotions": ["playful", "fun", "lighthearted"]
    },
    "elegant": {
        "colors": ["#2B2D42", "#8D99AE", "#EDF2F4", "#EF233C", "#D90429"],
        "description": "Sophisticated and refined",
        "emotions": ["elegant", "sophisticated", "refined"]
    },
    "warm": {
        "colors": ["#FFBA08", "#FAA307", "#F48C06", "#E85D04", "#DC2F02"],
        "description": "Cozy and inviting",
        "emotions": ["warm", "cozy", "inviting"]
    },
    "cool": {
        "colors": ["#023E8A", "#0077B6", "#0096C7", "#00B4D8", "#48CAE4"],
        "description": "Fresh and modern",
        "emotions": ["cool", "fresh", "modern"]
    },
    "nature": {
        "colors": ["#386641", "#6A994E", "#A7C957", "#F2E8CF", "#BC4749"],
        "description": "Natural and organic",
        "emotions": ["natural", "organic", "earthy"]
    }
}


def suggest_complementary_colors(hex_color: str, count: int = 5) -> Dict:
    """Suggest colors that work well with the given color."""
    rgb = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    suggestions = []
    
    # Complementary
    comp_h = (h + 0.5) % 1.0
    comp_rgb = colorsys.hsv_to_rgb(comp_h, s, v)
    suggestions.append({
        "hex": rgb_to_hex(int(comp_rgb[0]*255), int(comp_rgb[1]*255), int(comp_rgb[2]*255)),
        "relationship": "Complementary",
        "description": "Opposite on color wheel, creates high contrast"
    })
    
    # Analogous
    for offset in [-0.083, 0.083]:  # ±30 degrees
        ana_h = (h + offset) % 1.0
        ana_rgb = colorsys.hsv_to_rgb(ana_h, s, v)
        suggestions.append({
            "hex": rgb_to_hex(int(ana_rgb[0]*255), int(ana_rgb[1]*255), int(ana_rgb[2]*255)),
            "relationship": "Analogous",
            "description": "Adjacent colors, harmonious and pleasing"
        })
    
    # Lighter version
    light_rgb = colorsys.hsv_to_rgb(h, s * 0.6, min(1, v * 1.3))
    suggestions.append({
        "hex": rgb_to_hex(int(light_rgb[0]*255), int(light_rgb[1]*255), int(light_rgb[2]*255)),
        "relationship": "Tint",
        "description": "Lighter version, good for backgrounds"
    })
    
    # Darker version
    dark_rgb = colorsys.hsv_to_rgb(h, min(1, s * 1.2), v * 0.6)
    suggestions.append({
        "hex": rgb_to_hex(int(dark_rgb[0]*255), int(dark_rgb[1]*255), int(dark_rgb[2]*255)),
        "relationship": "Shade",
        "description": "Darker version, good for text/accents"
    })
    
    return {
        "success": True,
        "base_color": hex_color.upper(),
        "suggestions": suggestions[:count]
    }


def suggest_palette_by_mood(mood: str) -> Dict:
    """Suggest a color palette based on mood."""
    mood = mood.lower()
    
    if mood in MOOD_PALETTES:
        palette = MOOD_PALETTES[mood]
        return {
            "success": True,
            "mood": mood.title(),
            "colors": palette["colors"],
            "description": palette["description"],
            "emotions": palette["emotions"]
        }
    
    # If mood not found, return a random one
    random_mood = random.choice(list(MOOD_PALETTES.keys()))
    palette = MOOD_PALETTES[random_mood]
    
    return {
        "success": True,
        "mood": random_mood.title(),
        "colors": palette["colors"],
        "description": palette["description"],
        "emotions": palette["emotions"],
        "note": f"'{mood}' not found, showing '{random_mood}' instead"
    }


def suggest_palette_by_industry(industry: str) -> Dict:
    """Suggest a color palette based on industry."""
    industry = industry.lower()
    
    if industry in INDUSTRY_PALETTES:
        palette = INDUSTRY_PALETTES[industry]
        return {
            "success": True,
            "industry": industry.title(),
            "colors": palette["colors"],
            "description": palette["description"],
            "keywords": palette["keywords"]
        }
    
    # Return all industries if not found
    return {
        "success": False,
        "error": f"Industry '{industry}' not found",
        "available_industries": list(INDUSTRY_PALETTES.keys())
    }


def get_all_moods() -> Dict:
    """Get all available mood palettes."""
    return {
        "success": True,
        "moods": {
            mood: {
                "description": data["description"],
                "colors": data["colors"],
                "emotions": data["emotions"]
            }
            for mood, data in MOOD_PALETTES.items()
        }
    }


def get_all_industries() -> Dict:
    """Get all available industry palettes."""
    return {
        "success": True,
        "industries": {
            industry: {
                "description": data["description"],
                "colors": data["colors"],
                "keywords": data["keywords"]
            }
            for industry, data in INDUSTRY_PALETTES.items()
        }
    }


def suggest_text_color(background_hex: str) -> Dict:
    """Suggest optimal text color (black or white) for a background."""
    rgb = hex_to_rgb(background_hex)
    
    # Calculate relative luminance
    def get_luminance(r, g, b):
        rgb_normalized = [r/255, g/255, b/255]
        rgb_adjusted = []
        
        for val in rgb_normalized:
            if val <= 0.03928:
                rgb_adjusted.append(val / 12.92)
            else:
                rgb_adjusted.append(((val + 0.055) / 1.055) ** 2.4)
        
        return 0.2126 * rgb_adjusted[0] + 0.7152 * rgb_adjusted[1] + 0.0722 * rgb_adjusted[2]
    
    bg_luminance = get_luminance(*rgb)
    
    # Use white text for dark backgrounds, black for light
    if bg_luminance > 0.5:
        text_color = "#000000"
        contrast_ratio = (bg_luminance + 0.05) / (0.0 + 0.05)
    else:
        text_color = "#FFFFFF"
        contrast_ratio = (1.0 + 0.05) / (bg_luminance + 0.05)
    
    # WCAG compliance
    wcag_aa = contrast_ratio >= 4.5
    wcag_aaa = contrast_ratio >= 7.0
    
    return {
        "success": True,
        "background": background_hex.upper(),
        "suggested_text_color": text_color,
        "contrast_ratio": round(contrast_ratio, 2),
        "wcag_aa": wcag_aa,
        "wcag_aaa": wcag_aaa,
        "recommendation": "Excellent" if wcag_aaa else "Good" if wcag_aa else "Poor"
    }


def generate_smart_palette(base_color: str, palette_type: str = "balanced") -> Dict:
    """
    Generate a smart color palette using AI-like rules.
    
    Args:
        base_color: Base hex color
        palette_type: 'balanced', 'monochromatic', 'vibrant', 'pastel', 'dark'
    
    Returns:
        Generated palette
    """
    rgb = hex_to_rgb(base_color)
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    palette = []
    
    if palette_type == "monochromatic":
        # Variations in lightness/saturation
        for i in range(5):
            factor = (i + 1) / 6
            new_v = v * (0.3 + factor * 0.7)
            new_s = s * (0.5 + factor * 0.5)
            color_rgb = colorsys.hsv_to_rgb(h, new_s, new_v)
            palette.append(rgb_to_hex(int(color_rgb[0]*255), int(color_rgb[1]*255), int(color_rgb[2]*255)))
    
    elif palette_type == "vibrant":
        # High saturation variations
        for i in range(5):
            new_h = (h + i * 0.15) % 1.0
            color_rgb = colorsys.hsv_to_rgb(new_h, 0.9, 0.9)
            palette.append(rgb_to_hex(int(color_rgb[0]*255), int(color_rgb[1]*255), int(color_rgb[2]*255)))
    
    elif palette_type == "pastel":
        # Low saturation, high value
        for i in range(5):
            new_h = (h + i * 0.12) % 1.0
            color_rgb = colorsys.hsv_to_rgb(new_h, 0.3, 0.95)
            palette.append(rgb_to_hex(int(color_rgb[0]*255), int(color_rgb[1]*255), int(color_rgb[2]*255)))
    
    elif palette_type == "dark":
        # Low value variations
        for i in range(5):
            new_h = (h + i * 0.1) % 1.0
            color_rgb = colorsys.hsv_to_rgb(new_h, 0.7, 0.3 + i * 0.1)
            palette.append(rgb_to_hex(int(color_rgb[0]*255), int(color_rgb[1]*255), int(color_rgb[2]*255)))
    
    else:  # balanced
        # Mix of different harmony types
        palette = [
            base_color,
            # Complementary
            rgb_to_hex(*[int(c*255) for c in colorsys.hsv_to_rgb((h + 0.5) % 1.0, s, v)]),
            # Triadic
            rgb_to_hex(*[int(c*255) for c in colorsys.hsv_to_rgb((h + 0.333) % 1.0, s, v)]),
            # Light version
            rgb_to_hex(*[int(c*255) for c in colorsys.hsv_to_rgb(h, s * 0.5, min(1, v * 1.3))]),
            # Dark version
            rgb_to_hex(*[int(c*255) for c in colorsys.hsv_to_rgb(h, min(1, s * 1.2), v * 0.6)])
        ]
    
    return {
        "success": True,
        "base_color": base_color.upper(),
        "palette_type": palette_type,
        "colors": palette,
        "count": len(palette)
    }


def analyze_palette_harmony(colors: List[str]) -> Dict:
    """Analyze how well colors work together."""
    if len(colors) < 2:
        return {"success": False, "error": "Need at least 2 colors"}
    
    # Convert to HSV
    hsv_colors = []
    for color in colors:
        rgb = hex_to_rgb(color)
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        hsv_colors.append(hsv)
    
    # Analyze hue distribution
    hues = [hsv[0] * 360 for hsv in hsv_colors]
    hue_variance = np.var(hues)
    
    # Analyze saturation
    saturations = [hsv[1] * 100 for hsv in hsv_colors]
    sat_variance = np.var(saturations)
    
    # Analyze value/brightness
    values = [hsv[2] * 100 for hsv in hsv_colors]
    val_variance = np.var(values)
    
    # Determine harmony type
    if hue_variance < 100:
        harmony = "Monochromatic"
    elif hue_variance < 1000:
        harmony = "Analogous"
    else:
        harmony = "Diverse"
    
    # Calculate harmony score (0-100)
    harmony_score = min(100, max(0, 100 - (hue_variance / 100)))
    
    return {
        "success": True,
        "colors": colors,
        "harmony_type": harmony,
        "harmony_score": round(harmony_score, 1),
        "statistics": {
            "hue_variance": round(hue_variance, 2),
            "saturation_variance": round(sat_variance, 2),
            "value_variance": round(val_variance, 2),
            "avg_saturation": round(np.mean(saturations), 1),
            "avg_brightness": round(np.mean(values), 1)
        },
        "recommendation": "Excellent" if harmony_score > 80 else "Good" if harmony_score > 60 else "Fair"
    }

"""Color blindness simulation utilities."""
import numpy as np
from typing import Dict, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}".upper()


# Color blindness transformation matrices
# Based on Brettel, Viénot and Mollon JPEG algorithm
TRANSFORMATION_MATRICES = {
    "protanopia": np.array([
        [0.56667, 0.43333, 0.00000],
        [0.55833, 0.44167, 0.00000],
        [0.00000, 0.24167, 0.75833]
    ]),
    "protanomaly": np.array([
        [0.81667, 0.18333, 0.00000],
        [0.33333, 0.66667, 0.00000],
        [0.00000, 0.12500, 0.87500]
    ]),
    "deuteranopia": np.array([
        [0.62500, 0.37500, 0.00000],
        [0.70000, 0.30000, 0.00000],
        [0.00000, 0.30000, 0.70000]
    ]),
    "deuteranomaly": np.array([
        [0.80000, 0.20000, 0.00000],
        [0.25833, 0.74167, 0.00000],
        [0.00000, 0.14167, 0.85833]
    ]),
    "tritanopia": np.array([
        [0.95000, 0.05000, 0.00000],
        [0.00000, 0.43333, 0.56667],
        [0.00000, 0.47500, 0.52500]
    ]),
    "tritanomaly": np.array([
        [0.96667, 0.03333, 0.00000],
        [0.00000, 0.73333, 0.26667],
        [0.00000, 0.18333, 0.81667]
    ]),
    "achromatopsia": np.array([
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114]
    ]),
    "achromatomaly": np.array([
        [0.618, 0.320, 0.062],
        [0.163, 0.775, 0.062],
        [0.163, 0.320, 0.516]
    ])
}


DEFICIENCY_INFO = {
    "protanopia": {
        "name": "Protanopia",
        "type": "Red-Blind",
        "description": "Complete absence of red cone cells. Cannot perceive red wavelengths.",
        "severity": "Total",
        "affected": "~1% of males",
        "difficulty": "Reds appear dark, red/green confusion"
    },
    "protanomaly": {
        "name": "Protanomaly",
        "type": "Red-Weak",
        "description": "Reduced sensitivity to red light due to anomalous red cones.",
        "severity": "Partial",
        "affected": "~1% of males",
        "difficulty": "Difficulty distinguishing red from green"
    },
    "deuteranopia": {
        "name": "Deuteranopia",
        "type": "Green-Blind",
        "description": "Complete absence of green cone cells. Cannot perceive green wavelengths.",
        "severity": "Total",
        "affected": "~1% of males",
        "difficulty": "Green appears beige, red/green confusion"
    },
    "deuteranomaly": {
        "name": "Deuteranomaly",
        "type": "Green-Weak",
        "description": "Most common form. Reduced sensitivity to green light.",
        "severity": "Partial",
        "affected": "~5% of males",
        "difficulty": "Mild red/green confusion"
    },
    "tritanopia": {
        "name": "Tritanopia",
        "type": "Blue-Blind",
        "description": "Rare. Complete absence of blue cone cells.",
        "severity": "Total",
        "affected": "~0.001% of people",
        "difficulty": "Blue/green and yellow/red confusion"
    },
    "tritanomaly": {
        "name": "Tritanomaly",
        "type": "Blue-Weak",
        "description": "Rare. Reduced sensitivity to blue light.",
        "severity": "Partial",
        "affected": "~0.01% of people",
        "difficulty": "Difficulty with blue/yellow distinction"
    },
    "achromatopsia": {
        "name": "Achromatopsia",
        "type": "Complete Color Blindness",
        "description": "Total absence of color vision. See only in grayscale.",
        "severity": "Total",
        "affected": "~0.003% of people",
        "difficulty": "No color perception at all"
    },
    "achromatomaly": {
        "name": "Achromatomaly",
        "type": "Partial Color Blindness",
        "description": "Severe reduction in color vision.",
        "severity": "Partial",
        "affected": "Very rare",
        "difficulty": "Very limited color perception"
    }
}


def simulate_color_blindness(hex_color: str, deficiency_type: str) -> Dict:
    """
    Simulate how a color appears to someone with color blindness.
    
    Args:
        hex_color: Original color in hex format
        deficiency_type: Type of color blindness (protanopia, deuteranopia, etc.)
    
    Returns:
        Dictionary with original and simulated colors
    """
    try:
        if deficiency_type not in TRANSFORMATION_MATRICES:
            return {
                "success": False,
                "error": f"Unknown deficiency type: {deficiency_type}"
            }
        
        # Convert to RGB
        rgb = hex_to_rgb(hex_color)
        rgb_normalized = np.array(rgb) / 255.0
        
        # Apply transformation
        matrix = TRANSFORMATION_MATRICES[deficiency_type]
        simulated_rgb = np.dot(matrix, rgb_normalized)
        
        # Clamp values
        simulated_rgb = np.clip(simulated_rgb * 255, 0, 255)
        
        # Convert back to hex
        simulated_hex = rgb_to_hex(*simulated_rgb)
        
        # Get deficiency info
        info = DEFICIENCY_INFO.get(deficiency_type, {})
        
        return {
            "success": True,
            "original": {
                "hex": hex_color.upper(),
                "rgb": {"r": rgb[0], "g": rgb[1], "b": rgb[2]}
            },
            "simulated": {
                "hex": simulated_hex,
                "rgb": {
                    "r": int(simulated_rgb[0]), 
                    "g": int(simulated_rgb[1]), 
                    "b": int(simulated_rgb[2])
                }
            },
            "deficiency": deficiency_type,
            "info": info
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def simulate_all_types(hex_color: str) -> Dict:
    """Simulate color appearance for all color blindness types."""
    results = {}
    
    for deficiency_type in TRANSFORMATION_MATRICES.keys():
        result = simulate_color_blindness(hex_color, deficiency_type)
        if result.get("success"):
            results[deficiency_type] = result
    
    return {
        "success": True,
        "original_color": hex_color.upper(),
        "simulations": results
    }


def check_color_pair_accessibility(color1: str, color2: str) -> Dict:
    """
    Check if a color pair is distinguishable for people with color blindness.
    
    Args:
        color1: First color (hex)
        color2: Second color (hex)
    
    Returns:
        Accessibility analysis for all deficiency types
    """
    results = {}
    
    for deficiency_type in TRANSFORMATION_MATRICES.keys():
        sim1 = simulate_color_blindness(color1, deficiency_type)
        sim2 = simulate_color_blindness(color2, deficiency_type)
        
        if sim1.get("success") and sim2.get("success"):
            # Calculate color difference
            rgb1 = np.array([
                sim1["simulated"]["rgb"]["r"],
                sim1["simulated"]["rgb"]["g"],
                sim1["simulated"]["rgb"]["b"]
            ])
            rgb2 = np.array([
                sim2["simulated"]["rgb"]["r"],
                sim2["simulated"]["rgb"]["g"],
                sim2["simulated"]["rgb"]["b"]
            ])
            
            # Euclidean distance
            difference = np.linalg.norm(rgb1 - rgb2)
            
            # Threshold for distinguishability (arbitrary, but reasonable)
            distinguishable = bool(difference > 50)
            
            results[deficiency_type] = {
                "distinguishable": distinguishable,
                "difference": round(float(difference), 2),
                "color1_simulated": sim1["simulated"]["hex"],
                "color2_simulated": sim2["simulated"]["hex"],
                "recommendation": "Good" if distinguishable else "Poor",
                "info": DEFICIENCY_INFO.get(deficiency_type, {})
            }
    
    # Calculate overall accessibility score
    total = len(results)
    passed = sum(1 for r in results.values() if r["distinguishable"])
    accessibility_score = (passed / total) * 100 if total > 0 else 0
    
    return {
        "success": True,
        "color1": color1.upper(),
        "color2": color2.upper(),
        "results": results,
        "accessibility_score": round(accessibility_score, 1),
        "passed": passed,
        "total": total
    }


def get_safe_color_alternatives(hex_color: str) -> Dict:
    """Suggest color alternatives that are more accessible."""
    # This is a simplified version - could be enhanced with ML
    rgb = hex_to_rgb(hex_color)
    
    alternatives = []
    
    # Suggest higher contrast versions
    # Lighter version
    lighter_rgb = tuple(min(255, int(c * 1.3)) for c in rgb)
    alternatives.append({
        "hex": rgb_to_hex(*lighter_rgb),
        "description": "Lighter version (30% brighter)",
        "type": "brightness"
    })
    
    # Darker version
    darker_rgb = tuple(max(0, int(c * 0.7)) for c in rgb)
    alternatives.append({
        "hex": rgb_to_hex(*darker_rgb),
        "description": "Darker version (30% darker)",
        "type": "brightness"
    })
    
    # More saturated
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    sat_rgb = colorsys.hsv_to_rgb(h, min(1, s * 1.3), v)
    sat_rgb = tuple(int(c * 255) for c in sat_rgb)
    alternatives.append({
        "hex": rgb_to_hex(*sat_rgb),
        "description": "More saturated",
        "type": "saturation"
    })
    
    return {
        "success": True,
        "original": hex_color.upper(),
        "alternatives": alternatives
    }


def get_all_deficiency_info() -> Dict:
    """Get information about all color blindness types."""
    return {
        "success": True,
        "deficiencies": DEFICIENCY_INFO
    }

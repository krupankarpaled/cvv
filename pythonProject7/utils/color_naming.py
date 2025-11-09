"""Color naming and search utilities."""
import webcolors
import numpy as np
from typing import Dict, List, Tuple, Optional


# Comprehensive color database (CSS3 + X11 + Extended)
COLOR_DATABASE = {
    # Basic colors
    "white": "#FFFFFF", "black": "#000000", "red": "#FF0000", "green": "#00FF00",
    "blue": "#0000FF", "yellow": "#FFFF00", "cyan": "#00FFFF", "magenta": "#FF00FF",
    
    # CSS3 Named Colors
    "aliceblue": "#F0F8FF", "antiquewhite": "#FAEBD7", "aqua": "#00FFFF",
    "aquamarine": "#7FFFD4", "azure": "#F0FFFF", "beige": "#F5F5DC",
    "bisque": "#FFE4C4", "blanchedalmond": "#FFEBCD", "blueviolet": "#8A2BE2",
    "brown": "#A52A2A", "burlywood": "#DEB887", "cadetblue": "#5F9EA0",
    "chartreuse": "#7FFF00", "chocolate": "#D2691E", "coral": "#FF7F50",
    "cornflowerblue": "#6495ED", "cornsilk": "#FFF8DC", "crimson": "#DC143C",
    "darkblue": "#00008B", "darkcyan": "#008B8B", "darkgoldenrod": "#B8860B",
    "darkgray": "#A9A9A9", "darkgreen": "#006400", "darkkhaki": "#BDB76B",
    "darkmagenta": "#8B008B", "darkolivegreen": "#556B2F", "darkorange": "#FF8C00",
    "darkorchid": "#9932CC", "darkred": "#8B0000", "darksalmon": "#E9967A",
    "darkseagreen": "#8FBC8F", "darkslateblue": "#483D8B", "darkslategray": "#2F4F4F",
    "darkturquoise": "#00CED1", "darkviolet": "#9400D3", "deeppink": "#FF1493",
    "deepskyblue": "#00BFFF", "dimgray": "#696969", "dodgerblue": "#1E90FF",
    "firebrick": "#B22222", "floralwhite": "#FFFAF0", "forestgreen": "#228B22",
    "fuchsia": "#FF00FF", "gainsboro": "#DCDCDC", "ghostwhite": "#F8F8FF",
    "gold": "#FFD700", "goldenrod": "#DAA520", "gray": "#808080",
    "greenyellow": "#ADFF2F", "honeydew": "#F0FFF0", "hotpink": "#FF69B4",
    "indianred": "#CD5C5C", "indigo": "#4B0082", "ivory": "#FFFFF0",
    "khaki": "#F0E68C", "lavender": "#E6E6FA", "lavenderblush": "#FFF0F5",
    "lawngreen": "#7CFC00", "lemonchiffon": "#FFFACD", "lightblue": "#ADD8E6",
    "lightcoral": "#F08080", "lightcyan": "#E0FFFF", "lightgoldenrodyellow": "#FAFAD2",
    "lightgray": "#D3D3D3", "lightgreen": "#90EE90", "lightpink": "#FFB6C1",
    "lightsalmon": "#FFA07A", "lightseagreen": "#20B2AA", "lightskyblue": "#87CEFA",
    "lightslategray": "#778899", "lightsteelblue": "#B0C4DE", "lightyellow": "#FFFFE0",
    "lime": "#00FF00", "limegreen": "#32CD32", "linen": "#FAF0E6",
    "maroon": "#800000", "mediumaquamarine": "#66CDAA", "mediumblue": "#0000CD",
    "mediumorchid": "#BA55D3", "mediumpurple": "#9370DB", "mediumseagreen": "#3CB371",
    "mediumslateblue": "#7B68EE", "mediumspringgreen": "#00FA9A", "mediumturquoise": "#48D1CC",
    "mediumvioletred": "#C71585", "midnightblue": "#191970", "mintcream": "#F5FFFA",
    "mistyrose": "#FFE4E1", "moccasin": "#FFE4B5", "navajowhite": "#FFDEAD",
    "navy": "#000080", "oldlace": "#FDF5E6", "olive": "#808000",
    "olivedrab": "#6B8E23", "orange": "#FFA500", "orangered": "#FF4500",
    "orchid": "#DA70D6", "palegoldenrod": "#EEE8AA", "palegreen": "#98FB98",
    "paleturquoise": "#AFEEEE", "palevioletred": "#DB7093", "papayawhip": "#FFEFD5",
    "peachpuff": "#FFDAB9", "peru": "#CD853F", "pink": "#FFC0CB",
    "plum": "#DDA0DD", "powderblue": "#B0E0E6", "purple": "#800080",
    "rebeccapurple": "#663399", "rosybrown": "#BC8F8F", "royalblue": "#4169E1",
    "saddlebrown": "#8B4513", "salmon": "#FA8072", "sandybrown": "#F4A460",
    "seagreen": "#2E8B57", "seashell": "#FFF5EE", "sienna": "#A0522D",
    "silver": "#C0C0C0", "skyblue": "#87CEEB", "slateblue": "#6A5ACD",
    "slategray": "#708090", "snow": "#FFFAFA", "springgreen": "#00FF7F",
    "steelblue": "#4682B4", "tan": "#D2B48C", "teal": "#008080",
    "thistle": "#D8BFD8", "tomato": "#FF6347", "turquoise": "#40E0D0",
    "violet": "#EE82EE", "wheat": "#F5DEB3", "whitesmoke": "#F5F5F5",
    "yellowgreen": "#9ACD32",
}


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return f"#{r:02x}{g:02x}{b:02x}".upper()


def color_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two RGB colors."""
    return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


def find_closest_color_name(hex_color: str) -> Dict:
    """Find the closest named color to the given hex color."""
    try:
        # Try exact match first
        try:
            name = webcolors.hex_to_name(hex_color)
            return {
                "name": name.title(),
                "hex": hex_color.upper(),
                "distance": 0,
                "exact_match": True
            }
        except ValueError:
            pass
        
        # Find closest color
        rgb = hex_to_rgb(hex_color)
        min_distance = float('inf')
        closest_name = None
        closest_hex = None
        
        for name, named_hex in COLOR_DATABASE.items():
            named_rgb = hex_to_rgb(named_hex)
            distance = color_distance(rgb, named_rgb)
            
            if distance < min_distance:
                min_distance = distance
                closest_name = name
                closest_hex = named_hex
        
        return {
            "name": closest_name.title() if closest_name else "Unknown",
            "hex": closest_hex.upper() if closest_hex else hex_color.upper(),
            "distance": round(min_distance, 2),
            "exact_match": False,
            "similarity": round(max(0, 100 - (min_distance / 4.41)), 2)  # Normalize to 0-100
        }
    except Exception as e:
        return {
            "name": "Unknown",
            "hex": hex_color.upper(),
            "distance": None,
            "exact_match": False,
            "error": str(e)
        }


def search_colors_by_name(query: str, limit: int = 10) -> List[Dict]:
    """Search colors by name (fuzzy search)."""
    query = query.lower().strip()
    results = []
    
    # Exact match first
    if query in COLOR_DATABASE:
        results.append({
            "name": query.title(),
            "hex": COLOR_DATABASE[query].upper(),
            "rgb": hex_to_rgb(COLOR_DATABASE[query]),
            "match_type": "exact"
        })
    
    # Partial matches
    for name, hex_color in COLOR_DATABASE.items():
        if query in name and name != query:
            results.append({
                "name": name.title(),
                "hex": hex_color.upper(),
                "rgb": hex_to_rgb(hex_color),
                "match_type": "partial"
            })
    
    return results[:limit]


def get_color_by_name(name: str) -> Optional[Dict]:
    """Get color information by exact name."""
    name = name.lower().strip()
    
    if name in COLOR_DATABASE:
        hex_color = COLOR_DATABASE[name]
        rgb = hex_to_rgb(hex_color)
        
        return {
            "name": name.title(),
            "hex": hex_color.upper(),
            "rgb": {"r": rgb[0], "g": rgb[1], "b": rgb[2]},
            "found": True
        }
    
    return None


def get_all_color_names() -> List[Dict]:
    """Get all available color names."""
    return [
        {
            "name": name.title(),
            "hex": hex_color.upper(),
            "rgb": hex_to_rgb(hex_color)
        }
        for name, hex_color in sorted(COLOR_DATABASE.items())
    ]


def get_colors_by_hue_range(min_hue: int, max_hue: int) -> List[Dict]:
    """Get colors within a specific hue range."""
    import colorsys
    results = []
    
    for name, hex_color in COLOR_DATABASE.items():
        rgb = hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        hue = int(h * 360)
        
        if min_hue <= hue <= max_hue:
            results.append({
                "name": name.title(),
                "hex": hex_color.upper(),
                "hue": hue,
                "saturation": round(s * 100, 1),
                "value": round(v * 100, 1)
            })
    
    return sorted(results, key=lambda x: x["hue"])

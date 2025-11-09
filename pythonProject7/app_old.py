from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
import colorsys
import os

app = Flask(__name__)

# ----------------------------------------------------------
# EXTENDED COLOR DATABASE (HTML + Fashion + Common Colors)
# ----------------------------------------------------------
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

# ----------------------------------------------------------
# Helper functions
# ----------------------------------------------------------
def bgr_to_hex(bgr):
    b, g, r = map(int, bgr)
    return '#%02x%02x%02x' % (r, g, b)

def hex_to_rgb_tuple(hex_code):
    h = hex_code.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def nearest_color_name(rgb_tuple):
    """Find nearest color from COLOR_DB by Euclidean distance."""
    r0, g0, b0 = rgb_tuple
    best = (None, None, 1e9)
    for name, hexc in COLOR_DB.items():
        r1, g1, b1 = hex_to_rgb_tuple(hexc)
        d = (r0 - r1)**2 + (g0 - g1)**2 + (b0 - b1)**2
        if d < best[2]:
            best = (name, hexc, d)
    return best[0], best[1]

def hls_to_bgr(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h % 1.0, l, s)
    return (int(b * 255), int(g * 255), int(r * 255))

def make_matching_palette(center_bgr):
    """Generate a monochromatic palette: tints, shades, and neutrals for clothing matching."""
    b, g, r = center_bgr
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(rn, gn, bn)

    # Generate tints (lighter) and shades (darker) by varying lightness
    palette = []
    lightness_steps = [0.9, 0.7, 0.5, 0.3, 0.1]  # From very light to very dark
    for new_l in lightness_steps:
        new_l = min(1.0, max(0.0, new_l))  # Clamp to valid range
        palette.append(hls_to_bgr(h, new_l, s))

    # Add neutrals: black, white, gray if not too similar to existing
    neutrals = [(0, 0, 0), (255, 255, 255), (128, 128, 128)]
    for neutral in neutrals:
        if neutral not in palette:
            palette.append(neutral)

    # Deduplicate by hex and limit to 6
    seen, final = set(), []
    for col in palette:
        hx = bgr_to_hex(col)
        if hx not in seen:
            seen.add(hx)
            final.append(col)
        if len(final) >= 6:
            break
    return final

# ----------------------------------------------------------
# Flask routes
# ----------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    data = request.json
    img_data = base64.b64decode(data['image'].split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    h, w = frame.shape[:2]
    cx, cy, s = w // 2, h // 2, 60
    roi = frame[cy - s:cy + s, cx - s:cx + s]
    avg = roi.mean(axis=(0, 1))
    avg_bgr = tuple(map(int, avg))
    avg_rgb = (avg_bgr[2], avg_bgr[1], avg_bgr[0])

    name, name_hex = nearest_color_name(avg_rgb)
    palette_bgr = make_matching_palette(avg_bgr)
    palette = [{'hex': bgr_to_hex(p), 'name': nearest_color_name((p[2], p[1], p[0]))[0]} for p in palette_bgr]

    return jsonify({
        'color': bgr_to_hex(avg_bgr),
        'name': name,
        'palette': palette
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

"""API Routes for Color Detector Application."""
import logging
import colorsys
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.exceptions import BadRequest

from models import (
    db, ColorHistory, ColorPalette, BrandCollection, FavoriteColor,
    ColorAnalytics, SharedPalette, PaletteComment, Gradient
)
from utils.color_utils import (
    hex_to_rgb, rgb_to_hex, nearest_color_name,
    format_color_info, get_complementary_color, get_analogous_colors,
    get_triadic_colors, get_tetradic_colors, get_monochromatic_palette,
    get_shades_and_tints, get_split_complementary
)
from utils.image_processing import validate_image_data, decode_image, extract_color_from_image
from utils.color_naming import (
    search_colors_by_name, find_closest_color_name, get_color_by_name,
    get_all_color_names, get_colors_by_hue_range
)
from utils.palette_extraction import (
    extract_palette_from_image, analyze_color_distribution
)
from utils.gradient_generator import (
    generate_gradient, generate_gradient_css, generate_preset_gradients,
    generate_custom_gradient
)
from utils.color_blindness import (
    simulate_color_blindness, simulate_all_types, check_color_pair_accessibility,
    get_safe_color_alternatives, get_all_deficiency_info
)
from utils.color_mixer import (
    mix_colors_rgb, mix_colors_cmyk, mix_colors_hsl, mix_colors_subtractive,
    mix_two_colors_interactive, create_color_palette_mix
)
from utils.ai_suggestions import (
    suggest_complementary_colors, suggest_palette_by_mood, suggest_palette_by_industry,
    get_all_moods, get_all_industries, suggest_text_color, generate_smart_palette,
    analyze_palette_harmony
)

logger = logging.getLogger(__name__)

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


def error_response(message: str, status_code: int = 400):
    """Create standardized error response."""
    return jsonify({
        'success': False,
        'error': message,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code


def save_to_history(rgb: tuple, hex_code: str, name: str, session_id: str):
    """Save color detection to history."""
    try:
        history = ColorHistory(
            hex_code=hex_code,
            color_name=name,
            rgb_r=rgb[0],
            rgb_g=rgb[1],
            rgb_b=rgb[2],
            session_id=session_id
        )
        db.session.add(history)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error saving to history: {str(e)}")
        db.session.rollback()


def track_analytics(hex_code: str, action_type: str, metadata: dict = None):
    """Track color usage analytics."""
    try:
        if 'session_id' in session:
            analytics = ColorAnalytics(
                hex_code=hex_code,
                action_type=action_type,
                session_id=session['session_id'],
                analytics_data=metadata
            )
            db.session.add(analytics)
            db.session.commit()
    except Exception as e:
        logger.error(f"Error tracking analytics: {str(e)}")
        db.session.rollback()


@api.route('/detect', methods=['POST'])
def detect_color():
    """Detect color from webcam image."""
    try:
        data = request.get_json()
        
        if not validate_image_data(data):
            return error_response("Invalid image data", 400)
        
        frame = decode_image(data['image'])
        x = data.get('x')
        y = data.get('y')
        rgb = extract_color_from_image(frame, x, y)
        
        hex_code = rgb_to_hex(rgb)
        name, _ = nearest_color_name(rgb)
        
        # Save to history if session exists
        if 'session_id' in session:
            save_to_history(rgb, hex_code, name, session['session_id'])
        
        # Get color schemes
        schemes = {
            'monochromatic': [
                {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
                for c in get_monochromatic_palette(rgb)
            ],
            'complementary': [
                {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
                for c in [get_complementary_color(rgb)]
            ],
            'analogous': [
                {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
                for c in get_analogous_colors(rgb, 2)[:4]
            ],
            'triadic': [
                {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
                for c in get_triadic_colors(rgb)
            ],
            'tetradic': [
                {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
                for c in get_tetradic_colors(rgb)
            ],
            'split_complementary': [
                {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
                for c in get_split_complementary(rgb)
            ]
        }
        
        shades_tints = get_shades_and_tints(rgb)
        schemes['shades'] = [
            {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
            for c in shades_tints['shades']
        ]
        schemes['tints'] = [
            {'hex': rgb_to_hex(c), 'name': nearest_color_name(c)[0]}
            for c in shades_tints['tints']
        ]
        
        color_info = format_color_info(rgb, hex_code, name)
        
        return jsonify({
            'success': True,
            'color': color_info,
            'schemes': schemes,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error in detect_color: {str(e)}", exc_info=True)
        return error_response("Internal server error", 500)


@api.route('/history', methods=['GET'])
def get_history():
    """Get color detection history."""
    try:
        if 'session_id' not in session:
            return jsonify({'success': True, 'history': [], 'count': 0})
        
        limit = min(request.args.get('limit', 20, type=int), 100)
        
        history = ColorHistory.query.filter_by(
            session_id=session['session_id']
        ).order_by(ColorHistory.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'history': [h.to_dict() for h in history],
            'count': len(history)
        })
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return error_response("Failed to fetch history", 500)


@api.route('/history/<int:history_id>', methods=['DELETE'])
def delete_history_item(history_id):
    """Delete a history item."""
    try:
        if 'session_id' not in session:
            return error_response("No session found", 404)
        
        item = ColorHistory.query.filter_by(
            id=history_id,
            session_id=session['session_id']
        ).first()
        
        if not item:
            return error_response("History item not found", 404)
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'History item deleted'})
    except Exception as e:
        logger.error(f"Error deleting history: {str(e)}")
        db.session.rollback()
        return error_response("Failed to delete history item", 500)


@api.route('/history/clear', methods=['DELETE'])
def clear_history():
    """Clear all history."""
    try:
        if 'session_id' not in session:
            return jsonify({'success': True, 'message': 'No history to clear'})
        
        ColorHistory.query.filter_by(session_id=session['session_id']).delete()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'History cleared'})
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        db.session.rollback()
        return error_response("Failed to clear history", 500)


@api.route('/analyze', methods=['POST'])
def analyze_color():
    """Analyze a color by hex code."""
    try:
        data = request.get_json()
        
        if not data or 'hex' not in data:
            return error_response("Missing hex code", 400)
        
        hex_code = data['hex']
        if not hex_code.startswith('#'):
            hex_code = '#' + hex_code
        
        rgb = hex_to_rgb(hex_code)
        name, _ = nearest_color_name(rgb)
        color_info = format_color_info(rgb, hex_code, name)
        
        return jsonify({'success': True, 'color': color_info})
    except Exception as e:
        logger.error(f"Error analyzing color: {str(e)}")
        return error_response("Failed to analyze color", 500)


@api.route('/palettes', methods=['GET', 'POST'])
def manage_palettes():
    """Get all palettes or create new one."""
    if request.method == 'POST':
        try:
            if 'session_id' not in session:
                return error_response("No session found", 400)
            
            data = request.get_json()
            
            if not data or 'name' not in data or 'colors' not in data:
                return error_response("Missing required fields", 400)
            
            palette = ColorPalette(
                name=data['name'],
                description=data.get('description', ''),
                colors=data['colors'],
                session_id=session['session_id'],
                is_favorite=data.get('is_favorite', False)
            )
            db.session.add(palette)
            db.session.commit()
            
            return jsonify({'success': True, 'palette': palette.to_dict()}), 201
        except Exception as e:
            logger.error(f"Error creating palette: {str(e)}")
            db.session.rollback()
            return error_response("Failed to create palette", 500)
    else:
        try:
            if 'session_id' not in session:
                return jsonify({'success': True, 'palettes': [], 'count': 0})
            
            palettes = ColorPalette.query.filter_by(
                session_id=session['session_id']
            ).order_by(
                ColorPalette.is_favorite.desc(),
                ColorPalette.created_at.desc()
            ).all()
            
            return jsonify({
                'success': True,
                'palettes': [p.to_dict() for p in palettes],
                'count': len(palettes)
            })
        except Exception as e:
            logger.error(f"Error fetching palettes: {str(e)}")
            return error_response("Failed to fetch palettes", 500)


@api.route('/palettes/<int:palette_id>', methods=['PUT', 'DELETE'])
def manage_palette(palette_id):
    """Update or delete a palette."""
    try:
        if 'session_id' not in session:
            return error_response("No session found", 404)
        
        palette = ColorPalette.query.filter_by(
            id=palette_id,
            session_id=session['session_id']
        ).first()
        
        if not palette:
            return error_response("Palette not found", 404)
        
        if request.method == 'DELETE':
            db.session.delete(palette)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Palette deleted'})
        else:
            data = request.get_json()
            if 'name' in data:
                palette.name = data['name']
            if 'description' in data:
                palette.description = data['description']
            if 'colors' in data:
                palette.colors = data['colors']
            if 'is_favorite' in data:
                palette.is_favorite = data['is_favorite']
            
            db.session.commit()
            return jsonify({'success': True, 'palette': palette.to_dict()})
    except Exception as e:
        logger.error(f"Error managing palette: {str(e)}")
        db.session.rollback()
        return error_response("Operation failed", 500)


# ============================================================================
# COLOR NAMING & SEARCH
# ============================================================================

@api.route('/colors/search', methods=['GET'])
def search_colors():
    """Search colors by name."""
    try:
        query = request.args.get('q', '').strip()
        limit = min(request.args.get('limit', 10, type=int), 50)
        
        if not query:
            return error_response("Query parameter required", 400)
        
        results = search_colors_by_name(query, limit)
        return jsonify({'success': True, 'results': results, 'count': len(results)})
    except Exception as e:
        logger.error(f"Error searching colors: {str(e)}")
        return error_response("Search failed", 500)


@api.route('/colors/name/<hex_color>', methods=['GET'])
def get_color_name(hex_color):
    """Get closest color name for a hex color."""
    try:
        if not hex_color.startswith('#'):
            hex_color = '#' + hex_color
        
        result = find_closest_color_name(hex_color)
        track_analytics(hex_color, 'color_name_lookup')
        
        return jsonify({'success': True, **result})
    except Exception as e:
        logger.error(f"Error getting color name: {str(e)}")
        return error_response("Failed to get color name", 500)


@api.route('/colors/all', methods=['GET'])
def get_all_colors():
    """Get all named colors."""
    try:
        colors = get_all_color_names()
        return jsonify({'success': True, 'colors': colors, 'count': len(colors)})
    except Exception as e:
        logger.error(f"Error getting all colors: {str(e)}")
        return error_response("Failed to get colors", 500)


# ============================================================================
# IMAGE PALETTE EXTRACTION
# ============================================================================

@api.route('/palette/extract', methods=['POST'])
def extract_palette():
    """Extract color palette from image."""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return error_response("Image data required", 400)
        
        n_colors = data.get('n_colors', 5)
        method = data.get('method', 'kmeans')
        
        result = extract_palette_from_image(data['image'], n_colors, method)
        
        if result.get('success'):
            track_analytics('palette_extraction', 'extract_palette', 
                          {'n_colors': n_colors, 'method': method})
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error extracting palette: {str(e)}")
        return error_response("Palette extraction failed", 500)


# ============================================================================
# GRADIENT GENERATOR
# ============================================================================

@api.route('/gradient/generate', methods=['POST'])
def generate_gradient_route():
    """Generate gradient from colors."""
    try:
        data = request.get_json()
        
        if not data or 'colors' not in data:
            return error_response("Colors array required", 400)
        
        colors = data['colors']
        steps = data.get('steps', 10)
        method = data.get('method', 'rgb')
        
        result = generate_gradient(colors, steps, method)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error generating gradient: {str(e)}")
        return error_response("Gradient generation failed", 500)


@api.route('/gradient/presets', methods=['GET'])
def get_gradient_presets():
    """Get preset gradients."""
    try:
        presets = generate_preset_gradients()
        return jsonify({'success': True, 'presets': presets, 'count': len(presets)})
    except Exception as e:
        logger.error(f"Error getting presets: {str(e)}")
        return error_response("Failed to get presets", 500)


@api.route('/gradient/custom', methods=['POST'])
def create_custom_gradient():
    """Create custom gradient."""
    try:
        data = request.get_json()
        
        if not data or 'start' not in data or 'end' not in data:
            return error_response("Start and end colors required", 400)
        
        result = generate_custom_gradient(
            data['start'], data['end'], 
            data.get('steps', 10),
            data.get('gradient_type', 'linear'),
            data.get('angle', 90)
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error creating custom gradient: {str(e)}")
        return error_response("Failed to create gradient", 500)


# ============================================================================
# COLOR BLINDNESS SIMULATOR
# ============================================================================

@api.route('/colorblindness/simulate', methods=['POST'])
def simulate_color_blindness_route():
    """Simulate color blindness for a color."""
    try:
        data = request.get_json()
        
        if not data or 'color' not in data:
            return error_response("Color required", 400)
        
        deficiency_type = data.get('type', 'protanopia')
        result = simulate_color_blindness(data['color'], deficiency_type)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error simulating color blindness: {str(e)}")
        return error_response("Simulation failed", 500)


@api.route('/colorblindness/all-types', methods=['POST'])
def simulate_all_types_route():
    """Simulate all color blindness types."""
    try:
        data = request.get_json()
        
        if not data or 'color' not in data:
            return error_response("Color required", 400)
        
        result = simulate_all_types(data['color'])
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error simulating all types: {str(e)}")
        return error_response("Simulation failed", 500)


@api.route('/colorblindness/check-pair', methods=['POST'])
def check_color_pair():
    """Check if color pair is distinguishable."""
    try:
        data = request.get_json()
        
        if not data or 'color1' not in data or 'color2' not in data:
            return error_response("Two colors required", 400)
        
        result = check_color_pair_accessibility(data['color1'], data['color2'])
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error checking color pair: {str(e)}")
        return error_response("Check failed", 500)


@api.route('/colorblindness/info', methods=['GET'])
def get_colorblindness_info():
    """Get information about all color blindness types."""
    try:
        result = get_all_deficiency_info()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting info: {str(e)}")
        return error_response("Failed to get info", 500)


# ============================================================================
# COLOR MIXER
# ============================================================================

@api.route('/mixer/mix', methods=['POST'])
def mix_colors():
    """Mix colors using different methods."""
    try:
        data = request.get_json()
        
        if not data or 'colors' not in data:
            return error_response("Colors array required", 400)
        
        colors = data['colors']
        method = data.get('method', 'cmyk')
        ratios = data.get('ratios')
        
        if method == 'rgb':
            result = mix_colors_rgb(colors, ratios)
        elif method == 'cmyk':
            result = mix_colors_cmyk(colors, ratios)
        elif method == 'hsl':
            result = mix_colors_hsl(colors, ratios)
        elif method == 'subtractive':
            result = mix_colors_subtractive(colors, ratios)
        else:
            result = mix_colors_cmyk(colors, ratios)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error mixing colors: {str(e)}")
        return error_response("Mixing failed", 500)


@api.route('/mixer/two-colors', methods=['POST'])
def mix_two_colors():
    """Mix two colors with variable ratio."""
    try:
        data = request.get_json()
        
        if not data or 'color1' not in data or 'color2' not in data:
            return error_response("Two colors required", 400)
        
        ratio = data.get('ratio', 0.5)
        result = mix_two_colors_interactive(data['color1'], data['color2'], ratio)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error mixing two colors: {str(e)}")
        return error_response("Mixing failed", 500)


# ============================================================================
# AI SUGGESTIONS
# ============================================================================

@api.route('/ai/suggest-complementary', methods=['POST'])
def suggest_complementary():
    """Suggest complementary colors."""
    try:
        data = request.get_json()
        
        if not data or 'color' not in data:
            return error_response("Color required", 400)
        
        count = data.get('count', 5)
        result = suggest_complementary_colors(data['color'], count)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error suggesting complementary colors: {str(e)}")
        return error_response("Suggestion failed", 500)


@api.route('/ai/palette-by-mood', methods=['GET'])
def get_mood_palette():
    """Get palette by mood."""
    try:
        mood = request.args.get('mood', '').strip()
        
        if not mood:
            return error_response("Mood parameter required", 400)
        
        result = suggest_palette_by_mood(mood)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting mood palette: {str(e)}")
        return error_response("Failed to get palette", 500)


@api.route('/ai/palette-by-industry', methods=['GET'])
def get_industry_palette():
    """Get palette by industry."""
    try:
        industry = request.args.get('industry', '').strip()
        
        if not industry:
            return error_response("Industry parameter required", 400)
        
        result = suggest_palette_by_industry(industry)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting industry palette: {str(e)}")
        return error_response("Failed to get palette", 500)


@api.route('/ai/moods', methods=['GET'])
def get_all_moods_route():
    """Get all available moods."""
    try:
        result = get_all_moods()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting moods: {str(e)}")
        return error_response("Failed to get moods", 500)


@api.route('/ai/industries', methods=['GET'])
def get_all_industries_route():
    """Get all available industries."""
    try:
        result = get_all_industries()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting industries: {str(e)}")
        return error_response("Failed to get industries", 500)


@api.route('/ai/smart-palette', methods=['POST'])
def generate_smart_palette_route():
    """Generate smart palette."""
    try:
        data = request.get_json()
        
        if not data or 'color' not in data:
            return error_response("Base color required", 400)
        
        palette_type = data.get('type', 'balanced')
        result = generate_smart_palette(data['color'], palette_type)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error generating smart palette: {str(e)}")
        return error_response("Generation failed", 500)


@api.route('/ai/analyze-harmony', methods=['POST'])
def analyze_harmony():
    """Analyze palette harmony."""
    try:
        data = request.get_json()
        
        if not data or 'colors' not in data:
            return error_response("Colors array required", 400)
        
        result = analyze_palette_harmony(data['colors'])
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error analyzing harmony: {str(e)}")
        return error_response("Analysis failed", 500)


# ============================================================================
# BRAND COLLECTIONS
# ============================================================================

@api.route('/brands', methods=['GET', 'POST'])
def manage_brands():
    """Get or create brand collections."""
    if request.method == 'POST':
        try:
            if 'session_id' not in session:
                return error_response("No session found", 400)
            
            data = request.get_json()
            
            if not data or 'name' not in data or 'primary_colors' not in data:
                return error_response("Missing required fields", 400)
            
            brand = BrandCollection(
                name=data['name'],
                description=data.get('description', ''),
                logo_url=data.get('logo_url'),
                primary_colors=data['primary_colors'],
                secondary_colors=data.get('secondary_colors', []),
                project_type=data.get('project_type', 'personal'),
                client_name=data.get('client_name'),
                session_id=session['session_id']
            )
            db.session.add(brand)
            db.session.commit()
            
            return jsonify({'success': True, 'brand': brand.to_dict()}), 201
        except Exception as e:
            logger.error(f"Error creating brand: {str(e)}")
            db.session.rollback()
            return error_response("Failed to create brand", 500)
    else:
        try:
            if 'session_id' not in session:
                return jsonify({'success': True, 'brands': [], 'count': 0})
            
            brands = BrandCollection.query.filter_by(
                session_id=session['session_id'],
                is_archived=False
            ).order_by(BrandCollection.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'brands': [b.to_dict() for b in brands],
                'count': len(brands)
            })
        except Exception as e:
            logger.error(f"Error fetching brands: {str(e)}")
            return error_response("Failed to fetch brands", 500)


@api.route('/brands/<int:brand_id>', methods=['PUT', 'DELETE'])
def manage_brand(brand_id):
    """Update or delete brand collection."""
    try:
        if 'session_id' not in session:
            return error_response("No session found", 404)
        
        brand = BrandCollection.query.filter_by(
            id=brand_id,
            session_id=session['session_id']
        ).first()
        
        if not brand:
            return error_response("Brand not found", 404)
        
        if request.method == 'DELETE':
            brand.is_archived = True
            db.session.commit()
            return jsonify({'success': True, 'message': 'Brand archived'})
        else:
            data = request.get_json()
            if 'name' in data:
                brand.name = data['name']
            if 'description' in data:
                brand.description = data['description']
            if 'primary_colors' in data:
                brand.primary_colors = data['primary_colors']
            if 'secondary_colors' in data:
                brand.secondary_colors = data['secondary_colors']
            
            db.session.commit()
            return jsonify({'success': True, 'brand': brand.to_dict()})
    except Exception as e:
        logger.error(f"Error managing brand: {str(e)}")
        db.session.rollback()
        return error_response("Operation failed", 500)


# ============================================================================
# FAVORITE COLORS
# ============================================================================

@api.route('/favorites', methods=['GET', 'POST'])
def manage_favorites():
    """Get or create favorite colors."""
    if request.method == 'POST':
        try:
            if 'session_id' not in session:
                return error_response("No session found", 400)
            
            data = request.get_json()
            
            if not data or 'hex_code' not in data:
                return error_response("Hex code required", 400)
            
            # Check if already exists
            existing = FavoriteColor.query.filter_by(
                hex_code=data['hex_code'].upper(),
                session_id=session['session_id']
            ).first()
            
            if existing:
                return error_response("Color already in favorites", 409)
            
            favorite = FavoriteColor(
                hex_code=data['hex_code'].upper(),
                color_name=data.get('color_name'),
                notes=data.get('notes'),
                tags=data.get('tags', []),
                session_id=session['session_id']
            )
            db.session.add(favorite)
            db.session.commit()
            
            return jsonify({'success': True, 'favorite': favorite.to_dict()}), 201
        except Exception as e:
            logger.error(f"Error adding favorite: {str(e)}")
            db.session.rollback()
            return error_response("Failed to add favorite", 500)
    else:
        try:
            if 'session_id' not in session:
                return jsonify({'success': True, 'favorites': [], 'count': 0})
            
            favorites = FavoriteColor.query.filter_by(
                session_id=session['session_id']
            ).order_by(FavoriteColor.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'favorites': [f.to_dict() for f in favorites],
                'count': len(favorites)
            })
        except Exception as e:
            logger.error(f"Error fetching favorites: {str(e)}")
            return error_response("Failed to fetch favorites", 500)


@api.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    """Delete a favorite color."""
    try:
        if 'session_id' not in session:
            return error_response("No session found", 404)
        
        favorite = FavoriteColor.query.filter_by(
            id=favorite_id,
            session_id=session['session_id']
        ).first()
        
        if not favorite:
            return error_response("Favorite not found", 404)
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Favorite deleted'})
    except Exception as e:
        logger.error(f"Error deleting favorite: {str(e)}")
        db.session.rollback()
        return error_response("Failed to delete favorite", 500)


# ============================================================================
# ANALYTICS
# ============================================================================

@api.route('/analytics/usage', methods=['GET'])
def get_usage_analytics():
    """Get color usage analytics."""
    try:
        if 'session_id' not in session:
            return jsonify({'success': True, 'analytics': {}})
        
        # Get most used colors
        most_used = db.session.query(
            ColorAnalytics.hex_code,
            db.func.count(ColorAnalytics.id).label('count')
        ).filter_by(session_id=session['session_id']).group_by(
            ColorAnalytics.hex_code
        ).order_by(db.desc('count')).limit(10).all()
        
        # Get action types
        actions = db.session.query(
            ColorAnalytics.action_type,
            db.func.count(ColorAnalytics.id).label('count')
        ).filter_by(session_id=session['session_id']).group_by(
            ColorAnalytics.action_type
        ).all()
        
        return jsonify({
            'success': True,
            'most_used_colors': [{'hex': hex_code, 'count': count} for hex_code, count in most_used],
            'action_types': [{'action': action_type, 'count': count} for action_type, count in actions]
        })
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return error_response("Failed to get analytics", 500)


# ============================================================================
# QUICK WIN FEATURES
# ============================================================================

@api.route('/tools/compare', methods=['POST'])
def compare_colors():
    """Compare two colors side by side."""
    try:
        data = request.get_json()
        
        if not data or 'color1' not in data or 'color2' not in data:
            return error_response("Two colors required", 400)
        
        # Get color info for both
        rgb1 = hex_to_rgb(data['color1'])
        rgb2 = hex_to_rgb(data['color2'])
        
        # Calculate difference
        diff = sum(abs(c1 - c2) for c1, c2 in zip(rgb1, rgb2))
        
        return jsonify({
            'success': True,
            'color1': {'hex': data['color1'], 'rgb': {'r': rgb1[0], 'g': rgb1[1], 'b': rgb1[2]}},
            'color2': {'hex': data['color2'], 'rgb': {'r': rgb2[0], 'g': rgb2[1], 'b': rgb2[2]}},
            'difference': diff,
            'similarity': round(max(0, 100 - (diff / 7.65)), 2)
        })
    except Exception as e:
        logger.error(f"Error comparing colors: {str(e)}")
        return error_response("Comparison failed", 500)


@api.route('/tools/random', methods=['GET'])
def generate_random_color():
    """Generate random beautiful colors."""
    try:
        import random
        
        # Generate random colors with good saturation and brightness
        colors = []
        for _ in range(5):
            h = random.random()
            s = random.uniform(0.5, 1.0)
            v = random.uniform(0.5, 1.0)
            
            rgb = colorsys.hsv_to_rgb(h, s, v)
            hex_color = rgb_to_hex((int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))
            colors.append(hex_color)
        
        return jsonify({
            'success': True,
            'colors': colors,
            'count': len(colors)
        })
    except Exception as e:
        logger.error(f"Error generating random colors: {str(e)}")
        return error_response("Generation failed", 500)


@api.route('/tools/convert', methods=['POST'])
def convert_color_format():
    """Convert color between formats."""
    try:
        data = request.get_json()
        
        if not data or 'color' not in data:
            return error_response("Color required", 400)
        
        color = data['color']
        
        # Convert to RGB
        rgb = hex_to_rgb(color)
        
        # Convert to other formats
        h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        hsl_h, hsl_l, hsl_s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        
        return jsonify({
            'success': True,
            'hex': color.upper(),
            'rgb': {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]},
            'hsv': {'h': round(h*360, 1), 's': round(s*100, 1), 'v': round(v*100, 1)},
            'hsl': {'h': round(hsl_h*360, 1), 's': round(hsl_s*100, 1), 'l': round(hsl_l*100, 1)}
        })
    except Exception as e:
        logger.error(f"Error converting color: {str(e)}")
        return error_response("Conversion failed", 500)

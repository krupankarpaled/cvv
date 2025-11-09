"""Image palette extraction using K-means clustering."""
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import io
import base64
from typing import List, Dict, Tuple
from collections import Counter


def extract_palette_from_image(image_data: str, n_colors: int = 5, method: str = 'kmeans') -> Dict:
    """
    Extract dominant colors from an image.
    
    Args:
        image_data: Base64 encoded image or PIL Image
        n_colors: Number of colors to extract
        method: 'kmeans' or 'median_cut'
    
    Returns:
        Dictionary with palette information
    """
    try:
        # Decode image
        if isinstance(image_data, str):
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            image = image_data
        
        # Convert to RGB
        image = image.convert('RGB')
        
        # Resize for performance
        max_size = 300
        if image.width > max_size or image.height > max_size:
            ratio = min(max_size / image.width, max_size / image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        if method == 'kmeans':
            return _extract_kmeans(image, n_colors)
        elif method == 'median_cut':
            return _extract_median_cut(image, n_colors)
        else:
            return _extract_kmeans(image, n_colors)
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def _extract_kmeans(image: Image.Image, n_colors: int) -> Dict:
    """Extract colors using K-means clustering."""
    # Convert image to numpy array
    pixels = np.array(image)
    pixels = pixels.reshape(-1, 3)
    
    # Remove very dark and very bright pixels (optional filtering)
    # This can improve results by removing pure black/white artifacts
    mask = np.all((pixels > 10) & (pixels < 245), axis=1)
    filtered_pixels = pixels[mask] if mask.sum() > 100 else pixels
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(filtered_pixels)
    
    # Get cluster centers (dominant colors)
    colors = kmeans.cluster_centers_.astype(int)
    
    # Get labels for all pixels
    labels = kmeans.predict(pixels)
    
    # Count occurrences
    label_counts = Counter(labels)
    total_pixels = len(labels)
    
    # Create palette
    palette = []
    for i, color in enumerate(colors):
        count = label_counts.get(i, 0)
        percentage = (count / total_pixels) * 100
        
        r, g, b = int(color[0]), int(color[1]), int(color[2])
        hex_color = f"#{r:02x}{g:02x}{b:02x}".upper()
        
        palette.append({
            "hex": hex_color,
            "rgb": {"r": r, "g": g, "b": b},
            "percentage": round(percentage, 2),
            "pixels": count
        })
    
    # Sort by percentage
    palette.sort(key=lambda x: x["percentage"], reverse=True)
    
    return {
        "success": True,
        "palette": palette,
        "n_colors": n_colors,
        "method": "kmeans",
        "total_pixels": total_pixels
    }


def _extract_median_cut(image: Image.Image, n_colors: int) -> Dict:
    """Extract colors using median cut algorithm (PIL's quantize)."""
    # Quantize image
    quantized = image.quantize(colors=n_colors, method=Image.Quantize.MEDIANCUT)
    
    # Get palette
    palette_data = quantized.getpalette()
    
    # Count pixels for each color
    pixel_data = np.array(quantized)
    total_pixels = pixel_data.size
    
    palette = []
    for i in range(n_colors):
        r = palette_data[i * 3]
        g = palette_data[i * 3 + 1]
        b = palette_data[i * 3 + 2]
        
        hex_color = f"#{r:02x}{g:02x}{b:02x}".upper()
        count = np.sum(pixel_data == i)
        percentage = (count / total_pixels) * 100
        
        palette.append({
            "hex": hex_color,
            "rgb": {"r": r, "g": g, "b": b},
            "percentage": round(percentage, 2),
            "pixels": int(count)
        })
    
    # Sort by percentage
    palette.sort(key=lambda x: x["percentage"], reverse=True)
    
    return {
        "success": True,
        "palette": palette,
        "n_colors": n_colors,
        "method": "median_cut",
        "total_pixels": total_pixels
    }


def analyze_color_distribution(image_data: str) -> Dict:
    """Analyze overall color distribution in an image."""
    try:
        # Decode image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Convert to numpy array
        pixels = np.array(image).reshape(-1, 3)
        
        # Calculate statistics
        avg_color = pixels.mean(axis=0).astype(int)
        dominant_channel = ['Red', 'Green', 'Blue'][pixels.mean(axis=0).argmax()]
        
        # Color temperature
        avg_r, avg_g, avg_b = avg_color
        warmth = (avg_r + avg_g) / 2 - avg_b
        temperature = "warm" if warmth > 0 else "cool"
        
        # Brightness
        brightness = pixels.mean()
        
        # Saturation (simplified)
        max_vals = pixels.max(axis=1)
        min_vals = pixels.min(axis=1)
        saturation = ((max_vals - min_vals) / (max_vals + 1e-6)).mean() * 100
        
        return {
            "success": True,
            "average_color": {
                "hex": f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}".upper(),
                "rgb": {"r": int(avg_r), "g": int(avg_g), "b": int(avg_b)}
            },
            "dominant_channel": dominant_channel,
            "temperature": temperature,
            "warmth_value": round(float(warmth), 2),
            "brightness": round(float(brightness), 2),
            "saturation": round(float(saturation), 2)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def extract_palette_by_region(image_data: str, regions: List[Dict]) -> Dict:
    """Extract palette from specific regions of an image."""
    try:
        # Decode image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        results = []
        
        for region in regions:
            x, y, width, height = region['x'], region['y'], region['width'], region['height']
            
            # Crop region
            cropped = image.crop((x, y, x + width, y + height))
            
            # Extract palette from this region
            palette_result = extract_palette_from_image(cropped, n_colors=3, method='kmeans')
            
            if palette_result.get('success'):
                results.append({
                    "region": region,
                    "palette": palette_result['palette']
                })
        
        return {
            "success": True,
            "regions": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

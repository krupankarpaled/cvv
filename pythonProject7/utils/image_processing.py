"""Image processing utilities for color detection."""
import logging
import base64
import numpy as np
import cv2

logger = logging.getLogger(__name__)


def validate_image_data(data: dict) -> bool:
    """Validate image data from request."""
    if not data or 'image' not in data:
        return False
    if not isinstance(data['image'], str) or not data['image'].startswith('data:image'):
        return False
    return True


def decode_image(image_data: str) -> np.ndarray:
    """Decode base64 image data to numpy array."""
    try:
        img_data = base64.b64decode(image_data.split(',')[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Failed to decode image")
        return frame
    except Exception as e:
        logger.error(f"Image decoding error: {str(e)}")
        raise ValueError(f"Image decoding failed: {str(e)}")


def extract_color_from_image(frame: np.ndarray, x: int = None, y: int = None, size: int = 60) -> tuple:
    """Extract average color from image ROI."""
    h, w = frame.shape[:2]
    cx = x if x is not None else w // 2
    cy = y if y is not None else h // 2
    
    # Ensure ROI is within bounds
    x1 = max(0, cx - size)
    y1 = max(0, cy - size)
    x2 = min(w, cx + size)
    y2 = min(h, cy + size)
    
    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        raise ValueError("Invalid ROI")
    
    avg = roi.mean(axis=(0, 1))
    avg_bgr = tuple(map(int, avg))
    avg_rgb = (avg_bgr[2], avg_bgr[1], avg_bgr[0])
    
    return avg_rgb

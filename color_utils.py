import cv2
import numpy as np

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV with proper scaling and type handling"""
    try:
        # Ensure inputs are proper numeric types
        r, g, b = float(r), float(g), float(b)
        
        # Normalize RGB values
        r, g, b = r/255.0, g/255.0, b/255.0
        
        # Calculate HSV manually to avoid OpenCV uint8 limitations
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Calculate Hue
        if max_val == min_val:
            h = 0.0
        elif max_val == r:
            h = (60 * ((g - b)/diff) + 360) % 360
        elif max_val == g:
            h = (60 * ((b - r)/diff) + 120) % 360
        elif max_val == b:
            h = (60 * ((r - g)/diff) + 240) % 360
            
        # Calculate Saturation
        s = 0.0 if max_val == 0.0 else (diff / max_val)
        
        # Value is simply max_val
        v = max_val
        
        return (h, s, v)
    except Exception as e:
        print(f"Error in HSV conversion: {e}")
        return (0.0, 0.0, 0.0)

def rgb_to_cmyk(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k) if (1 - k) != 0 else 0
    m = (1 - g - k) / (1 - k) if (1 - k) != 0 else 0
    y = (1 - b - k) / (1 - k) if (1 - k) != 0 else 0
    return (round(c*100), round(m*100), round(y*100), round(k*100))

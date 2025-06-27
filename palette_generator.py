import cv2
import numpy as np

def generate_palette(r, g, b):
    # Generate complementary and analogous colors
    hsv = cv2.cvtColor(np.uint8([[[r, g, b]]]), cv2.COLOR_RGB2HSV)[0][0]
    h, s, v = hsv
    
    # Complementary color
    comp_h = (h + 90) % 180
    comp_rgb = cv2.cvtColor(np.uint8([[[comp_h, s, v]]]), cv2.COLOR_HSV2RGB)[0][0]
    
    # Analogous colors (30° apart)
    ana1_h = (h + 30) % 180
    ana2_h = (h - 30) % 180
    ana1_rgb = cv2.cvtColor(np.uint8([[[ana1_h, s, v]]]), cv2.COLOR_HSV2RGB)[0][0]
    ana2_rgb = cv2.cvtColor(np.uint8([[[ana2_h, s, v]]]), cv2.COLOR_HSV2RGB)[0][0]
    
    return {
        'complementary': comp_rgb,
        'analogous1': ana1_rgb,
        'analogous2': ana2_rgb
    }

def simulate_color_blindness(r, g, b, mode='protanopia'):
    # Simulate different types of color blindness
    if mode == 'protanopia':
        return (0.567 * r + 0.433 * g, 0.558 * r + 0.442 * g, g)
    elif mode == 'deuteranopia':
        return (0.625 * r + 0.375 * g, 0.7 * r + 0.3 * g, g)
    elif mode == 'tritanopia':
        return (r, 0.95 * g + 0.05 * b, 0.433 * g + 0.567 * b)
    return (r, g, b)

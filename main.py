import cv2
import numpy as np
from color_utils import *
from color_names import get_color_name
from palette_generator import *
from clipboard import copy_with_message

# Read the image
img_path = 'new.jpg'
img = cv2.imread(img_path)
if img is None:
    print(f"Error: Could not load image at {img_path}")
    print("Please ensure the image file exists and is accessible")
    exit(1)

try:
    img = cv2.resize(img, (800, 600))
except Exception as e:
    print(f"Error resizing image: {e}")
    exit(1)

# Global variables
clicked = False
r = g = b = xpos = ypos = 0

# Mouse callback
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        
        # Always get color under cursor
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        
        # Prepare color values
        color_name = get_color_name(r, g, b)
        rgb_text = f"{r}, {g}, {b}"
        hex_color = rgb_to_hex(r, g, b)
        h, s, v = rgb_to_hsv(r, g, b)
        # Ensure HSV values are properly scaled and clamped
        h = min(360, max(0, round(h * 360)))
        s = min(100, max(0, round(s * 100)))
        v = min(100, max(0, round(v * 100)))
        hsv_text = f"{h}°, {s}%, {v}%"
        
        # Check if click is on color info area (y between 20-150)
        if 20 <= y <= 150 and 30 <= x <= 200:
            # Selective copying when clicking format labels
            if 40 <= y <= 70:   # Color name
                copy_with_message(color_name, "Color Name")
                cv2.putText(img, "Copied Color Name!", (250, 50), 2, 0.7, (255, 255, 255), 2)
            elif 70 <= y <= 100:  # RGB
                copy_with_message(rgb_text, "RGB")
                cv2.putText(img, "Copied RGB!", (250, 50), 2, 0.7, (255, 255, 255), 2)
            elif 100 <= y <= 130:  # HEX
                copy_with_message(hex_color, "HEX")
                cv2.putText(img, "Copied HEX!", (250, 50), 2, 0.7, (255, 255, 255), 2)
            elif 130 <= y <= 160:  # HSV
                copy_with_message(hsv_text, "HSV")
                cv2.putText(img, "Copied HSV!", (250, 50), 2, 0.7, (255, 255, 255), 2)

try:
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_function)
    print("Color Detector running - click on the image to detect colors")
    print("Press ESC or close window to exit")

    while True:
        cv2.imshow("Image", img)
        if clicked:
            # Convert to different color formats
            hex_color = rgb_to_hex(r, g, b)
            h, s, v = rgb_to_hsv(r, g, b)
            c, m, y, k = rgb_to_cmyk(r, g, b)
            
            # Draw info panel
            cv2.rectangle(img, (20, 20), (750, 120), (b, g, r), -1)
            
            # Display color info with copy indicators
            text_color = f"Color: {get_color_name(r, g, b)} [📋]"
            text_rgb = f"RGB: {r}, {g}, {b} [📋]"
            text_hex = f"HEX: {hex_color} [📋]"
            text_hsv = f"HSV: {h}°, {s}%, {v}% [📋]"
            text_cmyk = f"CMYK: {c}%, {m}%, {y}%, {k}%"
            
            # Draw info panel (larger to fit messages)
            cv2.rectangle(img, (20, 20), (750, 150), (b, g, r), -1)
            
            # Display color info
            cv2.putText(img, text_color, (30, 50), 2, 0.7, (255, 255, 255), 2)
            cv2.putText(img, text_rgb, (30, 80), 2, 0.7, (255, 255, 255), 2)
            cv2.putText(img, text_hex, (30, 110), 2, 0.7, (255, 255, 255), 2)
            cv2.putText(img, text_hsv, (30, 140), 2, 0.7, (255, 255, 255), 2)
            
            # For dark colors, use white text
            if r + g + b >= 600:
                cv2.putText(img, text_color, (30, 50), 2, 0.7, (0, 0, 0), 2)
                cv2.putText(img, text_rgb, (30, 80), 2, 0.7, (0, 0, 0), 2)
                cv2.putText(img, text_hex, (30, 110), 2, 0.7, (0, 0, 0), 2)
                cv2.putText(img, text_hsv, (30, 140), 2, 0.7, (0, 0, 0), 2)
            
            # Show copied message temporarily
            cv2.putText(img, "Copied to clipboard!", (250, 50), 2, 0.7, (255, 255, 255), 2)

            clicked = False

        # Exit with ESC or window close
        if cv2.waitKey(20) & 0xFF == 27 or cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Ensure windows are closed

except Exception as e:
    print(f"Error running color detector: {e}")
finally:
    cv2.destroyAllWindows()

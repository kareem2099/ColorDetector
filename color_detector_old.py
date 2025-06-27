import cv2
import pyperclip
import numpy as np

# Read the image
img_path = 'new.png'
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

# Color format conversion functions
def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def rgb_to_hsv(r, g, b):
    rgb = np.uint8([[[r, g, b]]])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    return tuple(hsv[0][0])

def rgb_to_cmyk(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k) if (1 - k) != 0 else 0
    m = (1 - g - k) / (1 - k) if (1 - k) != 0 else 0
    y = (1 - b - k) / (1 - k) if (1 - k) != 0 else 0
    return (round(c*100), round(m*100), round(y*100), round(k*100))

def get_color_name(r, g, b):
    # Enhanced color name detection using HSV space
    hsv = cv2.cvtColor(np.uint8([[[r, g, b]]]), cv2.COLOR_RGB2HSV)[0][0]
    h, s, v = hsv
    
    # First check for achromatic colors
    if v < 20: return "Black"
    if v > 230 and s < 30: return "White"
    if s < 30 and v > 100: return "Gray"
    
    # Then check for chromatic colors with adjusted hue ranges
    if h < 15: return "Red"
    elif h < 35: return "Orange"
    elif h < 65: return "Yellow"
    elif h < 90: return "Lime"
    elif h < 110: return "Green"
    elif h < 140: return "Teal"
    elif h < 170: return "Cyan"
    elif h < 200: return "Sky Blue"
    elif h < 240: return "Blue"
    elif h < 270: return "Purple"
    elif h < 300: return "Magenta"
    elif h < 330: return "Pink"
    else: return "Red"

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

def copy_with_message(text, format_name):
    pyperclip.copy(text)
    print(f"Successfully copied {format_name} to clipboard: {text}")

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

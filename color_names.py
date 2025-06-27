import math
import csv
from collections import namedtuple
from pathlib import Path

Color = namedtuple('Color', ['name', 'r', 'g', 'b'])

# Load colors from CSV file
def load_colors():
    colors = []
    csv_path = Path(__file__).parent / 'colors.csv'
    print(f"Loading colors from: {csv_path}")
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f"CSV headers: {reader.fieldnames}")
            for i, row in enumerate(reader, 1):
                colors.append(Color(
                    name=row['color_name'],
                    r=int(row['R']),
                    g=int(row['G']),
                    b=int(row['B'])
                ))
            print(f"Successfully loaded {i} colors")
    except Exception as e:
        print(f"Error loading colors: {e}")
    return colors

COLORS = load_colors()

def color_distance(c1, c2):
    """Calculate perceptual color distance using Delta E (CIE76)"""
    # Convert RGB to LAB color space
    def rgb_to_lab(rgb):
        # Convert RGB to XYZ
        r, g, b = [x/255.0 for x in rgb]
        
        r = r**2.2 if r > 0.04045 else r/12.92
        g = g**2.2 if g > 0.04045 else g/12.92
        b = b**2.2 if b > 0.04045 else b/12.92
        
        x = r*0.4124 + g*0.3576 + b*0.1805
        y = r*0.2126 + g*0.7152 + b*0.0722
        z = r*0.0193 + g*0.1192 + b*0.9505
        
        # Convert XYZ to LAB
        x /= 0.95047
        z /= 1.08883
        
        x = x**(1/3) if x > 0.008856 else 7.787*x + 16/116
        y = y**(1/3) if y > 0.008856 else 7.787*y + 16/116
        z = z**(1/3) if z > 0.008856 else 7.787*z + 16/116
        
        l = max(0, 116*y - 16)
        a = 500*(x - y)
        b = 200*(y - z)
        
        return (l, a, b)
    
    lab1 = rgb_to_lab((c1.r, c1.g, c1.b))
    lab2 = rgb_to_lab((c2.r, c2.g, c2.b))
    
    # Calculate Delta E (CIE76)
    return math.sqrt(
        (lab1[0]-lab2[0])**2 + 
        (lab1[1]-lab2[1])**2 + 
        (lab1[2]-lab2[2])**2
    )

def get_color_name(r, g, b):
    """Find closest named color using professional database"""
    input_color = Color("input", r, g, b)
    closest = min(COLORS, key=lambda c: color_distance(input_color, c))
    return closest.name

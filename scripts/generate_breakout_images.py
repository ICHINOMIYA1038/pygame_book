import os
from PIL import Image, ImageDraw, ImageFont
import random
import math

# Configuration
OUTPUT_DIR_BOOK = "books/python_breakout"
OUTPUT_DIR_IMAGES = "images/python_breakout"

# Ensure directories exist
os.makedirs(OUTPUT_DIR_BOOK, exist_ok=True)
os.makedirs(OUTPUT_DIR_IMAGES, exist_ok=True)

# Colors
COLOR_BG = (20, 20, 30)  # Dark Blue-ish Black
COLOR_PADDLE = (0, 128, 255)
COLOR_BALL = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (255, 200, 50)
BLOCK_COLORS = [
    (255, 100, 100),  # Red
    (255, 200, 100),  # Orange
    (255, 255, 100),  # Yellow
    (100, 255, 100),  # Green
    (100, 200, 255),  # Light Blue
]

def get_font(size):
    # Try common fonts on macOS/Linux/Windows
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

def draw_text_centered(draw, text, x, y, font, color=COLOR_TEXT):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((x - text_width / 2, y - text_height / 2), text, font=font, fill=color)

def create_cover():
    width, height = 800, 600
    img = Image.new("RGB", (width, height), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Draw Title
    title_font = get_font(80)
    subtitle_font = get_font(40)
    
    draw_text_centered(draw, "Python", width // 2, height // 3 - 40, title_font)
    draw_text_centered(draw, "Breakout", width // 2, height // 3 + 50, title_font, COLOR_ACCENT)
    draw_text_centered(draw, "Game Programming for Beginners", width // 2, height // 2 + 20, subtitle_font, (200, 200, 200))

    # Draw blocks at the bottom for decoration
    block_w, block_h = 60, 20
    rows = 3
    cols = width // block_w + 1
    for r in range(rows):
        for c in range(cols):
            color = BLOCK_COLORS[r % len(BLOCK_COLORS)]
            x = c * block_w
            y = height - (rows - r) * block_h
            draw.rectangle([x, y, x + block_w - 2, y + block_h - 2], fill=color)

    # Draw a ball and paddle stylized
    draw.rectangle([width//2 - 60, height - 100, width//2 + 60, height - 85], fill=COLOR_PADDLE)
    draw.ellipse([width//2 - 10, height - 130, width//2 + 10, height - 110], fill=COLOR_BALL)

    path = os.path.join(OUTPUT_DIR_BOOK, "cover.png")
    img.save(path)
    print(f"Created {path}")

def create_summary_01():
    # Chapter 1: Paddle Movement
    width, height = 600, 400
    img = Image.new("RGB", (width, height), (30, 30, 40))
    draw = ImageDraw.Draw(img)
    font = get_font(24)
    title_font = get_font(32)

    draw_text_centered(draw, "Chapter 1: Move the Paddle", width // 2, 40, title_font)

    # Screen representation
    screen_rect = [100, 80, 500, 350]
    draw.rectangle(screen_rect, outline=(100, 100, 100), width=2)
    
    # Paddle
    px, py = 300, 320
    pw, ph = 80, 15
    draw.rectangle([px - pw//2, py - ph//2, px + pw//2, py + ph//2], fill=COLOR_PADDLE)
    
    # Arrows
    arrow_y = 360
    # Left Arrow
    draw.polygon([(240, arrow_y), (260, arrow_y-10), (260, arrow_y+10)], fill=(200, 200, 200))
    draw_text_centered(draw, "Left", 250, arrow_y + 20, get_font(16))
    
    # Right Arrow
    draw.polygon([(360, arrow_y), (340, arrow_y-10), (340, arrow_y+10)], fill=(200, 200, 200))
    draw_text_centered(draw, "Right", 350, arrow_y + 20, get_font(16))

    # Explanation text
    draw_text_centered(draw, "Class Paddle", 300, 280, font, COLOR_ACCENT)

    path = os.path.join(OUTPUT_DIR_IMAGES, "summary_01.png")
    img.save(path)
    print(f"Created {path}")

def create_summary_02():
    # Chapter 2: Ball Physics
    width, height = 600, 400
    img = Image.new("RGB", (width, height), (30, 30, 40))
    draw = ImageDraw.Draw(img)
    font = get_font(24)
    title_font = get_font(32)

    draw_text_centered(draw, "Chapter 2: Ball Physics", width // 2, 40, title_font)

    # Ball
    bx, by = 300, 200
    r = 10
    draw.ellipse([bx-r, by-r, bx+r, by+r], fill=COLOR_BALL)

    # Vectors
    # dx
    draw.line([bx, by, bx+50, by], fill=(255, 100, 100), width=3)
    draw_text_centered(draw, "dx (speed x)", bx+40, by-20, get_font(18), (255, 100, 100))
    # dy
    draw.line([bx, by, bx, by-50], fill=(100, 255, 100), width=3)
    draw_text_centered(draw, "dy (speed y)", bx-60, by-30, get_font(18), (100, 255, 100))

    # Wall bounce
    wall_x = 500
    draw.line([wall_x, 100, wall_x, 300], fill=(150, 150, 150), width=4)
    
    # Path
    draw.line([400, 250, wall_x, 200], fill=(255, 255, 255), width=1)
    draw.line([wall_x, 200, 400, 150], fill=(255, 255, 255), width=1, joint="curve")
    
    draw_text_centered(draw, "dx = -dx", wall_x - 60, 200, font, COLOR_ACCENT)

    path = os.path.join(OUTPUT_DIR_IMAGES, "summary_02.png")
    img.save(path)
    print(f"Created {path}")

def create_summary_03():
    # Chapter 3: Collision
    width, height = 600, 400
    img = Image.new("RGB", (width, height), (30, 30, 40))
    draw = ImageDraw.Draw(img)
    font = get_font(24)
    title_font = get_font(32)

    draw_text_centered(draw, "Chapter 3: Collision & Game Over", width // 2, 40, title_font)

    # Paddle and Ball colliding
    px, py = 300, 250
    pw, ph = 80, 15
    draw.rectangle([px - pw//2, py - ph//2, px + pw//2, py + ph//2], fill=COLOR_PADDLE)
    
    bx, by = 300, 250 - ph//2 - 6 # just above paddle
    r = 6
    draw.ellipse([bx-r, by-r, bx+r, by+r], fill=COLOR_BALL)

    draw_text_centered(draw, "Hit!", 300, 210, font, COLOR_ACCENT)
    draw_text_centered(draw, "dy = -abs(dy)", 300, 290, get_font(20), (200, 200, 200))

    # Game Over Zone
    draw.line([100, 350, 500, 350], fill=(255, 50, 50), width=2)
    draw_text_centered(draw, "Screen Height (Limit)", 300, 370, get_font(18), (255, 100, 100))
    
    bx_out = 450
    by_out = 360
    draw.ellipse([bx_out-r, by_out-r, bx_out+r, by_out+r], fill=(100, 100, 100))
    draw_text_centered(draw, "Game Over", 450, 330, get_font(18), (200, 200, 200))

    path = os.path.join(OUTPUT_DIR_IMAGES, "summary_03.png")
    img.save(path)
    print(f"Created {path}")

def create_summary_04():
    # Chapter 4: Blocks Loop
    width, height = 600, 400
    img = Image.new("RGB", (width, height), (30, 30, 40))
    draw = ImageDraw.Draw(img)
    font = get_font(24)
    title_font = get_font(32)

    draw_text_centered(draw, "Chapter 4: Blocks & Loops", width // 2, 40, title_font)

    # Draw Grid
    start_x, start_y = 150, 120
    bw, bh = 50, 20
    margin = 5
    
    for r in range(3):
        color = BLOCK_COLORS[r]
        # Row Arrow
        draw_text_centered(draw, f"Row {r}", 80, start_y + r*(bh+margin) + bh//2, get_font(16))
        
        for c in range(4):
            x = start_x + c * (bw + margin)
            y = start_y + r * (bh + margin)
            draw.rectangle([x, y, x+bw, y+bh], fill=color)
            
            if r == 0:
                draw_text_centered(draw, f"Col {c}", x + bw//2, start_y - 20, get_font(14))

    # Explain Loop
    code_text = "for row in range(3):\n    for col in range(4):\n        create_block()"
    draw.text((150, 250), code_text, font=get_font(20), fill=(200, 255, 200))

    path = os.path.join(OUTPUT_DIR_IMAGES, "summary_04.png")
    img.save(path)
    print(f"Created {path}")

if __name__ == "__main__":
    create_cover()
    create_summary_01()
    create_summary_02()
    create_summary_03()
    create_summary_04()

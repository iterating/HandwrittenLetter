from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import json
from config.cors_config import CORS_CONFIG
from config.app_config import (
    LETTER_COLORS,
    FONT_SIZE,
    FONT_COLOR,
    IMAGE_MODE,
    IMAGE_SIZE,
    IMAGE_BACKGROUND,
    LETTERS_DIR,
    IMAGES_DIR,
    LETTER_SETS_DIR
)

app = Flask(__name__)
CORS(app, resources=CORS_CONFIG)

def get_font():
    """Get system font for text rendering"""
    try:
        # Try to use Arial font
        return ImageFont.truetype("arial.ttf", FONT_SIZE)
    except:
        # Fallback to default font
        return ImageFont.load_default()

def create_letter_image(char, font, size=IMAGE_SIZE):
    """Create a centered letter image"""
    if char == ' ':
        return Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
        
    img = Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Center the character
    bbox = draw.textbbox((0, 0), char, font=font)
    x = (size[0] - (bbox[2] - bbox[0])) // 2
    y = (size[1] - (bbox[3] - bbox[1])) // 2
    
    draw.text((x, y), char, fill=FONT_COLOR, font=font)
    return img.convert(IMAGE_MODE)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/api/save-letter', methods=['POST'])
def save_letter():
    try:
        data = request.get_json()
        letter = data.get('letter')
        image_data = data.get('imageData')
        
        if not letter or not image_data:
            return jsonify({"success": False, "error": "Missing letter or image data"}), 400
        
        # Remove data URL prefix
        image_data = image_data.split(',')[1]
        
        # Create directory if it doesn't exist
        for color in LETTER_COLORS:
            os.makedirs(os.path.join(LETTERS_DIR, color), exist_ok=True)
        
        # Convert base64 to image and save
        img_data = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_data))
        
        # Save for each color
        for color in LETTER_COLORS:
            img.save(os.path.join(LETTERS_DIR, color, f"{ord(letter)}.png"))
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-test-dataset', methods=['POST'])
def generate_test_dataset():
    try:
        data = request.get_json()
        letterlist = data.get('letterlist', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        font = get_font()
        
        # Create directories and generate images
        for color in LETTER_COLORS:
            os.makedirs(os.path.join(LETTER_SETS_DIR, 'set1', color), exist_ok=True)
            
            for char in letterlist:
                img = create_letter_image(char, font)
                img.save(os.path.join(LETTER_SETS_DIR, 'set1', color, f'{ord(char)}.png'))
        
        return jsonify({'success': True, 'message': f'Generated {len(letterlist)} characters'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/render', methods=['POST'])
def render_handwriting():
    try:
        text = request.get_json().get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        # Generate HTML
        html = ['<!DOCTYPE html><html><head><style>',
                '.lines { width: 100%; height: auto; float: left; }',
                '#paper { background: white; padding: 50px; width: 90%; }',
                'img, span { height: 25px; width: 15px; float: left; margin: 5px 0 10px; }',
                '</style></head><body><div id="paper">']
        
        # Add text lines
        for line in text.split('\n'):
            html.append('<div class="lines">')
            for char in line:
                html.append('<span></span>' if char == ' ' else 
                          f'<img src="/images/letters/set1/blue/{ord(char)}.png"/>')
            html.append('</div>')
            
        html.append('</div></body></html>')
        
        return jsonify({'success': True, 'html_content': ''.join(html)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

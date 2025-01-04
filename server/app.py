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
    img = Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Get text size
    text_width = draw.textlength(char, font=font)
    _, text_height = draw.textsize(char, font=font)
    
    # Calculate position to center text
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2
    
    # Draw text
    draw.text((x, y), char, font=font, fill=FONT_COLOR)
    return img

@app.route('/api/images/<path:filename>')
def serve_image(filename):
    """Serve image files"""
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/api/save-letter', methods=['POST'])
def save_letter():
    """Save a letter image"""
    try:
        data = request.get_json()
        letter = data.get('letter', '').upper()
        image_data = data.get('imageData', '')
        
        if not letter or not image_data:
            return jsonify({'error': 'Missing required data'}), 400
            
        # Create directory if it doesn't exist
        os.makedirs(LETTERS_DIR, exist_ok=True)
        
        # Remove header from base64 string
        image_data = image_data.split(',')[1]
        
        # Convert base64 to image
        image_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(image_bytes))
        
        # Save image
        filename = f"{letter}_{len(os.listdir(LETTERS_DIR))}.png"
        img.save(os.path.join(LETTERS_DIR, filename))
        
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-test', methods=['POST'])
def generate_test_dataset():
    """Generate test dataset with system font"""
    try:
        font = get_font()
        os.makedirs(LETTER_SETS_DIR, exist_ok=True)
        
        # Generate images for A-Z
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            img = create_letter_image(char, font)
            filename = f"{char}_0.png"
            img.save(os.path.join(LETTER_SETS_DIR, filename))
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/render', methods=['POST'])
def render_handwriting():
    """Render text using handwritten letters"""
    try:
        data = request.get_json()
        text = data.get('text', '').upper()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        # Get available letters
        available_letters = {}
        for filename in os.listdir(LETTERS_DIR):
            letter = filename.split('_')[0]
            if letter not in available_letters:
                available_letters[letter] = []
            available_letters[letter].append(filename)
            
        # Create output image
        total_width = len(text) * IMAGE_SIZE[0]
        img = Image.new(IMAGE_MODE, (total_width, IMAGE_SIZE[1]), IMAGE_BACKGROUND)
        
        # Place each letter
        x_offset = 0
        for char in text:
            if char in available_letters:
                # Randomly select a variant of the letter
                letter_file = random.choice(available_letters[char])
                letter_img = Image.open(os.path.join(LETTERS_DIR, letter_file))
                img.paste(letter_img, (x_offset, 0))
            x_offset += IMAGE_SIZE[0]
            
        # Save and return image
        output = io.BytesIO()
        img.save(output, format='PNG')
        img_str = base64.b64encode(output.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'imageData': f'data:image/png;base64,{img_str}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

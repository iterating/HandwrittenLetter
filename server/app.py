from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from PIL import Image, ImageDraw, ImageFont
import base64
import io

# Configuration
FONT_SIZE = 128
FONT_COLOR = "black"
IMAGE_MODE = "RGB"
IMAGE_SIZE = (200, 200)
IMAGE_BACKGROUND = "white"
LETTER_COLORS = ["black"]

# CORS Configuration
default_origins = ['https://handwrittenletter.vercel.app']
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',') or default_origins
if os.getenv('FLASK_ENV') == 'development':
    ALLOWED_ORIGINS.extend(['http://localhost:5173', 'http://127.0.0.1:5173'])

CORS_CONFIG = {
    r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
}

app = Flask(__name__)
CORS(app, resources=CORS_CONFIG)

def get_font():
    """Get system font for text rendering"""
    try:
        # Use default font in serverless environment
        font = ImageFont.load_default()
        print("Successfully loaded default font", file=sys.stderr)
        return font
    except Exception as e:
        print(f"Error loading font: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None

def create_letter_image(char, font, size=IMAGE_SIZE):
    """Create a centered letter image"""
    try:
        img = Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
        draw = ImageDraw.Draw(img)
        
        if font:
            # Get text size using font.getbbox
            bbox = font.getbbox(char)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position to center text
            x = (size[0] - text_width) / 2
            y = (size[1] - text_height) / 2
            
            # Draw text
            draw.text((x, y), char, font=font, fill=FONT_COLOR)
        else:
            # Fallback to basic text rendering
            draw.text((size[0]/4, size[1]/4), char, fill=FONT_COLOR)
        
        print(f"Successfully created image for character: {char}", file=sys.stderr)
        return img
    except Exception as e:
        print(f"Error creating letter image: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise

@app.route('/api/render', methods=['POST'])
def render_handwriting():
    try:
        print("Starting render_handwriting endpoint", file=sys.stderr)
        data = request.get_json()
        text = data.get('text', '')
        print(f"Received text: {text}", file=sys.stderr)
        
        # Get font
        font = get_font()
        print(f"Font loaded: {font is not None}", file=sys.stderr)
        
        # Create image for text
        img = create_letter_image(text[0] if text else 'A', font)
        print("Image created successfully", file=sys.stderr)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        print("Image converted to base64", file=sys.stderr)
        
        return jsonify({
            'image': f'data:image/png;base64,{img_str}',
            'text': text
        })
    except Exception as e:
        print(f"Error in render_handwriting: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-test-dataset', methods=['POST'])
def generate_test_dataset():
    try:
        print("Starting generate_test_dataset endpoint", file=sys.stderr)
        # Generate a single test image
        font = get_font()
        print(f"Font loaded: {font is not None}", file=sys.stderr)
        
        img = create_letter_image('A', font)
        print("Test image created successfully", file=sys.stderr)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        print("Image converted to base64", file=sys.stderr)
        
        return jsonify({
            'image': f'data:image/png;base64,{img_str}',
            'success': True
        })
    except Exception as e:
        print(f"Error in generate_test_dataset: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

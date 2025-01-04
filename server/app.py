from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from PIL import Image, ImageDraw
import base64
import io

# Configuration
IMAGE_MODE = "RGB"
IMAGE_SIZE = (200, 200)
IMAGE_BACKGROUND = "white"
FONT_COLOR = "black"

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

def create_letter_image(char, size=IMAGE_SIZE):
    """Create a simple letter image"""
    try:
        # Create new image
        img = Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
        draw = ImageDraw.Draw(img)
        
        # Draw text at fixed position
        draw.text((size[0]//3, size[1]//3), char, fill=FONT_COLOR)
        
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
        
        # Create image for text
        img = create_letter_image(text[0] if text else 'A')
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
        
        # Generate a simple test image
        img = create_letter_image('A')
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

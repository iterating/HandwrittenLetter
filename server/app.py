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

@app.route('/api/save-letter', methods=['POST'])
def save_letter():
    try:
        print("Starting save_letter endpoint", file=sys.stderr)
        data = request.get_json()
        letter = data.get('letter', '')
        image_data = data.get('imageData', '')
        
        if not letter or not image_data:
            return jsonify({'error': 'Missing letter or image data'}), 400
            
        print(f"Successfully processed letter: {letter}", file=sys.stderr)
        
        # In serverless environment, we'll just acknowledge receipt
        return jsonify({
            'success': True,
            'message': f'Processed letter {letter}'
        })
    except Exception as e:
        print(f"Error in save_letter: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

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
        data = request.get_json()
        letterlist = data.get('letterlist', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        print(f"Generating test dataset for letters: {letterlist}", file=sys.stderr)
        
        # Generate a simple test image for 'A'
        img = create_letter_image('A')
        print("Test image created successfully", file=sys.stderr)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        print("Image converted to base64", file=sys.stderr)
        
        return jsonify({
            'success': True,
            'message': 'Generated test dataset',
            'image': f'data:image/png;base64,{img_str}'
        })
    except Exception as e:
        print(f"Error in generate_test_dataset: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

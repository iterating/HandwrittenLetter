from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from PIL import Image, ImageDraw
import base64
import io

app = Flask(__name__)
CORS(app)

# Configuration
IMAGE_MODE = "RGB"
IMAGE_SIZE = (200, 200)
IMAGE_BACKGROUND = "white"
FONT_COLOR = "black"

def create_letter_image(char, size=IMAGE_SIZE):
    """Create a simple letter image"""
    try:
        # Create new image with white background
        img = Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
        draw = ImageDraw.Draw(img)
        
        # Draw text at center position
        x = size[0] // 2
        y = size[1] // 2
        draw.text((x, y), char, fill=FONT_COLOR)
        
        return img
    except Exception as e:
        print(f"Error creating letter image: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise

@app.route('/api/save-letter', methods=['POST'])
def save_letter():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        letter = data.get('letter', '')
        image_data = data.get('imageData', '')
        
        if not letter or not image_data:
            return jsonify({'error': 'Missing letter or image data'}), 400
            
        # Just acknowledge receipt in serverless environment
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
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        # Create image for first character
        img = create_letter_image(text[0])
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
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
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        # Generate a test image for 'A'
        img = create_letter_image('A')
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'message': 'Generated test dataset',
            'image': f'data:image/png;base64,{img_str}'
        })
    except Exception as e:
        print(f"Error in generate_test_dataset: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run()

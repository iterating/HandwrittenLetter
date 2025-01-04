from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from PIL import Image, ImageDraw
import base64
import io
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
IMAGE_MODE = "RGB"
IMAGE_SIZE = (200, 200)
IMAGE_BACKGROUND = "white"
FONT_COLOR = "black"

# CORS Configuration
ALLOWED_ORIGINS = [
    'https://handwrittenletter.vercel.app',
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.before_request
def log_request_info():
    logger.debug('Headers: %s', dict(request.headers))
    logger.debug('Method: %s', request.method)
    logger.debug('URL: %s', request.url)
    if request.is_json:
        logger.debug('JSON Body: %s', request.get_json())

def create_letter_image(char, size=IMAGE_SIZE):
    """Create a simple letter image"""
    try:
        # Create new image
        img = Image.new(IMAGE_MODE, size, IMAGE_BACKGROUND)
        draw = ImageDraw.Draw(img)
        
        # Draw text at fixed position
        draw.text((size[0]//3, size[1]//3), char, fill=FONT_COLOR)
        
        logger.info(f"Successfully created image for character: {char}")
        return img
    except Exception as e:
        logger.error(f"Error creating letter image: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@app.route('/api/save-letter', methods=['POST', 'OPTIONS'])
def save_letter():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        logger.info("Starting save_letter endpoint")
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        letter = data.get('letter', '')
        image_data = data.get('imageData', '')
        
        if not letter or not image_data:
            logger.error("Missing required fields")
            return jsonify({'error': 'Missing letter or image data'}), 400
            
        logger.info(f"Successfully processed letter: {letter}")
        
        return jsonify({
            'success': True,
            'message': f'Processed letter {letter}'
        })
    except Exception as e:
        logger.error(f"Error in save_letter: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/render', methods=['POST', 'OPTIONS'])
def render_handwriting():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        logger.info("Starting render_handwriting endpoint")
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        text = data.get('text', '')
        logger.info(f"Received text: {text}")
        
        # Create image for text
        img = create_letter_image(text[0] if text else 'A')
        logger.info("Image created successfully")
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        logger.info("Image converted to base64")
        
        return jsonify({
            'image': f'data:image/png;base64,{img_str}',
            'text': text
        })
    except Exception as e:
        logger.error(f"Error in render_handwriting: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-test-dataset', methods=['POST', 'OPTIONS'])
def generate_test_dataset():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        logger.info("Starting generate_test_dataset endpoint")
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        letterlist = data.get('letterlist', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        logger.info(f"Generating test dataset for letters: {letterlist}")
        
        # Generate a simple test image for 'A'
        img = create_letter_image('A')
        logger.info("Test image created successfully")
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        logger.info("Image converted to base64")
        
        return jsonify({
            'success': True,
            'message': 'Generated test dataset',
            'image': f'data:image/png;base64,{img_str}'
        })
    except Exception as e:
        logger.error(f"Error in generate_test_dataset: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Flask server is running'
    })

if __name__ == '__main__':
    app.run(debug=True)

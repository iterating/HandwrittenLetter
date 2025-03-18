from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from PIL import Image, ImageDraw
import base64
import io
import logging
from handwrite import create_letter, check_directory
import pygame

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize Pygame
pygame.init()

# Configuration
IMAGE_MODE = "RGB"
IMAGE_SIZE = (200, 200)
IMAGE_BACKGROUND = "white"
FONT_COLOR = "black"

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow requests from any origin
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Set additional CORS headers for all responses
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Log all requests
@app.before_request
def log_request_info():
    logger.info('Headers: %s', request.headers)
    logger.info('Body: %s', request.get_data())

def create_letter_image(char, size=IMAGE_SIZE):
    try:
        logger.info(f"Creating image for character: {char}")
        
        # Create new image with white background
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

@app.route('/api/save-letter', methods=['POST'])
def save_letter():
    """Save a letter image from the client"""
    logger.info("Received save-letter request")
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"success": False, "error": "No data received"})
        
        letter = data.get('letter')
        image_data = data.get('imageData')
        
        if not letter or not image_data:
            logger.error(f"Missing required fields: letter={bool(letter)}, imageData={bool(image_data)}")
            return jsonify({"success": False, "error": "Missing letter or image data"})
        
        # Remove the data:image/png;base64, prefix
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        logger.debug(f"Processing letter: {letter}")
        
        try:
            # Decode the base64 image
            image_bytes = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(image_bytes))
            
            # Get the directory for saving images
            base_dir = os.path.join('client', 'public', 'images', 'letters', 'set1')
            if not os.path.exists(base_dir):
                os.makedirs(base_dir, exist_ok=True)
                os.makedirs(os.path.join(base_dir, 'blue'), exist_ok=True)
                os.makedirs(os.path.join(base_dir, 'black'), exist_ok=True)
                logger.info(f"Created directories in: {base_dir}")
            
            # Save the image in both colors
            black_path = os.path.join(base_dir, 'black', f"{letter}.png")
            blue_path = os.path.join(base_dir, 'blue', f"{letter}.png")
            
            # Save original (black)
            img.save(black_path, 'PNG')
            
            # Create blue version
            blue_img = img.copy()
            pixels = blue_img.load()
            width, height = blue_img.size
            
            # Replace black with blue
            for i in range(width):
                for j in range(height):
                    r, g, b, a = pixels[i, j]
                    if r < 100 and g < 100 and b < 100 and a > 0:
                        pixels[i, j] = (0, 0, 255, a)  # Blue
            
            blue_img.save(blue_path, 'PNG')
            logger.info(f"Saved letter {letter} to {black_path} and {blue_path}")
            
            return jsonify({"success": True, "message": f"Letter {letter} saved successfully"})
        except Exception as e:
            logger.exception(f"Error processing image: {str(e)}")
            return jsonify({"success": False, "error": f"Error processing image: {str(e)}"})
            
    except Exception as e:
        logger.exception(f"Error in save_letter: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/render', methods=['POST'])
def render_handwriting():
    """Render text as handwritten HTML"""
    logger.info("Received render request")
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"success": False, "error": "No data received"})
        
        text = data.get('text', '')
        if not text:
            logger.error("No text provided for rendering")
            return jsonify({"success": False, "error": "No text provided"})
        
        logger.debug(f"Rendering text: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        # Get the directory for images
        base_dir = os.path.join('client', 'public', 'images', 'letters', 'set1')
        if not os.path.exists(base_dir):
            logger.error(f"Image directory not found: {base_dir}")
            return jsonify({"success": False, "error": "Image directory not found"})
        
        # Generate HTML
        html = ['<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Handwritten Text</title>',
                '<style>',
                'body { font-family: Arial, sans-serif; line-height: 1.6; }',
                '.handwritten { display: inline-block; margin: 0; padding: 0; }',
                '.handwritten img { height: 50px; margin: 0; padding: 0; vertical-align: middle; }',
                '</style></head><body><div class="handwritten">']
        
        for char in text:
            if char == '\n':
                html.append('<br/>')
            elif char == ' ':
                html.append('&nbsp; ')
            elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                img_path = f"/images/letters/set1/blue/{char}.png"
                html.append(f'<img src="{img_path}" alt="{char}" />')
            else:
                html.append(char)
        
        html.append('</div></body></html>')
        html_content = ''.join(html)
        
        logger.info("Successfully rendered handwritten text")
        return jsonify({"success": True, "html_content": html_content})
    except Exception as e:
        logger.exception(f"Error in render_handwriting: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/generate-test-dataset', methods=['POST'])
def generate_test_dataset():
    """Generate a test dataset of handwritten letters"""
    logger.info("Received generate-test-dataset request")
    try:
        data = request.get_json()
        letterlist = data.get('letterlist', "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        
        logger.debug(f"Generating test dataset for letters: {letterlist}")
        
        # Get the directory for saving images
        base_dir = os.path.join('client', 'public', 'images', 'letters', 'set1')
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
            os.makedirs(os.path.join(base_dir, 'blue'), exist_ok=True)
            os.makedirs(os.path.join(base_dir, 'black'), exist_ok=True)
            logger.info(f"Created directories in: {base_dir}")
        
        # Generate images for each letter
        for letter in letterlist:
            try:
                # Create a basic image for the letter
                img = create_letter_image(letter)
                
                # Save in black
                black_path = os.path.join(base_dir, 'black', f"{letter}.png")
                img.save(black_path, 'PNG')
                
                # Create blue version
                blue_img = img.copy()
                pixels = blue_img.load()
                width, height = blue_img.size
                
                # Replace black with blue
                for i in range(width):
                    for j in range(height):
                        r, g, b, a = pixels[i, j]
                        if r < 100 and g < 100 and b < 100 and a > 0:
                            pixels[i, j] = (0, 0, 255, a)  # Blue
                
                blue_path = os.path.join(base_dir, 'blue', f"{letter}.png")
                blue_img.save(blue_path, 'PNG')
                
                logger.debug(f"Generated test image for letter: {letter}")
            except Exception as e:
                logger.exception(f"Error generating image for letter {letter}: {str(e)}")
        
        logger.info(f"Successfully generated test dataset with {len(letterlist)} letters")
        return jsonify({"success": True, "message": f"Generated {len(letterlist)} test letters"})
    except Exception as e:
        logger.exception(f"Error in generate_test_dataset: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/log', methods=['POST'])
def client_log():
    """Receive and store logs from the frontend client"""
    try:
        data = request.get_json()
        if not data:
            logger.error("No log data received from client")
            return jsonify({"success": False, "error": "No data received"})
        
        level = data.get('level', 'info').upper()
        message = data.get('message', '')
        timestamp = data.get('timestamp', '')
        user_agent = data.get('userAgent', '')
        url = data.get('url', '')
        
        # Format the log message
        log_message = f"CLIENT [{level}] [{timestamp}] [{url}] [{user_agent}]: {message}"
        
        # Log using the appropriate level
        if level == 'ERROR':
            logger.error(log_message)
        elif level == 'WARN':
            logger.warning(log_message)
        elif level == 'DEBUG':
            logger.debug(log_message)
        else:
            logger.info(log_message)
            
        return jsonify({"success": True})
    except Exception as e:
        logger.exception(f"Error handling client log: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("Health check request received")
    return jsonify({"status": "healthy", "message": "API is running"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')

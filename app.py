from flask import Flask, request, jsonify, send_from_directory
import os
from PIL import Image, ImageDraw, ImageFont
import base64
import io

# Setup paths and constants
IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images'))
LETTER_SETS_DIR = os.path.join(IMAGES_DIR, "letters")
LETTER_COLORS = ("blue", "black")

app = Flask(__name__)

def get_font():
    """Get system font for text rendering"""
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    except:
        return ImageFont.load_default()

def create_letter_image(char, font, size=(30, 40)):
    """Create a centered letter image"""
    if char == ' ':
        return Image.new('L', size, 'white')
        
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Center the character
    bbox = draw.textbbox((0, 0), char, font=font)
    x = (size[0] - (bbox[2] - bbox[0])) // 2
    y = (size[1] - (bbox[3] - bbox[1])) // 2
    
    draw.text((x, y), char, fill='black', font=font)
    return img.convert('L')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/api/save-letter', methods=['POST'])
def save_letter():
    try:
        data = request.json
        letter = data['letter']
        image_data = data['imageData'].split(',')[1]  # Remove data URL prefix
        
        # Convert base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to grayscale
        image = image.convert('L')
        
        # Save for both colors
        for color in LETTER_COLORS:
            # Ensure directory exists
            letter_dir = os.path.join(LETTER_SETS_DIR, 'set1', color)
            os.makedirs(letter_dir, exist_ok=True)
            
            # Save image
            output_path = os.path.join(letter_dir, f'{ord(letter)}.png')
            image.save(output_path)
            print(f"Saved {letter} to {output_path}")
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving letter: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-test-dataset', methods=['POST'])
def generate_test_dataset():
    try:
        data = request.json
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
        text = request.json.get('text', '').strip()
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

import os

# Image configuration
FONT_SIZE = 128
FONT_COLOR = "black"
IMAGE_MODE = "RGB"
IMAGE_SIZE = (200, 200)
IMAGE_BACKGROUND = "white"
LETTER_COLORS = ["black"]

# Directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
LETTERS_DIR = os.path.join(IMAGES_DIR, "letters")
LETTER_SETS_DIR = os.path.join(IMAGES_DIR, "letter_sets")

"""
This script takes a text file containing a story and renders it as HTML. Each line is
rendered as a separate div, and each character is rendered as a separate image. The
images are chosen randomly from the images/letters directory, and the "color" of the
characters is changed every time the user types a '#' character.

The script also adds a background image to the output, which is specified in the
style sheet as images/background.png.

The output of the script is written to a file named output.html.
"""

import random
import os

LETTER_SETS_DIR = "images/letters"
BACKGROUND_IMAGE = "images/background.png"
OUTPUT_FILE = "output.html"
INPUT_FILE = "input.txt"

LETTER_COLORS = ("blue", "black")
CHARACTER_HEIGHT = 25
CHARACTER_WIDTH = 15
CHARACTER_MARGIN_TOP = 5
CHARACTER_MARGIN_BOTTOM = 10

html_content = [
    "<html>",
    "<head>",
    "<style>",
    ".lines { width: 100%; height: auto; float: left; }",
    f"#paper {{ background: white; background-image: url('{BACKGROUND_IMAGE}'); height: auto; float: left; padding: 50px 50px; width: 90%; }}",
    f"img, span {{ height: {CHARACTER_HEIGHT}px; width: {CHARACTER_WIDTH}px; float: left; margin-top: {CHARACTER_MARGIN_TOP}px; margin-bottom: {CHARACTER_MARGIN_BOTTOM}px; }}",
    ".clblack { filter: brightness(30%); }",
    ".clblue { filter: brightness(100%); }",
    "</style>",
    "</head>",
    "<body>",
    "<div id='paper'></div>"
]

try:
    with open(INPUT_FILE, "r") as file:
        for line in file:
            current_string = line.strip()
            html_content.append('<div class="lines">')
            current_letter_color = "blue"
            toggle_letter_color = False
            for character in current_string:
                character_code = ord(character)
                if character_code == 35:  # '#'
                    current_letter_color = LETTER_COLORS[toggle_letter_color]
                    toggle_letter_color = not toggle_letter_color
                elif character_code == 32 or character_code == 36:  # ' ' or '$'
                    html_content.append("<span></span>")
                else:
                    current_letter_set = f"set{random.randrange(1, len(os.listdir(LETTER_SETS_DIR)) + 1)}"
                    html_content.append(f"<img src='{LETTER_SETS_DIR}/{current_letter_set}/{current_letter_color}/{character_code}.png'/>")
            html_content.append("</div>")
    html_content.append("</div></body></html>")

    with open(OUTPUT_FILE, "w") as file:
        file.writelines(html_content)
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} not found.")
except Exception as e:
    print(f"An error occurred: {e}")
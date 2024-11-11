import os
import random

LETTER_SETS_DIR = "images/letters"
BACKGROUND_IMAGE = "images/background.png"
OUTPUT_FILE = "output.html"
INPUT_FILE = "input.txt"

LETTER_COLORS = ("blue", "black")
CHARACTER_HEIGHT = 25
CHARACTER_WIDTH = 15
CHARACTER_MARGIN_TOP = 5
CHARACTER_MARGIN_BOTTOM = 10

HTML_HEADER = [
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
    "<div id='paper'>",
]

def process_line(line, letter_sets_count):
    html_content = ['<div class="lines">']
    current_color = "blue"
    toggle_color = False
    for character in line.strip():
        character_code = ord(character)
        if character_code == 35:  # '#'
            current_color = LETTER_COLORS[toggle_color]
            toggle_color = not toggle_color
        elif character_code == 32 or character_code == 36:  # ' ' or '$'
            html_content.append("<span></span>")
        else:
            current_letter_set = f"set{random.randint(1, letter_sets_count)}"
            html_content.append(f"<img src='{LETTER_SETS_DIR}/{current_letter_set}/{current_color}/{character_code}.png'/>")
    html_content.append("</div>")
    return html_content

try:
    letter_sets_count = len(os.listdir(LETTER_SETS_DIR))
    with open(INPUT_FILE, "r") as file:
        lines = file.readlines()
    for line_number, line in enumerate(lines, start=1):
        HTML_HEADER.extend(process_line(line, letter_sets_count))
    HTML_HEADER.append("</div></body></html>")

    with open(OUTPUT_FILE, "w") as file:
        file.write("".join(HTML_HEADER))
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} not found.")


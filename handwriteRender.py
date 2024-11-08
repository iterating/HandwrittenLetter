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


current_letter_color = "blue"
current_letter_set = "set0"
toggle_letter_color = False
total_letter_sets = len(os.listdir("images/letters")) + 1

html_content = [
    "<html>",
    "<head>",
    "<style>",
    # set the background image for the output
    ".lines { width: 100%; height: auto; float: left; }",
    "#paper { background: white; background-image: url('images/background.png'); height: auto; float: left; padding: 50px 50px; width: 90%; }",
    # set the size of the characters
    "img, span { height: 25px; width: 15px; float: left; margin-top: 5px; margin-bottom: 10px; }",
    # set the brightness of the characters
    ".clblack { filter: brightness(30%); }",
    ".clblue { filter: brightness(100%); }",
    "</style>",
    "</head>",
    "<body>",
    "<div id='paper'></div>"
]


try:
    with open("input.txt", "r") as input_file:
        for line in input_file:
            # strips the newline character
            current_string = line.strip()
            html_content.append('<div class="lines">')
            for character in current_string:
                # get char ASCII Code of char
                character_code = ord(character)

                # select Random set
                random_letter_set = random.randrange(1, total_letter_sets)
                current_letter_set = f"set{random_letter_set}"

                if character_code == 35:
                    # toggle color of characters every time the user types a '#'
                    if toggle_letter_color:
                        current_letter_color = "blue"
                        toggle_letter_color = False
                    else:
                        current_letter_color = "black"
                        toggle_letter_color = True
                elif character_code == 32 or character_code == 36:
                    html_content.append("<span></span>")
                else:
                    html_content.append(
                        f"<img src='images/letters/{current_letter_set}/{current_letter_color}/{character_code}.png'/>"
                    )
            html_content.append("</div>")

    html_content.append("</div></body></html>")

    with open("output.html", "w") as output_html:
        output_html.writelines(html_content)
except FileNotFoundError:
    print("Error: input.txt not found.")
except Exception as e:
    print(f"An error occurred: {e}")



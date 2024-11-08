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


letter_color = "blue"
letter_set = "set0"
trcolor = False
totalset = len(os.listdir("images/letters")) + 1

htmlc = [
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
    with open("input.txt", "r") as textfile:
        for line in textfile:
            # strips the newline character
            curst = line.strip()
            htmlc.append('<div class="lines">')
            for ch in curst:
                # get char ASCII Code of char
                chcode = ord(ch)

                # select Random set
                random_letter = random.randrange(1, totalset)
                letter_set = f"set{random_letter}"

                if chcode == 35:
                    # toggle color of characters every time the user types a '#'
                    if trcolor:
                        letter_color = "blue"
                        trcolor = False
                    else:
                        letter_color = "black"
                        trcolor = True
                elif chcode == 32 or chcode == 36:
                    htmlc.append("<span></span>")
                else:
                    htmlc.append(
                        f"<img src='images/letters/{letter_set}/{letter_color}/{chcode}.png'/>"
                    )
            htmlc.append("</div>")

    htmlc.append("</div></body></html>")

    with open("output.html", "w") as output_html:
        output_html.writelines(htmlc)
except FileNotFoundError:
    print("Error: input.txt not found.")
except Exception as e:
    print(f"An error occurred: {e}")


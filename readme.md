# Convert typed text to handwritten letters

This project provides a simple tool for converting typed text into handwritten letters. The application is built using Python, Pygame, and Pillow libraries.

## Features

- Converts typed text into a handwritten format.
- Supports a variety of characters including alphabets, numbers, and special symbols.
- Renders the handwritten text into an HTML file with customizable styles.
- Randomly selects character styles from a predefined set of images.

## Installation

Ensure you have Python installed on your system. Then, install the required dependencies:

```bash
pip install pygame pillow
```

## Usage

To run the application, execute the following scripts:

1. Generate handwritten datasets by running `handwrite.py`.
2. Render the handwritten text into an HTML file using `handwriteRender.py`.

Each line is rendered as a separate div, and each character is rendered as a separate image. The images are chosen randomly from the images/letters directory,

The "color" of the characters is changed from blue to blackevery time the user types a '#' or '$' character.

The program also adds a background image to the output, which is specified in the
style sheet as images/background.png.

The output is written to a file named output.html.

## Directory Structure

- `handwrite.py`: Main script for generating handwriting trace datasets.
- `handwriteRender.py`: Script for rendering the handwriting into HTML.
- `images/`: Contains images used for rendering characters.
- `input.txt`: Input text file containing the text to be converted.
- `output.html`: The output file containing the rendered handwritten text.

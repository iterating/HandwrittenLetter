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

## Directory Structure

- `handwrite.py`: Main script for generating handwriting datasets.
- `handwriteRender.py`: Script for rendering the handwriting into HTML.
- `images/`: Contains images used for rendering characters.
- `output.html`: The output file containing the rendered handwritten text.

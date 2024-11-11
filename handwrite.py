import sys
import os
import pygame
from pygame.locals import *
from pygame import Color
from PIL import Image, ImageEnhance

# Constants
WIDTH = 500
HEIGHT = 350
DRAW_WIDTH = 200
DRAW_HEIGHT = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
try:
    pygame.init()
except pygame.error as e:
    print(f"Error: {e}")
    sys.exit()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Handwritten")

# Create a drawing surface
mydraw = pygame.Surface((DRAW_WIDTH, DRAW_HEIGHT), pygame.SRCALPHA)

# Program label
font = pygame.font.Font("freesansbold.ttf", 18)
text = font.render("Text To Hand Writing", True, (62, 97, 219))
screen.blit(text, (260, 30))

# Button coordinates and colors
createButton = (220, 65, 250, 35)
clearButton = (220, 110, 250, 35)
newSetButton = (220, 155, 250, 35)
editPrevButton = (220, 200, 250, 35)
noactcolor = (164, 170, 164)
actcolor = (184, 238, 57)
empty = Color(0, 0, 0, 0)

# Text coordinates
t1 = (320, 75)
t2 = (320, 120)
t3 = (300, 165)
t4 = (320, 210)
textCoords = (65, 320)
instructions = "Draw --> A"

# Text font size and style
txtfont = pygame.font.Font("freesansbold.ttf", 15)
txt1 = txtfont.render("Create", True, BLACK)
txt2 = txtfont.render("Clear", True, BLACK)
txt3 = txtfont.render("Create New Trace Set", True, BLACK)
txt4 = txtfont.render("Edit Previous", True, BLACK)

# Setup initial display
screen.blit(mydraw, (10, 10))
brush = pygame.transform.scale(pygame.image.load("images/brush.png"), (15, 15))
pygame.display.update()
clock = pygame.time.Clock()

# Variables
z = 0
actdirectory = "images/letters"
no_set = 0
actset = 0
letter_act_index = 0
letterlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.?{}()-_+=*&^%@<>|/'\"\\;:"
letter_images = []

def render_display():
    """Display the current instruction on the screen"""
    screen.fill(WHITE, (65, 320, 120, 100))
    textbox = font.render(instructions, True, BLACK)
    screen.blit(textbox, textCoords)

def check_directory():
    """Check if the directory exists and create it if it doesn't"""
    global actdirectory, no_set, actset
    sdir = os.path.isdir(actdirectory)
    if sdir:
        cdir = os.listdir("images/letters")
        no_set = len(cdir)
        actset = no_set + 1
        actdirectory = f"images/letters/set{actset}"
        os.mkdir(actdirectory)
        os.mkdir(actdirectory + "/blue")
        os.mkdir(actdirectory + "/black")
    else:
        os.mkdir("images/letters")
        actset = 1
        actdirectory = f"images/letters/set{actset}"
        os.mkdir(actdirectory)
        os.mkdir(actdirectory + "/blue")
        os.mkdir(actdirectory + "/black")

def create_letter():
    """Save the current letter as a PNG image and create a new letter"""
    global actdirectory, letter_act_index, instructions, letter_images
    letter = ord(letterlist[letter_act_index])
    imfile = f"{actdirectory}/blue/{letter}.png"
    pygame.image.save(mydraw, imfile)
    im = Image.open(imfile)
    enhancer = ImageEnhance.Brightness(im)
    factor = 0.35
    im_output = enhancer.enhance(factor)
    im_output.save(f"{actdirectory}/black/{letter}.png")
    letter_images.append((letter, imfile, f"{actdirectory}/black/{letter}.png"))
    letter_act_index += 1
    if letter_act_index < 87:
        instructions = f"Draw --> {letterlist[letter_act_index]}"
    else:
        instructions = "Set Done."
        btn_reset()

def reset_surface():
    """Reset the drawing surface"""
    pygame.draw.rect(screen, WHITE, (10, 10, DRAW_WIDTH, DRAW_HEIGHT))
    mydraw.fill(empty)
    pygame.draw.line(screen, (163, 163, 163), (10, 110), (210, 110), 1)
    pygame.draw.line(screen, (163, 163, 163), (10, 210), (210, 210), 1)
    pygame.draw.rect(screen, BLACK, (10, 10, DRAW_WIDTH, DRAW_HEIGHT), 2)

def btn_reset():
    """Reset the buttons"""
    pygame.draw.rect(screen, noactcolor, createButton)
    pygame.draw.rect(screen, noactcolor, clearButton)
    pygame.draw.rect(screen, noactcolor, newSetButton)
    pygame.draw.rect(screen, noactcolor, editPrevButton)
    screen.blit(txt1, t1)
    screen.blit(txt2, t2)
    screen.blit(txt3, t3)
    screen.blit(txt4, t4)
    pygame.display.update()

def btn_clicked(btnid):
    """Change the color of the button to show which one is active"""
    btn_reset()
    if btnid == 1:
        pygame.draw.rect(screen, actcolor, createButton)
        screen.blit(txt1, t1)
    elif btnid == 2:
        pygame.draw.rect(screen, actcolor, clearButton)
        screen.blit(txt2, t2)
    elif btnid == 3:
        pygame.draw.rect(screen, actcolor, newSetButton)
        screen.blit(txt3, t3)
    else:
        pygame.draw.rect(screen, actcolor, editPrevButton)
        screen.blit(txt4, t4)
    pygame.display.update()

def mouse_clicked(x, y):
    """Check if the mouse is clicked on a button and perform the action"""
    global letter_act_index, instructions, letter_images
    if createButton[0] < x < createButton[0] + createButton[2] and createButton[1] < y < createButton[1] + createButton[3]:
        btn_clicked(1)
        if letter_act_index < 87:
            create_letter()
        else:
            instructions = "Handwriting trace set done. Ready to render input.txt"
            btn_reset()
        reset_surface()
        render_display()
    elif clearButton[0] < x < clearButton[0] + clearButton[2] and clearButton[1] < y < clearButton[1] + clearButton[3]:
        btn_clicked(2)
        reset_surface()
    elif newSetButton[0] < x < newSetButton[0] + newSetButton[2] and newSetButton[1] < y < newSetButton[1] + newSetButton[3]:
        btn_clicked(3)
        check_directory()
        instructions = "Draw --> A"
        letter_act_index = 0
        letter_images = []
        render_display()
    elif editPrevButton[0] < x < editPrevButton[0] + editPrevButton[2] and editPrevButton[1] < y < editPrevButton[1] + editPrevButton[3]:
        btn_clicked(4)
        if letter_images:
            letter, blue_file, black_file = letter_images.pop()
            mydraw.fill(empty)
            img = pygame.image.load(blue_file)
            screen.blit(img, (10, 10))
            letter_act_index -= 1
            instructions = f"Redraw --> {chr(letter)}"
        else:
            instructions = "No previous letters to edit."
        reset_surface()
        render_display()

check_directory()
reset_surface()
render_display()
btn_reset()

while True:
    clock.tick(50)
    x, y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            z = 1
        elif event.type == MOUSEBUTTONUP:
            z = 0
            mouse_clicked(x, y)
            pygame.display.update()

        if z == 1:
            mydraw.blit(brush, (x - 14, y - 14))
            screen.blit(mydraw, (10, 10))
            pygame.display.update()
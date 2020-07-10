import pygame as pg
from time import sleep

width = 860
height = 700
screen = pg.display.set_mode((width, height))
bg = pg.display.set_mode((width, height))
pg.display.set_caption("Python Paint")
# Background (bg) to blit instead of screen cause that causes errors

# Colors:
background = (21, 30, 47)
color1 = (109, 130, 177)
color2 = (218, 214, 159)
black = (0, 0, 0)
light_black = (0, 0, 0, 1)
white = (255, 255, 255)
gray = (200, 200, 200, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)
color = white

clock = pg.time.Clock()
mouse = pg.mouse
mouseDown = False

screen.fill(background)

# Title, using make-text.io
title = pg.image.load('title.png')
bg.blit(title, (0, 0))

# Clear Button, using make-text.io
clearStartX = 600
clearEndX = 840
clearStartY = 120
clearEndY = 180
clearButton1 = pg.image.load('clear.png')
clearButton2 = pg.image.load('clear2.png')
bg.blit(clearButton1, (clearStartX, clearStartY))

# Test Button
tbStartX = 600
tbWidth = 240
tbStartY = 200
tbLength = 100
pg.draw.rect(bg, green, (tbStartX, tbStartY, tbWidth, tbLength))

# Big White Drawing Board:
#  x: (20,580) y: (120, 680)
# (580, 580)
drawingBoard = pg.Surface((560, 560))
bg.blit(drawingBoard, (20, 120))
drawingBoard.fill(black)
drawX = 20
drawX_width = 560
drawY = 120
drawY_length = 560

inDrawBoard = False

blockSize = 20 #Set the size of the grid block

ListX = []
ListY = []
ListDrawX = []
ListDrawY = []

pg.font.init()

mediumFont    = pg.font.SysFont("Times New Roman", 50)
bigFont    = pg.font.SysFont("Times New Roman", 100)

guessText = mediumFont.render("Guess:", 1, white)

def updateGuess(guess):
    if guess == 'clear':
        guessDisplay = bigFont.render(' ', 1, (255, 255, 255))
    else:
        guessDisplay = bigFont.render(str(guess), 1, (255, 255, 255))

    return guessDisplay

pg.init()


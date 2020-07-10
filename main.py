import pygame as pg
import keras
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import config
import time
import sys

def initialize():
    """ Draws the grid """
    for x in range(0, 28):
        config.ListDrawX.append((x * config.blockSize, x * config.blockSize + config.blockSize))
    for y in range(0, 28):
        config.ListDrawY.append((y * config.blockSize, y * config.blockSize + config.blockSize))
    for x in range(1, 29):
        config.ListX.append((x * config.blockSize, x * config.blockSize + config.blockSize))
    for y in range(6, 34):
        config.ListY.append((y * config.blockSize, y * config.blockSize + config.blockSize))


def drawingBoardBorder():
    """
    Draws a border around the driving board,
    which displays over any "ink" that goes outside the drawing board
    """
    # (Start X, Start Y, End X, End Y)
    pg.draw.rect(config.bg, config.background, (0, 100, 20, 680))    # Left of Drawing Board
    pg.draw.rect(config.bg, config.background, (580, 100, 20, 680))  # Right of Drawing Board
    pg.draw.rect(config.bg, config.background, (0, 680, 1000, 30))   # Bottom of drawing board
    pg.draw.rect(config.bg, config.background, (0, 90, 740, 30))    # Top of drawing board



def test(model):
    """ Feeds the number into the neural network and returns a prediction """
    pg.Surface.lock(config.drawingBoard)
    CV = []  # Color Values
    CVBinary = []  # Color Values but 1s or 0s

    for row in range(0, 560, 20):
        for column in range(0, 560, 20):
            new = pg.Surface.get_at(config.drawingBoard, (column, row))[:3]
            CV.append(new)

    for i in CV:
        if i == (0, 0, 0):    # black
            CVBinary.append(1.)
        else:
            CVBinary.append(0.)

    CVBinary = np.array(CVBinary).reshape((1, 28, 28, 1))
    
    print(CVBinary)

    predictions = model.predict(CVBinary)
    guess = np.argmax(predictions)
    print('GUESS: ', guess)

    pg.Surface.unlock(config.drawingBoard)

    return guess


def getPositions(num, num2):
    """ Records all positions (grid boxes) that have been colored in """
    positions = []
    try:
        positions.append(pg.Rect(config.ListDrawX[num][0]  , config.ListDrawY[num2][0]  , 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num+1][0], config.ListDrawY[num2][0]  , 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num-1][0], config.ListDrawY[num2][0]  , 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num][0]  , config.ListDrawY[num2+1][0], 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num][0]  , config.ListDrawY[num2-1][0], 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num+1][0], config.ListDrawY[num2+1][0], 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num+1][0], config.ListDrawY[num2-1][0], 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num-1][0], config.ListDrawY[num2+1][0], 20, 20))
        positions.append(pg.Rect(config.ListDrawX[num-1][0], config.ListDrawY[num2-1][0], 20, 20))
    except:
        pass

    for i in positions:
        pg.draw.rect(config.drawingBoard, config.white, i)


def draw(model):
    px, py = pg.mouse.get_pos()

    # Stops program if user clicks red X in the top right corner
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


        # Drawing script (complicated --> so that it only draws on the drawing board)
        for num in range(0, 28):
            if config.ListX[num][0] < px < config.ListX[num][1]:
                for num2 in range(0, 28):
                    if config.ListY[num2][0] < py < config.ListY[num2][1]:
                        if event.type == pg.MOUSEBUTTONDOWN:
                            getPositions(num, num2)
                            # Update background
                            config.bg.blit(config.drawingBoard, (20, 120))
                            config.mouseDown = True

                        elif event.type == pg.MOUSEMOTION and config.mouseDown:
                            getPositions(num, num2)
                            # Update background
                            config.bg.blit(config.drawingBoard, (20, 120))

        # When user releases mouse button, mouseDown is no longer true
        if event.type == pg.MOUSEBUTTONUP:
            config.mouseDown = False

        # Clear Button Script
        if config.clearStartX <= px <= config.clearEndX and config.clearStartY <= py <= config.clearEndY:
            config.bg.blit(config.clearButton2, (config.clearStartX, config.clearStartY))
            if event.type == pg.MOUSEBUTTONDOWN:
                config.drawingBoard.fill(config.black)
                config.bg.blit(config.drawingBoard, (20, 120))
                pg.draw.rect(config.bg, config.background, (600, 400, 200, 200))
                pass
        else:
            config.bg.blit(config.clearButton1, (config.clearStartX, config.clearStartY))


        # Test Number Button Script
        if config.tbStartX <= px <= config.tbStartX + config.tbWidth \
        and config.tbStartY <= py <= config.tbStartY  + config.tbLength:
            pg.draw.rect(config.bg, config.red, (config.tbStartX, config.tbStartY, config.tbWidth, config.tbLength))
            if event.type == pg.MOUSEBUTTONDOWN:
                guess = test(model)
                g = config.bg.blit(config.updateGuess(guess), (680, 450))
                pass
        else:
            pg.draw.rect(config.bg, config.green, (config.tbStartX, config.tbStartY, config.tbWidth, config.tbLength))

    # Update Guess Display:
    config.bg.blit(config.guessText, (650, 350))

    pg.display.update()
    config.clock.tick(3000)


def main():
    initialize()
    model = load_model('epic_num_reader.model')

    while True:
        drawingBoardBorder()
        draw(model)


if __name__ == "__main__":
    main()










import aspirin_display
import aspirin_input
import aspirin_logic
import pygame
import os


if __name__ == "__main__":
    # initialize PyGame
    pygame.init()

    gameStatus = aspirin_logic.GameStatus()
    gameWindow = aspirin_display.Window(384, 216, gameStatus)
    while True:
        gameWindow.redraw()
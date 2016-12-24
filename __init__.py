import aspirin_display
import aspirin_input
import aspirin_logic
import pygame

if __name__=="__main__":
    # initialize PyGame
    pygame.init()

    gameStatus = aspirin_logic.GameStatus()
    gameWindow = aspirin_display.Window(640, 480, gameStatus)
    while True:
        gameWindow.redraw()
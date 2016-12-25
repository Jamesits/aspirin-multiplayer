import pygame

import aspirin_display
import aspirin_input
import aspirin_logic

if __name__ == "__main__":
    # initialize PyGame
    pygame.init()

    gameStatus = aspirin_logic.GameStatus()
    gameStatus.color_preset = "white"
    gameWindow = aspirin_display.Window(384, 216, gameStatus)
    gameStatus.addInitialObjects()
    gameWindow.register_input_group(aspirin_input.KeyboardInputGroupWASD(gameStatus.getPlayers()[0]))
    while True:
        gameWindow.redraw()

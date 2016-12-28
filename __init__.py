import pygame

import aspirin_display
import aspirin_input
import aspirin_logic
import util

if __name__ == "__main__":
    # initialize PyGame
    pygame.init()

    gameStatus = aspirin_logic.GameStatus()
    gameStatus.color_preset = "white"
    gameWindow = aspirin_display.Window(384, 216, gameStatus)
    gameStatus.addInitialObjects()
    gameStatus.addObject(aspirin_logic.Player("Player2", x=gameStatus.width//4, y=gameStatus.height//4))
    gameWindow.register_input_group(aspirin_input.KeyboardInputGroupWASD(gameStatus.getPlayers()[0]))
    gameWindow.register_input_group(aspirin_input.KeyboardInputGroupUDLR(gameStatus.getPlayers()[1]))
    while True:
        gameWindow.redraw()

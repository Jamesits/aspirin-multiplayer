import pygame
import sys

import aspirin_display
import aspirin_input
import aspirin_logic

if __name__ == "__main__":
    # initialize PyGame
    pygame.init()

    # initialize network
    addr = sys.argv[1]
    port = int(sys.argv[2])
    nc = aspirin_input.NetworkComm(addr, port)
    gameStatus = aspirin_logic.GameStatus(nc=nc)
    gameStatus.color_preset = "white"
    gameWindow = aspirin_display.Window(384, 216, gameStatus)
    gameStatus.addInitialObjects()
    gameStatus.addObject(aspirin_logic.Player("Player2", x=gameStatus.width//4, y=gameStatus.height//4))
    gameWindow.register_input_group(aspirin_input.KeyboardInputGroupUDLR(gameStatus.getPlayers()[0], nc))
    gameWindow.register_input_group(aspirin_input.KeyboardInputGroup_fromnet(gameStatus.getPlayers()[1], nc))
    while True:
        gameWindow.redraw()

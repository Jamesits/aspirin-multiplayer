import aspirin_logic
import pygame
from pygame.locals import *
import pyganim
import sys


class Window:
    def __init__(self, width: int, height: int, status: aspirin_logic.GameStatus, fps: int=30, foreground_color: (int, int, int)=(255, 255, 255), background_color: (int, int, int)=(0, 0, 0)):
        # initialize window configs
        self.width = width
        self.height = height
        self.status = status
        status.registerDataBindingCallback(self.redraw)
        self.fps = fps
        self.foreground_color = foreground_color
        self.background_color = background_color

        # init drawing things
        self.font = pygame.font.Font("/Users/james/Library/Fonts/DejaVuSans.ttf", 16)
        self.animTypes = []
        self.animObjs = {}
        self.moveConductor = pyganim.PygConductor(self.animObjs)
        self.windowSurface = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.instructionSurf = self.font.render('Aspirin Multiplayer', True, self.foreground_color)
        self.instructionRect = self.instructionSurf.get_rect()
        self.instructionRect.bottomleft = (10, self.height - 10)

        # set window property
        self.mainClock = pygame.time.Clock()
        pygame.display.set_caption('Aspirin')

    def redraw(self):
        self.windowSurface.fill(self.background_color)

        # event handling loop
        for event in pygame.event.get():

            # handle ending the program
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        self.windowSurface.blit(self.instructionSurf, self.instructionRect)

        pygame.display.update()
        self.mainClock.tick(self.fps)

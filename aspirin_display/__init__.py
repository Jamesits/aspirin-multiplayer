import sys

import pygame
import pyganim
from pygame.locals import *

import aspirin_input
import aspirin_logic


class Window:
    def __init__(self, width: int, height: int, status: aspirin_logic.GameStatus, fps: int = 30, tickQuotient: int = 2):
        # initialize window configs
        self.width = width
        self.height = height
        self.status = status
        self.status.registerDataBindingCallback(self.redraw)
        self.fps = fps
        self.tickQuotient = tickQuotient

        # fixed drawing properties
        self.line_length = 20
        self.font_size = 20
        self.status_bar_height = 22

        # init drawing things
        self.font = pygame.font.Font("/Users/james/Library/Fonts/DejaVuSans.ttf", 16)
        self.animTypes = []
        self.animObjs = {}
        self.moveConductor = pyganim.PygConductor(self.animObjs)
        self.windowSurface = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.instructionSurf = self.font.render('Aspirin Multiplayer', True,
                                                self.status.getColorPreset().fgColor.toRGBA())
        self.instructionRect = self.instructionSurf.get_rect()
        self.instructionRect.bottomleft = (10, self.height - 10)

        self.eventHandlers = {}

        # set window property
        self.mainClock = pygame.time.Clock()
        pygame.display.set_caption('Aspirin')

        # runtime values
        self.tickCount = 0

    def draw_status_bar(self):
        pygame.draw.line(self.windowSurface, self.status.getColorPreset().fgColor.toRGBA(), (0, self.status_bar_height),
                         (self.width, self.status_bar_height))
        status_text = "Score "
        for o in self.status.objects:
            if isinstance(o, aspirin_logic.Player):
                status_text += "{}: {}".format(o.name, o.score)
        statusBarSurf = self.font.render(status_text, True, self.status.getColorPreset().fgColor.toRGBA())
        statusBarRect = statusBarSurf.get_rect()
        self.windowSurface.blit(statusBarSurf, statusBarRect)

    def register_input_group(self, inputgroup: 'aspirin_input.InputGroup'):
        if isinstance(inputgroup, aspirin_input.KeyboardInputGroup):
            keys, handlers = inputgroup.registerKeys()
            for key in keys:
                self.eventHandlers[key] = handlers
        else:
            raise NotImplementedError()

    def tick(self):
        for o in self.status.objects:
            if isinstance(o, aspirin_logic.GameObject):
                o.tick()

    def redraw(self):
        self.windowSurface.fill(self.status.getColorPreset().bgColor.toRGBA())

        # event handling loop
        for event in pygame.event.get():

            # handle ending the program
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type in [KEYDOWN, KEYUP]:
                if event.key in self.eventHandlers:
                    self.eventHandlers[event.key][event.type](event)

        # count tick
        if self.tickCount == 0:
            self.tick()
        self.tickCount = (self.tickCount + 1) % self.tickQuotient

        # draw everything
        self.draw_status_bar()
        for o in self.status.objects:
            if isinstance(o, aspirin_logic.GameObject):
                o.draw(self.windowSurface)

        self.windowSurface.blit(self.instructionSurf, self.instructionRect)

        pygame.display.update()
        self.mainClock.tick(self.fps)

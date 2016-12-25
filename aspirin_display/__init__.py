import aspirin_logic
import aspirin_input
import pygame
from pygame.locals import *
import pyganim
import sys
import os


class Color:
    def __init__(self, red: int=0, green: int=0, blue: int=0):
        self.red = red
        self.green = green
        self.blue = blue

    @classmethod
    def fromHEX(cls, hexstr: str="#000000"):
        if hexstr[0] != "#":
            raise SyntaxError()
        red, green, blue = tuple(int(hexstr.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return Color(red, green, blue)

    # this is for casting to tuple
    def __iter__(self):
        yield self.red
        yield self.green
        yield self.blue

    def toRGBA(self):
        return tuple(self)


class ColorPreset:
    def __init__(self, bgColor: Color=Color(0, 0, 0), fgColor: Color=Color(0, 0, 255), fgColor2: Color=Color(255, 0, 0), lineColor: Color=Color(0, 0, 255)):
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.fgColor2 = fgColor2
        self.lineColor = lineColor


class Window:
    def __init__(self, width: int, height: int, status: aspirin_logic.GameStatus, fps: int=30):
        # initialize window configs
        self.width = width
        self.height = height
        self.status = status
        self.status.registerDataBindingCallback(self.redraw)
        self.fps = fps

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
        self.instructionSurf = self.font.render('Aspirin Multiplayer', True, self.status.getColorPreset().fgColor.toRGBA())
        self.instructionRect = self.instructionSurf.get_rect()
        self.instructionRect.bottomleft = (10, self.height - 10)

        self.eventHandlers = {}

        # set window property
        self.mainClock = pygame.time.Clock()
        pygame.display.set_caption('Aspirin')

    def draw_status_bar(self):
        pygame.draw.line(self.windowSurface, self.status.getColorPreset().fgColor.toRGBA(), (0, self.status_bar_height), (self.width, self.status_bar_height))
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

        self.draw_status_bar()
        for o in self.status.objects:
            if isinstance(o, aspirin_logic.GameObject):
                o.tick()
                o.draw(self.windowSurface, self.status.getColorPreset())

        self.windowSurface.blit(self.instructionSurf, self.instructionRect)

        pygame.display.update()
        self.mainClock.tick(self.fps)

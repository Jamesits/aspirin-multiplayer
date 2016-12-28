import sys
import json

import pygame
from pygame.locals import *

import aspirin_input
import aspirin_logic


class NetworkEvent:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Window:
    def __init__(self, width: int, height: int, status: aspirin_logic.GameStatus, fps: int = 20, tickQuotient: int = 1):
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
        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.animTypes = []
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
                status_text += "{}: {} ".format(o.name, o.score)
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
        for o in self.status.objects:
            if isinstance(o, aspirin_logic.GameObject) and o.visibility:
                o.collisionDetect(self.status)

    def process_event(self, event, isProxiedEvent: bool=False):
        if event.type in [KEYDOWN, KEYUP]:
            if event.key in self.eventHandlers:
                self.eventHandlers[event.key][event.type](event, isProxiedEvent)

    def redraw(self):
        pygame.event.pump()
        self.windowSurface.fill(self.status.getColorPreset().bgColor.toRGBA())

        if self.status.game_status == aspirin_logic.GameStatus.Status.READY:
            self.instructionSurf = self.font.render('Aspirin Multiplayer: Press Enter to start game.', True,
                                                    self.status.getColorPreset().fgColor.toRGBA())
            self.windowSurface.blit(self.instructionSurf, self.instructionRect)

            for event in pygame.event.get():

                # handle ending the program
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.status.start()

        elif self.status.game_status == aspirin_logic.GameStatus.Status.ONAIR:
            # event handling loop
            for event in pygame.event.get():

                # handle ending the program
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                self.process_event(event)
                if self.status.nc:
                    recv_event, _ = self.status.nc.recv()
                    while recv_event:
                        s = recv_event.decode()
                        print("Recv: ", s)
                        e = NetworkEvent(**json.loads(s))
                        self.process_event(e, isProxiedEvent=True)
                        recv_event, _ = self.status.nc.recv()

            # count tick
            if self.tickCount == 0:
                self.tick()
            self.tickCount = (self.tickCount + 1) % self.tickQuotient

            # draw everything
            self.draw_status_bar()
            for o in self.status.objects:
                if isinstance(o, aspirin_logic.GameObject) and o.visibility:
                    o.draw(self.windowSurface)
        else:
            self.instructionSurf = self.font.render('Died, press ESC to quit.', True,
                                                    self.status.getColorPreset().fgColor.toRGBA())
            self.windowSurface.blit(self.instructionSurf, self.instructionRect)

            for event in pygame.event.get():

                # handle ending the program
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        self.mainClock.tick(self.fps)

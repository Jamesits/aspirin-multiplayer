import os
import pygame
import aspirin_display


class GameStatus:
    def __init__(self, width: int=384, height: int=216, color_preset="default"):
        self.color_presets = {
            "default": aspirin_display.ColorPreset()
        }
        self.load_color_presets()
        self.width = width
        self.height = height
        self.dataBindingCallbacks = []
        self.line_length = 20
        self.color_preset = color_preset
        self.scores = {"Player1": 100}

    def load_color_presets(self):
        for filename in os.listdir("color_presets"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            cp_name = os.path.splitext(filename)[0]
            cp_loader = __import__("color_presets." + cp_name, fromlist=[cp_name])
            self.color_presets.update(cp_loader.color_presets)

    def registerDataBindingCallback(self, func: callable):
        self.dataBindingCallbacks.append(func)

    def getColorPreset(self):
        return self.color_presets[self.color_preset]


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 5
        self.speed = 2

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)

    def tick(self):
        pass


class Obstacle:
    class Orientation:
        HORIZONTAL = 0
        VERTICAL = 1

    class Direction:
        LEFT_OR_UP = -1
        RIGHT_OR_DOWN = 1

    def __init__(self):
        self.top = 0
        self.left = 0
        self.length = 20
        self.speed = 20
        self.orientation = Obstacle.Orientation.HORIZONTAL
        self.direction = Obstacle.Direction.LEFT_OR_UP

    def get_end1(self):
        return self.top, self.left

    def get_end2(self):
        if self.orientation == Obstacle.Orientation.HORIZONTAL:
            return self.top, self.left + self.length * self.direction
        else:
            return self.top + self.length * self.direction, self.left

    def draw(self, screen, color):
        pygame.draw.line(screen, color, self.get_end1(), self.get_end2())

    def tick(self):
        if self.orientation == Obstacle.Orientation.HORIZONTAL:
            self.left += self.speed * self.direction
        else:
            self.top += self.speed * self.direction


class Target:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 10

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)

    def tick(self):
        pass

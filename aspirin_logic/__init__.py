import os
import pygame
import pygame.gfxdraw
import aspirin_display


class GameObject:
    def __init__(self):
        self.visibility = True

    def draw(self, screen, colorpreset: 'aspirin_display.ColorPreset'):
        raise NotImplementedError()

    def tick(self):
        raise NotImplementedError()


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
        self.objects = []

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

    def addObject(self, obj: GameObject):
        self.objects.append(obj)

    def addInitialObjects(self):
        self.addObject(Player("Player1", self.width // 2, self.height // 2))
        self.addObject(Target(self.width // 2, self.height // 4))

    def clearObject(self):
        self.objects.clear()

    def getPlayers(self):
        return [x for x in self.objects if isinstance(x, Player)]

    def resetGame(self):
        self.clearObject()
        self.addInitialObjects()


class Player(GameObject):
    def __init__(self, name: str, x: int=0, y: int = 0):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.size = 5
        self.speed = 2
        self.score = 0
        self.score_delta = 100
        self.h_movement_level = 0
        self.v_movement_level = 0

    def draw(self, screen, colorpreset: 'aspirin_display.ColorPreset'):
        pygame.gfxdraw.aacircle(screen, self.x, self.y, self.size, colorpreset.fgColor.toRGBA())

    def tick(self):
        self.x += self.h_movement_level * self.speed
        self.y += self.v_movement_level * self.speed

    def addScore(self, times: int=1):
        self.score += self.score_delta * times


class Obstacle(GameObject):
    class Orientation:
        HORIZONTAL = 0
        VERTICAL = 1

    class Direction:
        LEFT_OR_UP = -1
        RIGHT_OR_DOWN = 1

    def __init__(self):
        super().__init__()
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

    def draw(self, screen, colorpreset: 'aspirin_display.ColorPreset'):
        pygame.gfxdraw.line(screen, colorpreset.fgColor, self.get_end1(), self.get_end2())

    def tick(self):
        if self.orientation == Obstacle.Orientation.HORIZONTAL:
            self.left += self.speed * self.direction
        else:
            self.top += self.speed * self.direction


class Target(GameObject):
    def __init__(self, x: int=0, y: int=0):
        super().__init__()
        self.x = x
        self.y = y
        self.size = 10

    def draw(self, screen, colorpreset: 'aspirin_display.ColorPreset'):
        pygame.gfxdraw.aacircle(screen, self.x, self.y, self.size, colorpreset.fgColor2.toRGBA())

    def tick(self):
        pass

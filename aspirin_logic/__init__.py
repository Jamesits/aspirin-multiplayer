import os
import random
import math

import pygame
import pygame.gfxdraw

import util


class GameObject:
    def __init__(self, colorpreset: 'util.ColorPreset' = util.ColorPreset()):
        self.visibility = True
        self.colorpreset = colorpreset

    def getDrawingColor(self):
        return self.colorpreset.fgColor.toRGBA()

    def draw(self, screen):
        raise NotImplementedError()

    def tick(self):
        pass

    def collisionDetect(self, status: 'GameStatus'):
        pass


class CircularGameObject(GameObject):
    def __init__(self, x: int = 0, y: int = 0, size: int = 0, colorpreset: 'util.ColorPreset' = util.ColorPreset()):
        super().__init__(colorpreset)
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, self.x, self.y, self.size, self.getDrawingColor())


class LinearGameObject(GameObject):
    class Orientation:
        HORIZONTAL = 0
        VERTICAL = 1

    class Direction:
        LEFT_OR_UP = -1
        RIGHT_OR_DOWN = 1

    def __init__(self, top: int = 0, left: int = 0, length: int = 0, dire: int = Direction.RIGHT_OR_DOWN, ori: int = Orientation.HORIZONTAL, colorpreset: 'util.ColorPreset' = util.ColorPreset()):
        super().__init__(colorpreset)
        self.top = top
        self.left = left
        self.length = length
        self.direction = dire
        self.orientation = ori

    def get_end1(self):
        return self.top, self.left

    def get_end2(self):
        if self.orientation == LinearGameObject.Orientation.VERTICAL:
            return self.top, self.left + self.length
        else:
            return self.top + self.length, self.left

    def getDrawingColor(self):
        return self.colorpreset.fgColor.toRGBA()

    def draw(self, screen):
        x1, y1 = self.get_end1()
        x2, y2 = self.get_end2()
        pygame.gfxdraw.line(screen, x1, y1, x2, y2, self.getDrawingColor())

    def collisionDetect(self, status: 'GameStatus'):
        x1, y1 = self.get_end1()
        x2, y2 = self.get_end2()
        if self.orientation == LinearGameObject.Orientation.HORIZONTAL:
            if x1 <= 0 or x2 >= status.width:
                self.direction *= -1
        elif self.orientation == LinearGameObject.Orientation.VERTICAL:
            if y1 <= 0 or y2 >= status.height:
                self.direction *= -1
        else:
            raise AttributeError()


class GameStatus:
    class Status:
        READY = 0
        ONAIR = 1
        DIED = 2

    def __init__(self, width: int = 384, height: int = 216, color_preset="default"):
        self.color_presets = {
            "default": util.ColorPreset()
        }
        self.load_color_presets()
        self.width = width
        self.height = height
        self.dataBindingCallbacks = []
        self.line_length = 20
        self.color_preset = color_preset
        self.objects = []
        self.game_status = GameStatus.Status.READY
        self.game_speed = 0

    def start(self):
        self.game_status = GameStatus.Status.ONAIR

    def die(self):
        self.game_status = GameStatus.Status.DIED

    def nextLevel(self):
        self.addObject(Obstacle(random.randint(0, self.width), random.randint(0, self.height), 20, LinearGameObject.Orientation.HORIZONTAL))
        self.addObject(Obstacle(random.randint(0, self.width), random.randint(0, self.height), 20, LinearGameObject.Orientation.VERTICAL))

    def nextSpeed(self):
        self.game_speed += 1
        for o in self.objects:
            if isinstance(o, Player):
                o.speed = math.floor(self.game_speed + 2)
            elif isinstance(o, Obstacle):
                o.speed = math.floor(1.5 * self.game_speed + 2)

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
        # self.addInitialObjects()
        self.game_status = GameStatus.Status.READY
        self.game_speed = 0


class Player(CircularGameObject):
    def __init__(self, name: str, x: int = 0, y: int = 0, colorpreset: 'util.ColorPreset' = util.ColorPreset()):
        super().__init__(x, y, 5, colorpreset)
        self.name = name
        self.speed = 2
        self.score = 0
        self.score_delta = 100
        self.h_movement_level = 0
        self.v_movement_level = 0

    def getDrawingColor(self):
        return self.colorpreset.fgColor.toRGBA()

    def tick(self):
        self.x += self.h_movement_level * self.speed
        self.y += self.v_movement_level * self.speed

    def addScore(self, times: int = 1):
        self.score += self.score_delta * times

    def collisionDetect(self, status: 'GameStatus'):
        for o in status.objects:
            if isinstance(o, Obstacle):
                x1, y1 = o.get_end1()
                x2, y2 = o.get_end2()
                if o.orientation == LinearGameObject.Orientation.VERTICAL:
                    if y1 < self.y < y2 and self.x - self.size < x1 < self.x + self.size:
                        status.die()
                elif o.orientation == LinearGameObject.Orientation.HORIZONTAL:
                    if x1 < self.x < x2 and self.y - self.size < y1 < self.y + self.size:
                        status.die()
            elif isinstance(o, Target):
                if self.x - self.size < o.x + o.size and self.x + self.size > o.x - o.size and self.y - self.size < o.y + o.size and self.y + self.size > o.y - o.size:
                    self.addScore()
                    status.nextLevel()
                    if self.score // self.score_delta % 10 == 0:
                        status.nextSpeed()
                    o.randomPosition(status)


class Obstacle(LinearGameObject):
    def __init__(self, top: int = 0, left: int = 0, length: int = 0, ori: int = LinearGameObject.Orientation.HORIZONTAL, dire: int = LinearGameObject.Direction.RIGHT_OR_DOWN, colorpreset: 'util.ColorPreset' = util.ColorPreset()):
        super().__init__(top, left, length, dire, ori, colorpreset)
        self.speed = 2

    def tick(self):
        if self.orientation == LinearGameObject.Orientation.VERTICAL:
            self.left += self.speed * self.direction
        else:
            self.top += self.speed * self.direction

    def getDrawingColor(self):
        return self.colorpreset.lineColor.toRGBA()


class Target(CircularGameObject):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 10)

    def getDrawingColor(self):
        return self.colorpreset.fgColor2.toRGBA()

    def randomPosition(self, status: 'GameStatus'):
        self.x = random.randint(0, status.width)
        self.y = random.randint(0, status.height)
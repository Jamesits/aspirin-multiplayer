from pygame.locals import *


class InputGroup:
    pass


class KeyboardInputGroup(InputGroup):
    def __init__(self):
        self.keys = []
        self.eventHandlers = {}

    def registerKeys(self):
        return self.keys, self.eventHandlers


class JoystickInputGroup(InputGroup):
    def __init__(self):
        raise NotImplementedError()


class KeyboardInputGroupASDF(KeyboardInputGroup):
    def __init__(self):
        super().__init__()
        self.keys = [K_a, K_b, K_c, K_d]
        self.eventHandlers = {
            KEYDOWN: self.onKeydown,
            KEYUP: self.onKeyUp,
        }

    def registerKeys(self):
        return self.keys, self.eventHandlers

    def onKeydown(self, event):
        print("Key pressed")

    def onKeyUp(self, event):
        pass


class KeyboardInputGroupUDLR(KeyboardInputGroup):
    def __init__(self):
        super().__init__()
        self.keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
        self.eventHandlers = {
            KEYDOWN: self.onKeydown,
            KEYUP: self.onKeyUp,
        }

    def onKeydown(self, event):
        pass

    def onKeyUp(self, event):
        pass

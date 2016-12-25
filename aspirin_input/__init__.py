from pygame.locals import *
import aspirin_logic

class InputGroup:
    def __init__(self, player: 'aspirin_logic.Player'):
        self.connectedPlayer = player

class KeyboardInputGroup(InputGroup):
    def __init__(self, player: 'aspirin_logic.Player'):
        super().__init__(player)
        self.keys = []
        self.eventHandlers = {}

    def registerKeys(self):
        return self.keys, self.eventHandlers


class JoystickInputGroup(InputGroup):
    def __init__(self, player: 'aspirin_logic.Player'):
        super().__init__(player)
        raise NotImplementedError()


class KeyboardInputGroupWASD(KeyboardInputGroup):
    def __init__(self, player: 'aspirin_logic.Player'):
        super().__init__(player)
        self.keys = [K_a, K_s, K_d, K_w]
        self.eventHandlers = {
            KEYDOWN: self.onKeydown,
            KEYUP: self.onKeyUp,
        }

    def onKeydown(self, event):
        if event.key == K_a:
            self.connectedPlayer.h_movement_level -= 1
        elif event.key == K_d:
            self.connectedPlayer.h_movement_level += 1
        elif event.key == K_s:
            self.connectedPlayer.v_movement_level += 1
        elif event.key == K_w:
            self.connectedPlayer.v_movement_level -= 1
        else:
            raise NotImplementedError()

    def onKeyUp(self, event):
        if event.key == K_a:
            self.connectedPlayer.h_movement_level += 1
        elif event.key == K_d:
            self.connectedPlayer.h_movement_level -= 1
        elif event.key == K_s:
            self.connectedPlayer.v_movement_level -= 1
        elif event.key == K_w:
            self.connectedPlayer.v_movement_level += 1
        else:
            raise NotImplementedError()


class KeyboardInputGroupUDLR(KeyboardInputGroup):
    def __init__(self, player: 'aspirin_logic.Player'):
        super().__init__(player)
        self.keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
        self.eventHandlers = {
            KEYDOWN: self.onKeydown,
            KEYUP: self.onKeyUp,
        }

    def onKeydown(self, event):
        if event.key == K_a:
            self.connectedPlayer.h_movement_level -= 1
        elif event.key == K_d:
            self.connectedPlayer.h_movement_level += 1
        elif event.key == K_s:
            self.connectedPlayer.v_movement_level += 1
        elif event.key == K_w:
            self.connectedPlayer.v_movement_level -= 1
        else:
            raise NotImplementedError()

    def onKeyUp(self, event):
        if event.key == K_a:
            self.connectedPlayer.h_movement_level += 1
        elif event.key == K_d:
            self.connectedPlayer.h_movement_level -= 1
        elif event.key == K_s:
            self.connectedPlayer.v_movement_level -= 1
        elif event.key == K_w:
            self.connectedPlayer.v_movement_level += 1
        else:
            raise NotImplementedError()

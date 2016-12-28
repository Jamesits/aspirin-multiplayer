from pygame.locals import *

import aspirin_logic
import json
import socket
import fcntl, os
import errno

class NetworkComm:
    def __init__(self, address: str="127.0.0.1", port: int=45645):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))
        fcntl.fcntl(self.sock, fcntl.F_SETFL, os.O_NONBLOCK)

    def send(self, data: bytes):
        self.sock.sendto(data, (self.address, self.port))

    def recv(self, bufsize: int=1024):
        try:
            return self.sock.recvfrom(bufsize)
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                return None, None
            else:
                raise


class InputGroup:
    def __init__(self, player: 'aspirin_logic.Player'):
        self.connectedPlayer = player
        self.proxied = False

    @staticmethod
    def eventToJson(event):
        d = event.__dict__
        d["type"] = event.type
        return json.dumps(d)


class KeyboardInputGroup(InputGroup):
    def __init__(self, player: 'aspirin_logic.Player'):
        super().__init__(player)
        self.keys = []
        self.eventHandlers = {}

    def registerKeys(self):
        return self.keys, self.eventHandlers

    def onKeydown(self, event):
        pass

    def onKeyUp(self, event):
        pass


class NetworkProxiedKeyboardInputGroup(KeyboardInputGroup):
    def __init__(self, player: 'aspirin_logic.Player', nc: NetworkComm):
        super().__init__(player)
        self.nc = nc

    def sendEvent(self, event):
        msg = self.eventToJson(event)
        print("Send: ", msg)
        self.nc.send(msg.encode())

    def recvEvent(self):
        data, _ = self.nc.recv()
        print("Recv: ", data)


class JoystickInputGroup(InputGroup):
    def __init__(self, player: 'aspirin_logic.Player'):
        super().__init__(player)
        raise NotImplementedError()


class KeyboardInputGroupWASD(NetworkProxiedKeyboardInputGroup):
    def __init__(self, player: 'aspirin_logic.Player', nc: NetworkComm):
        super().__init__(player, nc)
        self.keys = [K_a, K_s, K_d, K_w]
        self.eventHandlers = {
            KEYDOWN: self.onKeydown,
            KEYUP: self.onKeyUp,
        }

    def onKeydown(self, event, isProxiedEvent: bool=False):
        if not isProxiedEvent:
            self.sendEvent(event)
            return
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

    def onKeyUp(self, event, isProxiedEvent: bool=False):
        if not isProxiedEvent:
            self.sendEvent(event)
            return
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


class KeyboardInputGroupUDLR(NetworkProxiedKeyboardInputGroup):
    def __init__(self, player: 'aspirin_logic.Player', nc: NetworkComm):
        super().__init__(player, nc)
        self.keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
        self.eventHandlers = {
            KEYDOWN: self.onKeydown,
            KEYUP: self.onKeyUp,
        }

    def onKeydown(self, event, isProxiedEvent: bool=False):
        if not isProxiedEvent:
            self.sendEvent(event)
            return
        if event.key == K_LEFT:
            self.connectedPlayer.h_movement_level -= 1
        elif event.key == K_RIGHT:
            self.connectedPlayer.h_movement_level += 1
        elif event.key == K_DOWN:
            self.connectedPlayer.v_movement_level += 1
        elif event.key == K_UP:
            self.connectedPlayer.v_movement_level -= 1
        else:
            raise NotImplementedError()

    def onKeyUp(self, event, isProxiedEvent: bool=False):
        if not isProxiedEvent:
            self.sendEvent(event)
            return
        if event.key == K_LEFT:
            self.connectedPlayer.h_movement_level += 1
        elif event.key == K_RIGHT:
            self.connectedPlayer.h_movement_level -= 1
        elif event.key == K_DOWN:
            self.connectedPlayer.v_movement_level -= 1
        elif event.key == K_UP:
            self.connectedPlayer.v_movement_level += 1
        else:
            raise NotImplementedError()

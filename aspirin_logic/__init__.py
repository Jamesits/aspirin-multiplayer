class GameStatus:
    def __init__(self):
        self.dataBindingCallbacks = []

    def registerDataBindingCallback(self, func: callable):
        self.dataBindingCallbacks.append(func)
import os
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
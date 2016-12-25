class Color:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = red
        self.green = green
        self.blue = blue

    @classmethod
    def fromHEX(cls, hexstr: str = "#000000"):
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
    def __init__(self, bgColor: Color = Color(0, 0, 0), fgColor: Color = Color(0, 0, 255),
                 fgColor2: Color = Color(255, 0, 0), lineColor: Color = Color(0, 0, 255)):
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.fgColor2 = fgColor2
        self.lineColor = lineColor
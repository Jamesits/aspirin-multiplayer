from aspirin_display import ColorPreset, Color

color_presets = {
    "dark": ColorPreset(Color(0, 0, 0), Color(0, 0, 255), Color(255, 0, 0), Color(0, 0, 255)),
    "pink": ColorPreset(Color.fromHEX("#000000"), Color.fromHEX("#FF69B4"), Color.fromHEX("#EE82EE"),
                        Color.fromHEX("#FF00FF")),
    "lime": ColorPreset(Color.fromHEX("#000000"), Color.fromHEX("#32CD32"), Color.fromHEX("#0000FF"),
                        Color.fromHEX("#ADD8E6")),
    "white": ColorPreset(Color.fromHEX("#FFFFFF"), Color.fromHEX("#000000"), Color.fromHEX("#FF0000"),
                         Color.fromHEX("#0000FF")),
    "light": ColorPreset(Color.fromHEX("#800080"), Color.fromHEX("#FF69B4"), Color.fromHEX("#FFFFFF"),
                         Color.fromHEX("#FF00FF")),

}

def RGB2NextionColour(r:int, g:int, b:int) -> int:
    return ((r >> 3) << 11) + ((g >> 2) << 5) + (b >> 3)

def Nextion2RGBColour(color16bit:int):
    r = (color16bit >> 11) << 3
    g = ((color16bit >> 5) & 0x3F) << 2
    b = (color16bit & 0x1F) << 3
    return [r, g, b]
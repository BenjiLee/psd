"""
Miscellaneous functions such as the text renderer.
"""

def print_text(font, x, y, text, screen, color=(0,0,0)):
    """
    This will draw text at desired x,y coordinate on the given surface with
    given color.

    @param font: pygame's font object
    @type font: pygame.font.Font
    @param x: x coordinate of text starting with left most pixel
    @type x: int
    @param y: y coordinate of text starting with top most pixel
    @type y: int
    @param text: The text to be drawn
    @type text: string
    @param screen: The pygame surface we want to draw on
    @type screen: pygame.Surface
    @param color: RGB color for text
    @type color: tuple

    """
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

def merge_dict(d1,d2,merge_fn=lambda x,y:y):
    result = dict(d1)
    for k,v in d2.iteritems():
        if k in result:
            result[k] = merge_fn(result[k], v)
        else:
            result[k] = v
    return result

a = {"a":1}
b = {"a":3}
print merge_dict(a,b,lambda x,y: x+y)
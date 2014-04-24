import sys, pygame, os
from pygame.locals import *

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

#main program begins
pygame.init()

modes = pygame.display.list_modes(16)
screen = pygame.display.set_mode(modes[0], FULLSCREEN, 16)
#screen = pygame.display.set_mode((240,320))
pygame.display.set_caption("Mouse Demo")
font1 = pygame.font.Font(None, 24)
white = 255,255,255
black = 0,0,0
grey = 200,200,200
keyboard = pygame.image.load("keyboard.png").convert()
mouse_x = mouse_y = 0
mouse_down = mouse_up = 0
mouse_down_x = mouse_down_y = 0
mouse_up_x = mouse_up_y = 0

#repeating loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x,mouse_y = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = event.button
            mouse_down_x,mouse_down_y = event.pos
        elif event.type == MOUSEBUTTONUP:
            mouse_up = event.button
            mouse_up_x,mouse_up_y = event.pos

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    screen.fill((grey))
    screen.blit(keyboard, (0,100))

    print_text(font1, 0, 20, "Mouse position: " + str(mouse_x) +
               "," + str(mouse_y))

    print_text(font1, 0, 60, "Mouse button down: " + str(mouse_down) +
               " at " + str(mouse_down_x) + "," + str(mouse_down_y))

    print_text(font1, 0, 80, "Mouse button up: " + str(mouse_up) +
               " at " + str(mouse_up_x) + "," + str(mouse_up_y))


    pygame.display.update()

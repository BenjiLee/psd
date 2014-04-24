import sys, pygame, os
from pygame.locals import *

def print_text(font, x, y, text, color=(0,0,0)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV'      , '/dev/fb1')
# os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
# os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

#main program begins
pygame.init()

modes = pygame.display.list_modes(16)
#screen = pygame.display.set_mode(modes[0], FULLSCREEN, 16)
screen = pygame.display.set_mode((240,320))
font1 = pygame.font.Font(None, 24)
white = 255,255,255
black = 0,0,0
grey = 200,200,200
green = 0,204,0
wpa = {"ssid":"","pass":""}
caps = False
focus = "ssid"
back = "back" #TODO implement delte
space = ""
shift = "shift" #TODO implement caps
keyboard = pygame.image.load("keyboard.png").convert()
alphabet = [['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L',back],
            ['Z','X','C','V','B','N','M',',','.',back],
            ['1','2','3','4','5','6','7','8','9','0'],
            ['!','@','#','$','%','^','&','*','(',')'],
            ['_','+','-','=','{','}',"'",'"','<','>'],
            ['?','`','~','/','\\',shift,shift,' ',' ',' ']]
mouse_down = mouse_up = 0
mouse_down_x = mouse_down_y = 0

def submit(wpa):
    sys.exit()
    pass

def key_touch(x,y):
    global caps
    global focus
    if y >110:
        x = x/24
        y = (y-110)/30
        key = alphabet[y][x]
        if key is "shift":
            if caps is True:
                caps = False
            else:
                caps = True
        elif key is "back":
            wpa[focus] = wpa[focus][:-1]
        else:
            if key.isalpha():
                if caps is False:
                    key = key.lower()
            wpa[focus] = wpa[focus] + key
    elif x >165 :
        submit(wpa);
    elif y < 55:
        focus = "ssid"
    else:
        focus = "pass"

#repeating loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # mouse_down = event.button
            mouse_down_x,mouse_down_y = event.pos
            key_touch(mouse_down_x,mouse_down_y)
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    screen.fill((grey))
    screen.blit(keyboard, (0,106)) #fix keyboard.png to fix 7 rows or 30 pixels

    if caps is True:
        print_text(font1, 80,10, "Capslock")

    print_text(font1, 5,10, "SSID:")
    pygame.draw.rect(screen, white, (5,30,155,20))
    print_text(font1, 10,30, wpa["ssid"])

    print_text(font1, 5,55, "Password:")
    pygame.draw.rect(screen, white, (5,75,155,20))
    print_text(font1, 10,75, wpa["pass"])

    if focus is "ssid":
        pygame.draw.rect(screen, black, (5,30,155,20),2)
    else:
        pygame.draw.rect(screen, black, (5,75,155,20),2)

    pygame.draw.rect(screen, black, (165,15,70,80),2)
    pygame.draw.rect(screen, green, (165,15,70,80))
    print_text(font1, 173,45, "Submit")

    pygame.display.update()

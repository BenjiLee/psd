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

#pygame.mouse.set_visible(False)
font1 = pygame.font.Font(None, 24)
white = 255,255,255
black = 0,0,0
grey = 200,200,200
green = 0,200,0
red = 200,0,0
wpa = {"ssid":"","pass":""}
caps = False
focus = "ssid"
back = "back"
space = ""
shift = "shift"
#keyboard = pygame.image.load("/home/pi/psd/keyboard.png").convert()
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
    fo = open("/etc/network/interfaces", "w")
    new_settings =  "auto lo\niface lo inet loopback\niface eth0 inet dhcp\n"+\
                    "allow-hotplug wlan0\nauto wlan\n"+"iface wlan0 inet dhcp\n"+\
                    '        wpa-ssid "%s"\n        wpa-psk "%s"'\
                    % (wpa["ssid"], wpa["pass"])
    fo.write(new_settings)
    fo.close()
    sys.exit()

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
        if y < 55:
            submit(wpa);
        else:
            sys.exit()
    elif y < 55:
        focus = "ssid"
    else:
        focus = "pass"

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # mouse_down = event.button
            mouse_down_x,mouse_down_y = event.pos
            key_touch(mouse_down_x,mouse_down_y)

    screen.fill((grey))
    screen.blit(keyboard, (0,110)) #fix keyboard.png to fix 7 rows or 30 pixels

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

    pygame.draw.rect(screen, black, (165,5,70,50),2)
    pygame.draw.rect(screen, green, (165,5,70,50))
    print_text(font1, 172,25, "Submit")

    pygame.draw.rect(screen, black, (165,60,70,50),2)
    pygame.draw.rect(screen, red, (165,60,70,50))
    print_text(font1, 186,79, "Exit")

    pygame.display.update()

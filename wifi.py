import sys, pygame,os
from subprocess import Popen, PIPE
from pygame.locals import *



class Things:
    def __init__(self, caps, alphabet, focus, wpa,device):
        self.caps = caps
        self.alphabet = alphabet
        self.focus = focus
        self.wpa = wpa
        self.device = device


def main():
    output = Popen(['hostname'], stdout=PIPE)
    device = output.stdout.read().replace("\n", "")
    alphabet = (('Q','W','E','R','T','Y','U','I','O','P'),
            ('A','S','D','F','G','H','J','K','L',"back"),
            ('Z','X','C','V','B','N','M',',','.',"back"),
            ('1','2','3','4','5','6','7','8','9','0'),
            ('!','@','#','$','%','^','&','*','(',')'),
            ('_','+','-','=','{','}',"'",'"','<','>'),
            ('?','`','~','/','\\',"shift","shift",' ',' ',' '))
    caps = False
    wpa = {"ssid":"","pass":""}
    focus = "ssid"
    thing = Things(caps, alphabet,focus, wpa, device)

    if device == "raspberrypi":
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.putenv('SDL_FBDEV'      , '/dev/fb1')
        os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
        os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

    pygame.init()

    if device == "raspberrypi":
        modes = pygame.display.list_modes(16)
        screen = pygame.display.set_mode(modes[0], FULLSCREEN, 16)
        pygame.mouse.set_visible(False)
    else:
        screen = pygame.display.set_mode((240,320))

    font1 = pygame.font.Font(None, 24)
    colors = {"white":(255,255,255), "black":(0,0,0),"red":(200,0,0),\
                  "green":(0,200,0),"grey":(200,200,200)}

    if device == "raspberrypi":
        keyboard = pygame.image.load("/home/pi/psd/keyboard.png").convert()
    else:
        keyboard = pygame.image.load("keyboard.png").convert()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # mouse_down = event.button
                mouse_down_x,mouse_down_y = event.pos
                key_touch(mouse_down_x,mouse_down_y,thing)

        screen.fill((colors["grey"]))
        screen.blit(keyboard, (0,110)) #fix keyboard.png to fix 7 rows or 30 pixels

        if thing.caps is True:
            print_text(font1, 80,10, "Capslock", screen)

        print_text(font1, 5,10, "SSID:", screen)
        pygame.draw.rect(screen, colors["white"], (5,30,155,20))
        print_text(font1, 10,30, wpa["ssid"], screen)

        print_text(font1, 5,55, "Password:", screen)
        pygame.draw.rect(screen, colors["white"], (5,75,155,20))
        print_text(font1, 10,75, wpa["pass"], screen)

        if thing.focus is "ssid":
            pygame.draw.rect(screen, colors["black"], (5,30,155,20),2)
        else:
            pygame.draw.rect(screen, colors["black"], (5,75,155,20),2)

        pygame.draw.rect(screen, colors["black"], (165,5,70,50),2)
        pygame.draw.rect(screen, colors["green"], (165,5,70,50))
        print_text(font1, 172,25, "Submit", screen)

        pygame.draw.rect(screen, colors["black"], (165,60,70,50),2)
        pygame.draw.rect(screen, colors["red"], (165,60,70,50))
        print_text(font1, 186,79,"Exit", screen)

        pygame.display.update()

def print_text(font, x, y, text, screen, color=(0,0,0)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

def submit(wpa,device):
    new_settings =  "auto lo\n\n"+\
                        "iface lo inet loopback\n"+\
                        "iface eth0 inet dhcp\n\n"+\
                        "allow-hotplug wlan0\n"+\
                        "auto wlan0\n"+\
                        "iface wlan0 inet dhcp\n"+\
                        '        wpa-ssid "%s"\n        wpa-psk "%s"'\
                        % (wpa["ssid"], wpa["pass"])
    if device == "raspberrypi":
        fo = open("/etc/network/interfaces", "w")
        fo.write(new_settings)
        fo.close()
    else:
        print new_settings
    sys.exit()

def key_touch(x,y, thing):
    if y >110:
        x = x/24
        y = (y-110)/30
        key = thing.alphabet[y][x]
        if key is "shift":
            if thing.caps is True:
                thing.caps = False
            else:
                thing.caps = True
        elif key is "back":
            thing.wpa[thing.focus] = thing.wpa[thing.focus][:-1]
        else:
            if key.isalpha():
                if thing.caps is False:
                    key = key.lower()
            thing.wpa[thing.focus] = thing.wpa[thing.focus] + key
    elif x >165 :
        if y < 55:
            submit(thing.wpa,thing.device);
        else:
            sys.exit()
    elif y < 55:
        thing.focus = "ssid"
    else:
        thing.focus = "pass"

if __name__ == "__main__":
    main()

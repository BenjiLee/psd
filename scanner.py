import sys, pygame,os
import time
from subprocess import Popen, PIPE
from pygame.locals import *

class Info:
    def __init__(self):
        output = Popen(['hostname'], stdout=PIPE)
        self.device = output.stdout.read().replace("\n", "") #Set device
        if self.device == "raspberrypi":
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')
            os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
            os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
        pygame.init()

        if self.device == "raspberrypi":
            modes = pygame.display.list_modes(16)
            self.screen = pygame.display.set_mode(modes[0], FULLSCREEN, 16)
            pygame.mouse.set_visible(False)
        else:
            self.screen = pygame.display.set_mode((240,320))

        self.select = None
        self.page = 0
        self.state = "menu"
        self.font1 = pygame.font.Font(None, 24)
        self.colors = {"white":(255,255,255), "black":(0,0,0),"red":(200,0,0),\
              "green":(0,200,0),"dgrey":(200,200,200), "lgrey":(225,225,225)}
def main():

    info = Info()

    get_files(info)

    if info.device == "raspberrypi":
        keyboard = pygame.image.load("/home/pi/psd/keyboard.png").convert()
    else:
        keyboard = pygame.image.load("keyboard.png").convert()




    while True:
        if info.state == "menu":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    menu_keyboard(mouse_down_x,mouse_down_y,info)
            menu(info)


        elif info.state == "new_file":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    new_file_keyboard(mouse_down_x,mouse_down_y,info)
            new_file(info,keyboard)


        pygame.display.update()

def new_file(info, keyboard):
    info.screen.fill((info.colors["dgrey"]))
    info.screen.blit(keyboard, (0,110))

    print_text(info.font1, 5,10, "SSID:", info.screen)
    pygame.draw.rect(info.screen, info.colors["white"], (5,30,155,20))
    print_text(info.font1, 10,30,"ssid", info.screen)

    print_text(info.font1, 5,55, "Password:", info.screen)
    pygame.draw.rect(info.screen, info.colors["white"], (5,75,155,20))
    print_text(info.font1, 10,75, "pass", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (165,5,70,50),2)
    pygame.draw.rect(info.screen, info.colors["green"], (165,5,70,50))
    print_text(info.font1, 172,25, "Submit", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (165,60,70,50),2)
    pygame.draw.rect(info.screen, info.colors["red"], (165,60,70,50))
    print_text(info.font1, 186,79,"Exit", info.screen)

def menu(info):
    info.screen.fill((info.colors["white"]))

    pygame.draw.rect(info.screen, (150,150,150), (0,240,240,60))
    pygame.draw.rect(info.screen, info.colors["dgrey"], (0,0,60,320))


    pygame.draw.rect(info.screen, (50,50,50), (0,300,240,20))
    print_text(info.font1, 5, 303, \
               time.strftime("%Y-%m-%d                     %X"), \
               info.screen, color=info.colors["white"])

    column = 5

    for i in range(0,6):
        i += info.page*6
        if i >= len(info.files):
            break
        date, name= info.files[i].split("/")
        print_text(info.font1, 65, column, name, info.screen)
        print_text(info.font1, 75, (column+20), date, info.screen)
        column += 40

    #Left Menu
    pygame.draw.rect(info.screen, info.colors["black"], (3,3,54,72),2)
    pygame.draw.rect(info.screen, info.colors["green"], (4,4,52,70))
    print_text(info.font1, 13, 32,  "New", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (3,77,54,72),2)
    pygame.draw.rect(info.screen, info.colors["lgrey"], (4,78,52,70))
    print_text(info.font1, 16, 95,  "Re-", info.screen)
    print_text(info.font1, 8, 115,  "Name", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (3,151,54,72),2)
    pygame.draw.rect(info.screen, info.colors["red"], (4,152,52,70))
    print_text(info.font1, 16, 178,  "Del", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (3,225,54,72),2)
    pygame.draw.rect(info.screen, info.colors["red"], (4,226,52,70))
    print_text(info.font1, 14, 254,  "Exit" , info.screen)



    #Navigation bar
    pygame.draw.rect(info.screen, info.colors["black"], (63,243,56,54),2)
    pygame.draw.rect(info.screen, info.colors["lgrey"], (64,244,54,52))
    print_text(info.font1, 72, 262, "Back", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (122,243,56,54),2)
    pygame.draw.rect(info.screen, info.colors["lgrey"], (123,244,54,52))
    print_text(info.font1, 125, 262, "Select", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (181,243,56,54),2)
    pygame.draw.rect(info.screen, info.colors["lgrey"], (182,244,54, 52))
    print_text(info.font1, 191, 262, "Next", info.screen)

    if info.select is not None:
        y = 40*info.select - info.page*6*40
        pygame.draw.rect(info.screen, info.colors["black"],(60,y,180,40),1)



def print_text(font, x, y, text, screen, color=(0,0,0)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

def close_file():
    sys.exit()

def menu_keyboard(x,y,info):
    if x < 58 and y < 300: #left menu
        y = y/75
        if y == 0:
            info.state = "new_file"
        elif y == 1:
            pass #rename
        elif y == 2:
            pass #delete
        elif y == 3:
            sys.exit()
    elif x > 62 and y > 240: # bottom navigation
        x = x/60
        if x == 1:
            if info.page > 0:
                info.page -= 1 #previous page
                info.select = None
        if x == 2:
            pass #select files
        elif x == 3:
            if info.page < len(info.files)/6:
                info.page = info.page + 1 #next page
                info.select = None
    elif x > 62 and y < 240: #file view
        file_index = y/40 + info.page*6
        try:
            info.files[file_index]
            info.select = file_index
        except:
            print "no file in selected space"

def new_file_keyboard(x,y,info):
    info.state = "menu"

def get_files(info):
    if info.device == "raspberrypi":
        output = Popen(['ls','/home/pi/files'], stdout=PIPE)
        info.files = output.stdout.read().replace("\n"," ").split()
    else:
        #output = Popen(['ls','/home/spoon/files'], stdout=PIPE)
        info.files = ["2014-3-21 8:22/a","2014-3-21 8:25/b","2014-3-22 8:27/c",\
                      "2014-3-23 9:32/d","2014-3-24 10:12/e","2014-3-25 6:22/f",\
                      "2014-3-23 9:32/g","2014-3-24 10:12/h","2014-3-25 6:22/i"]


if __name__ == "__main__":
    main()
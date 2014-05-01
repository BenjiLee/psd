import sys, pygame, os, time
from subprocess import Popen, PIPE
from pygame.locals import *

import helpers.file_controls as f
from helpers.settings import print_text

class Info:
    def __init__(self):
        output = Popen(['hostname'], stdout=PIPE)
        self.device = output.stdout.read().replace("\n", "") #Set device
        
        if self.device == "raspberrypi":
            self.pi = True
        else:
            self.pi = False
            
        if self.pi:
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')
            os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
            os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
            
        pygame.init()

        if self.pi:
            modes = pygame.display.list_modes(16)
            self.screen = pygame.display.set_mode(modes[0], FULLSCREEN, 16)
            pygame.mouse.set_visible(False)
        else:
            self.screen = pygame.display.set_mode((240,320))

        output = Popen("echo $USER", stdout=PIPE, shell=True)
        self.user = output.stdout.read().replace("\n","") #Get user name for folders
        self.folder = "/home/"+self.user+"/files/"

        self.select = None
        self.page = 0
        self.state = "menu"
        self.rename = None
        self.font1 = pygame.font.Font(None, 24)
        self.colors = {"white":(255,255,255), "black":(0,0,0),"red":(200,0,0),\
              "green":(0,200,0),"dgrey":(200,200,200), "lgrey":(225,225,225)}

class Keyboard():
    def __init__(self, info):
        self.alphabet = (('Q','W','E','R','T','Y','U','I','O','P'),
            ('A','S','D','F','G','H','J','K','L',"back"),
            ('Z','X','C','V','B','N','M',',','.',"back"),
            ('1','2','3','4','5','6','7','8','9','0'),
            ('!','@','#','$','%','^','&','*','(',')'),
            ('_','+','-','=','{','}',"'",'"','<','>'),
            ('?','`','~','','\\',"shift","shift",' ',' ',' '))
        self.caps = False
        if info.pi:
            self.image = pygame.image.load("/home/pi/psd/keyboard.png").convert()
        else:
            self.image = pygame.image.load("keyboard.png").convert()
        self.filename = ""

def main():
    """
    This is the main loop which creates the info object that is passed around.
    It the retrieves the files and images we will be using. Depending on
    info.state (default "menu"), the while loop will be displaying different
    views with different inputs.
    """

    info = Info()

    f.get_files(info)

    keyboard = Keyboard(info)


    while True:
        if info.state == "menu":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    menu_touch_input(mouse_down_x,mouse_down_y,info, keyboard)
            menu_view(info)


        elif info.state == "file_name_view":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    new_file_touch_input(mouse_down_x, mouse_down_y, \
                                         keyboard, info)
            file_name_view(info,keyboard)


        pygame.display.update()

def menu_view(info):
    """
    The view for the menu. User is able to create, delete, and rename a file, or
    exit on the left panel. On the bottom panel, user is able to flip pages, or
    select the currently selected file in the top right panel.

    Menu View:
    -----------
    |  | file |
    |l | file |
    |e | etc. |
    |f |      |
    |t |      |
    |  |-------
    |  | bot  |
    -----------

    @param info: object with our configurations and states
    @type info: Info
    """
    info.screen.fill((info.colors["white"]))

    pygame.draw.rect(info.screen, (150,150,150), (0,240,240,60))
    pygame.draw.rect(info.screen, info.colors["dgrey"], (0,0,60,320))


    #Bottom bar for time and date
    pygame.draw.rect(info.screen, (50,50,50), (0,300,240,20))
    print_text(info.font1, 5, 303, \
               time.strftime("%Y-%m-%d                     %X"), \
               info.screen, color=info.colors["white"])

    column = 0
    if info.files is not None:
        for i in range(0,6):
            i += info.page*6
            if i >= len(info.files):
                break
            date, name = info.files[i].split("=")
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

def file_name_view(info, keyboard):
    '''
    The view for a new file. User is able to name and create new file or go to
    menu.

    @param info: object with our configurations and states
    @type info: Info
    @param keyboard: keyboard image
    @type keyboard: pygame.Surface
    '''
    info.screen.fill((info.colors["dgrey"]))
    info.screen.blit(keyboard.image, (0,110))

    print_text(info.font1, 5,10, "New file name:", info.screen)
    pygame.draw.rect(info.screen, info.colors["white"], (5,30,155,20))
    print_text(info.font1, 10,30,keyboard.filename, info.screen)

    print_text(info.font1, 5,55, "Date:", info.screen)
    print_text(info.font1, 10,75, time.strftime("%Y-%m-%d %I:%M%p"), info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (165,5,70,50),2)
    pygame.draw.rect(info.screen, info.colors["green"], (165,5,70,50))
    if info.rename is not None:
        print_text(info.font1, 170,25, "Rename", info.screen)
    else:
        print_text(info.font1, 172,25, "Create", info.screen)
    pygame.draw.rect(info.screen, info.colors["black"], (165,60,70,50),2)
    pygame.draw.rect(info.screen, info.colors["red"], (165,60,70,50))
    print_text(info.font1, 172,79,"Cancel", info.screen)



def close_file():
    sys.exit()

def menu_touch_input(x,y,info,keyboard):
    """
    Takes the touchscreen's input and runs the appropriate action depending on
    the location of the pixels input.

    @param x: x coordinate in pixels
    @type x: int
    @param y: y coordinate in pixels
    @type y: int
    @param info: object with our configurations and states
    @type info: Info

    """
    if x < 58 and y < 300:                     # left menu
        y = y/75
        if y == 0:                                 # new file
            info.state = "file_name_view"
        elif y == 1:
            if info.select is not None:            # rename
                info.rename = info.files[info.select]
                keyboard.filename = info.files[info.select].split("=")[1]
                info.state = "file_name_view"
        elif y == 2:                               # delete
            f.delete_file(info)
        elif y == 3:                               # exit
            sys.exit()
    elif x > 62 and y > 240:                   # bottom navigation
        x = x/60
        if x == 1:                                 # previous page
            if info.page > 0:
                info.page -= 1
                info.select = None
        if x == 2:                                 # select files
            pass
        elif x == 3:                               # next page
            if info.page < len(info.files)/7:
                info.page = info.page + 1
                info.select = None
    elif x > 62 and y < 240:                   #file highlight
        file_index = y/40 + info.page*6
        try:
            info.files[file_index]
            info.select = file_index
        except:
            print "no file in selected space"

def new_file_touch_input(x,y,keyboard,info):
    """
    Takes the touchscreen's input and runs the appropriate action depending on
    the location of the pixels input.

    @param x: x coordinate in pixels
    @type x: int
    @param y: y coordinate in pixels
    @type y: int
    @param info: object with our configurations and states
    @type info: Info

    """
    if y >110:
        x = x/24
        y = (y-110)/30
        key = keyboard.alphabet[y][x]
        if key is "shift":
            if keyboard.caps is True:
                keyboard.caps = False
            else:
                keyboard.caps = True
        elif key is "back":
            keyboard.filename = keyboard.filename[:-1]
        else:
            if key.isalpha():
                if keyboard.caps is False:
                    key = key.lower()
            keyboard.filename = keyboard.filename + key
    elif x >165 :
        if y < 55:
            if info.rename:
                f.rename_file(keyboard.filename,info)
            else:
                f.create_file(keyboard.filename,info)
            keyboard.filename = ""
            info.state = "menu"
            info.rename = None
        else:
            keyboard.filename = ""
            info.state = "menu"
            info.rename = None




if __name__ == "__main__":
    main()
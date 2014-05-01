import sys, pygame, os, time
from subprocess import Popen, PIPE
from pygame.locals import *

import helpers.views as view
import helpers.file_controls as f
import helpers.touchscreen_inputs as touch

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
                    touch.menu_touchscreen_input(mouse_down_x,mouse_down_y,info, keyboard)
            view.menu_view(info)


        elif info.state == "file_name_view":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    touch.new_file_touchscreen_input(mouse_down_x, mouse_down_y, \
                                         keyboard, info)
            view.file_name_view(info,keyboard)


        pygame.display.update()






if __name__ == "__main__":
    main()
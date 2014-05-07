import os
from subprocess import PIPE, Popen
from collections import defaultdict


import pygame
from pygame.locals import FULLSCREEN

class Info:
    """
    Only one of these objects will be instantiated and passed around.
    This object contains all the persistent information such as the device name,
    user name, state for the views, colors used etc.
    It also initializes pygame to the device/screen accordingly.
    """
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
        self.user = output.stdout.read().replace("\n","") #user name for folders
        self.folder = "/home/"+self.user+"/files/"

        self.selected = None
        self.upc_list= []
        self.page = 0
        self.view = "menu_view"
        self.barcode = ""
        # self.view = "selection_view"
        self.filename = None
        self.font1 = pygame.font.Font(None, 24)
        self.colors = {"white":(255,255,255), "black":(0,0,0),"red":(200,0,0),
              "green":(0,200,0),"dgrey":(200,200,200), "lgrey":(225,225,225),
              "pink":(240,120,120)}
        self.upc_qty = defaultdict(int)

class Keyboard():
    """
    If a view needs a keyboard, this object will be passed in. "=" has been
    disabled since we split the filename with it. "/" has been disabled because
    it is an invalid filename character.
    """
    def __init__(self, info):
        self.alphabet = (('Q','W','E','R','T','Y','U','I','O','P'),
            ('A','S','D','F','G','H','J','K','L',"back"),
            ('Z','X','C','V','B','N','M',',','',"back"),
            ('1','2','3','4','5','6','7','8','9','0'),
            ('!','@','#','$','%','^','&','*','(',')'),
            ('_','+','-','','{','}',"'",'"','<','>'),
            ('?','`','~','','\\',"shift","shift",' ',' ',' '))
        self.caps = False
        if info.pi:
            self.image = pygame.image.load("/home/pi/psd/keyboard.png").convert()
        else:
            self.image = pygame.image.load("keyboard.png").convert()
        self.filename = ""
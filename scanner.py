import sys, pygame,os
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

def main():

    info = Info()

    get_files(info)

    font1 = pygame.font.Font(None, 24)
    colors = {"white":(255,255,255), "black":(0,0,0),"red":(200,0,0),\
              "green":(0,200,0),"dgrey":(200,200,200), "lgrey":(250,250,250)}


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print colors
                mouse_down_x,mouse_down_y = event.pos
                key_touch(mouse_down_x,mouse_down_y)

        info.screen.fill((colors["lgrey"]))
        pygame.draw.rect(info.screen, colors["dgrey"], (0,0,70,320))

        column = 5
        for i in range(0,len(info.files)):
            print_text(font1, 75, column, info.files[i], info.screen)
            column += 20


        pygame.display.update()


def print_text(font, x, y, text, screen, color=(0,0,0)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

def close_file():
    sys.exit()

def key_touch(x,y):
    pass

def get_files(info):
    if info.device == "raspberrypi":
        output = Popen(['ls','/home/pi/files'], stdout=PIPE)
    else:
        output = Popen(['ls','/home/spoon/files'], stdout=PIPE)
    info.files = output.stdout.read().replace("\n"," ").split()

if __name__ == "__main__":
    main()
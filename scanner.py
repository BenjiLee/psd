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

    font1 = pygame.font.Font(None, 24)
    colors = {"white":(255,255,255), "black":(0,0,0),"red":(200,0,0),\
              "green":(0,200,0),"grey":(200,200,200)}

    mouse_down_x = mouse_down_y = 0

    #get_files(device)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print colors
                mouse_down_x,mouse_down_y = event.pos
                key_touch(mouse_down_x,mouse_down_y)

        info.screen.fill((colors["grey"]))


        pygame.draw.rect(info.screen, colors["black"], (165,5,70,50),2)
        pygame.draw.rect(info.screen, colors["green"], (165,5,70,50))
        print_text(font1, 172,25, "Submit",info.screen)

        pygame.draw.rect(info.screen, colors["black"], (165,60,70,50),2)
        pygame.draw.rect(info.screen, colors["red"], (165,60,70,50))
        print_text(font1, 186,79,"Exit",info.screen)

        pygame.display.update()


def print_text(font, x, y, text, screen, color=(0,0,0)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

def close_file():
    sys.exit()

def key_touch(x,y):
    pass

def get_files(device):
    if device == "raspberrypi":
        output = Popen(['ls','/home/pi/files'], stdout=PIPE)
    else:
        output = Popen(['ls','/home/pi/files'], stdout=PIPE)
    device = output.stdout.read().replace("\n", "")

if __name__ == "__main__":
    main()
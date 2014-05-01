import sys, pygame, os, time
from subprocess import Popen, PIPE
from pygame.locals import *

import helpers.views as view
import helpers.file_controls as f
import helpers.touchscreen_inputs as touch
import helpers.classes as classes


def main():
    """
    This is the main loop which creates the info object that is passed around.
    It the retrieves the files and images we will be using. Depending on
    info.state (default "menu"), the while loop will be displaying different
    views with different inputs.
    """

    info = classes.Info()

    f.get_files(info)

    keyboard = classes.Keyboard(info)


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
import sys, pygame
from pygame.locals import *

import helpers.views as view
import helpers.file_controls as f
import helpers.key_mouse_inputs as kvm
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
        if info.view == "menu_view":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    kvm.menu_view_input(mouse_down_x,mouse_down_y,
                                                 info, keyboard)
            view.menu_view(info)

        elif info.view == "filename_view":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    kvm.new_file_view_input(mouse_down_x, mouse_down_y,
                                                     keyboard, info)
            view.file_name_view(info,keyboard)

        elif info.view == "selection_view":
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_down_x,mouse_down_y = event.pos
                    kvm.selection_view_touch_input(mouse_down_x, mouse_down_y,
                                                     info)
                elif event.type == KEYDOWN:
                    if event.key == 13:
                        kvm.selection_view_key_input(info, "end")
                    else:
                        try:
                            char = chr(event.key)
                        except ValueError:
                            char = ""
                        kvm.selection_view_key_input(info, char)


            view.selection_view(info)


        pygame.display.update()

if __name__ == "__main__":
    main()
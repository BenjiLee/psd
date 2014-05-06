"""
This file contains the views that are selected by "state" in scanner.py.
"""

import time

import pygame
from settings import print_text


def selection_view(info):
    """
    The view for the selected file. By scanning a barcode, an entry will be
    appended. A selected entry can be deleted.

    @param info: object with our configurations and states
    @type info: Info
    """
    info.screen.fill((info.colors["white"]))
    pygame.draw.line(info.screen, info.colors["black"], (120,0), (120,320), )
    pygame.draw.rect(info.screen, (150,150,150), (0,240,240,60))

    #Bottom bar for time and date
    pygame.draw.rect(info.screen, (50,50,50), (0,300,240,20))
    print_text(info.font1, 5, 303, \
               time.strftime("%Y-%m-%d                     %X"), \
               info.screen, color=info.colors["white"])

    #TODO change to display lines in text file
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


    #Navigation bar
    pygame.draw.rect(info.screen, info.colors["black"], (3,243,56,54),2)
    pygame.draw.rect(info.screen, info.colors["red"], (4,244,54,52))
    print_text(info.font1, 10, 262, "Close", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (63,243,56,54),2)
    pygame.draw.rect(info.screen, info.colors["lgrey"], (64,244,54,52))
    print_text(info.font1, 72, 262, "Back", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (122,243,56,54),2)
    pygame.draw.rect(info.screen, info.colors["pink"], (123,244,54,52))
    print_text(info.font1, 125, 262, "Delete", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (181,243,56,54),2)
    pygame.draw.rect(info.screen, info.colors["lgrey"], (182,244,54, 52))
    print_text(info.font1, 191, 262, "Next", info.screen)

    #TODO fix this for selecting a different grid
    if info.selected is not None:
        y = 40*info.selected - info.page*6*40
        pygame.draw.rect(info.screen, info.colors["black"],(60,y,180,40),1)

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
    print_text(info.font1, 11, 95,  "Com-", info.screen)
    print_text(info.font1, 13, 115,  "bine", info.screen)

    pygame.draw.rect(info.screen, info.colors["black"], (3,151,54,72),2)
    pygame.draw.rect(info.screen, info.colors["pink"], (4,152,52,70))
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

    if info.selected is not None:
        y = 40*info.selected - info.page*6*40
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
    if info.filename is not None:
        print_text(info.font1, 170,25, "Rename", info.screen)
    else:
        print_text(info.font1, 172,25, "Create", info.screen)
    pygame.draw.rect(info.screen, info.colors["black"], (165,60,70,50),2)
    pygame.draw.rect(info.screen, info.colors["red"], (165,60,70,50))
    print_text(info.font1, 172,79,"Cancel", info.screen)
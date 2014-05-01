
"""
The file_controls file contains all the functions that deal with manipulating them.

"""

import os,time
from subprocess import PIPE, Popen

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from helpers.settings import print_text

def rename_file(filename,info):
    """
    Takes the new name and renames the file.

    @param filename: new name of the file
    @type filename: string
    @param info: object with our configurations and states
    @type info: Info
    """
    filename = info.rename.split("=")[0]+"="+filename
    current = info.folder+info.rename
    new = info.folder+filename
    os.rename(current, new)
    get_files(info)

def delete_file(info):
    """
    Will prompt you to delete a file that had been highlighted. If "delete" is
    selected, the file is deleted. This function draws a prompt window on top.

    @param info: object with our configurations and states
    @type info: Info
    """

    delete = False
    break_loop = False
    while info.select is not None and not break_loop:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x,y = event.pos
                if x > 40 and x < 200 and y > 145 and y < 185:
                    if x < 110:
                        delete = False
                        break_loop = True
                    elif x > 130:
                        delete = True
                        break_loop = True

        pygame.draw.rect(info.screen, info.colors["dgrey"], (25,100,190,100))
        pygame.draw.rect(info.screen, info.colors["black"], (24,99,191,101),2)
        print_text(info.font1, 90,120, "Delete?", info.screen)

        pygame.draw.rect(info.screen, info.colors["black"], (39,144,72,42),2)
        pygame.draw.rect(info.screen, info.colors["lgrey"], (40,145,70,40))
        print_text(info.font1, 47,155, "Cancel", info.screen)

        pygame.draw.rect(info.screen, info.colors["black"], (129,144,72,42),2)
        pygame.draw.rect(info.screen, info.colors["lgrey"], (130,145,70,40))
        print_text(info.font1, 140,155, "Delete", info.screen)

        pygame.display.update()
    if delete:
        os.remove(info.folder+info.files[info.select])
        get_files(info)
        info.select = None

def create_file(filename,info):
    date_filename = time.strftime("%Y-%m-%d %I:%M%p") +"="+filename

    fo = open(info.folder+date_filename, "a")


    fo.close()
    get_files(info)

def get_files(info):
    """
    Gets the files from a folder and puts them into the info object as a list.
    Files are named with the date and title separated by a "/"

    @param info: object with our configurations and states
    @type info: Info

    """
    output = Popen(['ls',info.folder], stdout=PIPE)

    if info.pi:
        info.files = output.stdout.read().replace("\n"," ").split()
    else:
        info.files = output.stdout.read().split("\n")
        info.files = info.files[:-1]
        """
        When working in windows
        info.files = ["2014-3-21 8:22=a","2014-3-21 8:25=b","2014-3-22 8:27=c",\
                     "2014-3-23 9:32=d","2014-3-24 10:12=e","2014-3-25 6:22=f",\
                     "2014-3-23 9:32=g","2014-3-24 10:12=h","2014-3-25 6:22=i"]
        """

"""
The file_controls file contains all the functions that deal with manipulating
them.

"""

import os,time, sys, csv
from subprocess import PIPE, Popen
from collections import defaultdict

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from helpers.settings import print_text, merge_dict


def write_to_file(info):
    start = time.clock()
    with open(info.folder+info.filename, 'wb') as f:
        writer = csv.writer(f)
        for upc, qty in info.upc_qty.items():
            writer.writerow([upc,str(qty)])

    get_files(info)
    print (time.clock() - start)*1000


def open_file(info):
    """
    Opens selected csv file, which will then be saved to a dictionary.

    @param info: object with our configurations and states
    @type info: Info
    """
    info.upc_qty = defaultdict(int)

    reader = csv.reader(open(info.folder+info.filename), delimiter=',')
    for row in reader:
        info.upc_qty[row[0]]=int(row[1])
    print "Initial"
    print info.upc_qty.items()

def combine_files(info):
    """
    Combines all available files into one.

    @param info: object with our configurations and states
    @type info: Info
    """
    path, dir, files = os.walk(info.folder).next()


    while len(files) > 1:
        head_dict = defaultdict(int)
        sub_dict = defaultdict(int)
        combined = defaultdict(int)
        head_reader = csv.reader(open(path+files[0]), delimiter=',')
        sub_reader = csv.reader(open(path+files[1]), delimiter=',')
        for row in head_reader:
            head_dict[row[0]] = int(row[1])
        for row in sub_reader:
            sub_dict[row[0]] = int(row[1])

        combined = merge_dict(head_dict,sub_dict, lambda x, y: x+y)
        os.remove(path+files[0])
        os.remove(path+files[1])

        with open(info.folder+time.strftime("%Y-%m-%d %I:%M%p") +
                  "=combined_file", 'w') as f:
            writer = csv.writer(f)
            for upc, qty in combined.items():
                writer.writerow([upc, str(qty)])
        f.close()
        path, dir, files = os.walk(info.folder).next()
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
    while info.selected is not None and not break_loop:
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
        os.remove(info.folder+info.files[info.selected])
        get_files(info)
        info.selected = None

def create_file(filename,info):
    """
    This function creates the file by combining the date/time and name
    separated by a "=".

    @param info: object with our configurations and states
    @type info: Info
    @param filename: name of the new file
    @type filename: string

    """
    date_filename = time.strftime("%Y-%m-%d %I:%M%p") +"="+filename
    fo = open(info.folder+date_filename, "a")

    #TODO When select file is implemented, decide if we go to select or menu.
    fo.close()
    info.filename = date_filename
    open_file(info)
    info.reset_view("selection_view")

def get_files(info):
    """
    Gets the files from a folder and puts them into the info object as a list.
    Files are named with the date and title separated by a "/"

    @param info: object with our configurations and states
    @type info: Info

    """

    output = Popen(['ls',info.folder], stdout=PIPE)

    info.files = output.stdout.read().split("\n")
    info.files = info.files[:-1]
    """
    When working in windows
    info.files = ["2014-3-21 8:22=a","2014-3-21 8:25=b","2014-3-22 8:27=c",\
                 "2014-3-23 9:32=d","2014-3-24 10:12=e","2014-3-25 6:22=f",\
                 "2014-3-23 9:32=g","2014-3-24 10:12=h","2014-3-25 6:22=i"]
    """
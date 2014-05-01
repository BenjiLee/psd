"""
This file contains all the functions that control the touchscreen inputs for the given pixel location and view.
"""
import sys

import helpers.file_controls as f


def menu_touchscreen_input(x,y,info,keyboard):
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

def new_file_touchscreen_input(x,y,keyboard,info):
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

"""
This file contains all the functions that control the touchscreen inputs for the given pixel location and view.
"""
import sys
from collections import defaultdict

import helpers.file_controls as f

def selection_view_touch_input(x,y,info):
    """
    Takes in touchscreen inputs for the file editing view.
    """
    x = x/80
    y = y/60
    if y > 3 and y < 5:
        if x == 0:                                      #exit
            info.reset_view("menu_view")
        elif x == 1:                                    #save
            f.write_to_file(info)
            info.reset_view("menu_view")
        elif x == 2:                                    #delete
            if info.last_upc_qty["qty"] != 0:
                info.upc_qty[info.last_upc_qty["upc"]] -= 1
                info.last_upc_qty = {"upc": info.last_upc_qty["upc"],
                                     "qty": info.upc_qty[info.last_upc_qty["upc"]]}



def selection_view_key_input(info, char):
    """
    Takes in the barcode scanner character and concatenates it until the "end"
    string is input.
    """
    if char != "end":
        info.barcode = info.barcode + char
    else:
        info.upc_qty[info.barcode] += 1
        info.last_upc_qty = {"upc":info.barcode,"qty":info.upc_qty[info.barcode]}
        info.barcode = ""


def menu_view_input(x,y,info,keyboard):
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
            info.reset_view("filename_view")
        elif y == 1:
            f.combine_files(info)           # combine
        elif y == 2:                               # delete
            f.delete_file(info)
        elif y == 3:                               # exit
            sys.exit()
    elif x > 62 and y > 240:                   # bottom navigation
        x = x/60
        if x == 1:                                 # previous page
            if info.page > 0:
                info.page -= 1
                info.selected = None
        if x == 2:                                 # select files
            if info.selected is not None:
                info.filename = info.files[info.selected]
                print "filename"+info.filename
                f.open_file(info)
                info.reset_view("selection_view")
        elif x == 3:                               # next page
            if info.page < len(info.files)/7:
                info.page = info.page + 1
                info.selected = None
    elif x > 62 and y < 240:                   #file highlight
        file_index = y/40 + info.page*6
        try:
            info.files[file_index]
            info.selected = file_index
        except:
            print "no file in selected space"

def new_file_view_input(x,y,keyboard,info):
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
    elif x >165:
        if y < 55:
            f.create_file(keyboard.filename, info)
            info.selected
            info.reset_view("selection_view")
            keyboard.filename = ""
        else:
            keyboard.filename = ""
            info.reset_view("menu_view")

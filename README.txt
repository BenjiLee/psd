Personal Scanning Device
=============

Personal Scanning Device

Christopher Lee
4/21/2014
christopherlee2012@gmail.com

Goals:

    This project's goal is to create a personal scanning device that will record
a stores barcodes into a text file. This text file needs to be easily accessible
for most users. This file will then be put into a retail software to update a
store's database with it's physical inventory. The file will be transfers by
making the raspberry pi a server, and having the client computer access it it
via local ip.



Learning goals:
    All this can be done bu simply hooking up a barcode scanner to a pi, loading
upa text file and then manually transferring it over. The main idea of this is
to reduce the amount of manual steps need to complete this process. Originally
I had planned to mount and umount a USB drive, but that was too easy/accessing
the information via server would better because there would be less physical
interaction with the product.

-Make the raspberry pi into a fileserver I can access from a browser in the
local network
-Create an interface to input the wifi name/pass.
-Assign the GPIO buttons to commands
-Attach a touchscreen (PiTFT by adafruit)
-Create an interface for writing barcode data to file


Notes:
GUI's will be made using pygame. Images will be created via photoshop.

GPIO configuration was written in C rather than python since it was originally
meant for C.


To compile gpio.c:
"gcc -o gpio gpio.c -I/usr/local/include -L/usr/local/lib -lwiringPi"
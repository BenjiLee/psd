Personal Scanning Device
=============

Personal Scanning Device

Christopher Lee
4/21/2014
christopherlee2012@gmail.com

Goals:

    This project's goal is to create a personal scanning device that will record
a store's barcodes into a text file. This text file needs to be easily accessible
for most users. This file will then be put into a retail software to update a
store's database with its physical inventory. The file will be transferred by
making the raspberry pi a server, and having the client computer access it
via a local ip.


Learning goals:

    All this can be done by simply hooking up a barcode scanner to a pi, loading
up a text file and then manually transferring it over. The main idea of this is
to reduce the number of manual steps needed to complete this process. Originally
I had planned to simply mount and umount a USB drive, but transferring the
information via server would minimize the physical interaction with the product
and optimize the user experience.

-Make the raspberry pi into a fileserver I can access from a browser in the
local network
-Create an interface to input the wifi name/pass
-Assign the GPIO buttons to commands
-Attach a touchscreen (PiTFT by adafruit)
-Create an interface for writing barcode data to file


Notes:
Screen is rotated to portrait.

GUI's will be made using pygame. Images will be created via photoshop.

GPIO configuration was written in C rather than python since it was originally
meant for C.

GPIO buttons from #23, #22, #21, #18

Shutdown, scanner gui, wifi setup gui, server gui


To compile gpio.c:
gcc -o gpio gpio.c -I/usr/local/include -L/usr/local/lib -lwiringPi

To start gpio daemon:
add "sudo ./home/pi/psd/gpio &" the line before "exit 0"

To configure samba:

    sudo apt-get install samba

    sudo nano /etc/samba/smb.conf

change

    workgroup = your_workgroup_name
    wins support = yes

add to end
    [barcodes]
       path=/home/pi/barcodes
       browseable=Yes
       writeable=Yes
       only guest=no
       create mask=0777
       directory mask=0777
       public=Yes

To access, find your workgroups name in your local network.

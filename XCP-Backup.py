# Created by austin3410
# Based off of a bash script by Mr Rahul Kumar:
#   https://tecadmin.net/backup-running-virtual-machine-in-xenserver/
# Created: 6/6/19
# Last Updated: 6/6/19
# Version: 1
#

# Import section, these are necessary modules for this script to run. # DON"T TOUCH
import time
import socket

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from modules import global_utilites
    else:
        from .modules import global_utilites

# Global Variables section # ADD BUT DON'T REMOVE
hostname = socket.gethostname()
time = time.strftime("%Y-%m-%d_%H:%M")
global_utilites = global_utilites.Global_Utilities()
g_banner = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
           "~       Welcome to XCP-ng Backup Utility      ~\n" \
           "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

while True:
    settings = global_utilites.load_settings()
    if settings == "no":
        global_utilites.initial_setup(g_banner)
        break
    else:
        break

global_utilites.load_menu(g_banner)

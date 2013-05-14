#!/usr/bin/env python

import sys

for i in range(30):
    print "\n" # double carriage return here.

print "Raw Print Server Setup\n"

print "Checking Prerequisites..."

try:
    import gobject, gtk, gtk.glade
except:
    print "Error:  Need a working PyGTK installation."
    sys.exit(1)

if sys.platform == "win32":
    try:
        import win32event, win32print, win32service, win32serviceutil
    except:
        print "Error:  On Windows, win32all needs to be installed."
        sys.exit(2)

print "Prerequisite Check:  OK!\n"

keys = {
    "PROGRAM": "/usr/share/rawprintserver",
}

myfiles = [
    ("logger.py", "PROGRAM"),
    ("printserver.py", "PROGRAM"),
    ("RawPrintServer.py", "PROGRAM"),
    ("RawPrintService.py", "PROGRAM"),
    ("rpsconf.py", "PROGRAM"),
    ("rpsprops.glade", "PROGRAM"),
    ("rpsprops.pyw", "PROGRAM"),
    ("spooler.py", "PROGRAM"),
]

if sys.platform == "win32":
    keys["PROGRAM"] = "C:/Program Files/RawPrintServer"
    # need to detect which windows version for the next part
    keys["MENU"] = "C:/Documents and Settings/All Users/Start Menu/Programs/Accessories/RawPrintServer"
    myfiles += [
        ("Raw Print Server Properties.lnk", "MENU"),
    ]


# end of file.

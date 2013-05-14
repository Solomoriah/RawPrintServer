#!/usr/bin/python
"""
rpsprops.py -- Raw Print Server Properties Script
"""

###########################################################################
# rpsprops.py -- Raw Print Server Properties Script
# Copyright 2005 Chris Gonnerman
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions
# are met:
# 
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer. 
# 
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution. 
# 
# Neither the name of the author nor the names of any contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###########################################################################

import sys, string
import gobject, gtk, gtk.glade

import rpsconf

interface = gtk.glade.XML("rpsprops.glade")

# initialize globals
cur_row = None
prnliststore = None
spooldir = None
logfile = None
prnqlabel = None

try:
    import win32print
    win32 = 1
except:
    win32 = 0

if win32:
    def getprinterlist(combo):
        store = combo.get_model()
        # clear existing list, if any
        while len(store) > 0:
            del store[0]
        prns = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)       
        for tup in prns:
            store.append((tup[2],))
        combo.child.set_editable(0)
        
else:
    def getprinterlist(combo):
        combo.child.set_editable(1)

def gtk_main_quit(*args):
    gtk.main_quit()

def showprinterpage():
    getprinterlist(interface.get_widget("printername"))
    interface.get_widget("notebook1").set_current_page(1)
    interface.get_widget("portnumber").grab_focus()

def on_addbutton_clicked(*args):
    global cur_row
    cur_row = -1
    port = interface.get_widget("portnumber")
    port.set_text("")
    printer = interface.get_widget("printername")
    printer.child.set_text("")
    prnqlabel.set_markup("<b>Add Print Queue</b>")
    showprinterpage()

def on_editbutton_clicked(*args):
    global cur_row
    printerlist = interface.get_widget("printerlist")
    model, sel = printerlist.get_selection().get_selected_rows()
    try:
        sel = sel[0][0]
    except:
        return
    cur_row = sel
    port = interface.get_widget("portnumber")
    port.set_text(str(model[sel][0]))
    printer = interface.get_widget("printername")
    printer.child.set_text(str(model[sel][1]))
    prnqlabel.set_markup("<b>Edit Print Queue</b>")
    showprinterpage()

def on_printerlist_row_activated(*args):
    on_editbutton_clicked(*args)

def on_prn_okbutton_clicked(*args):
    port = interface.get_widget("portnumber")
    printer = interface.get_widget("printername")
    if cur_row != -1:
        # edit existing row
        try:
            prnliststore[cur_row][0] = int(port.get_text())
            prnliststore[cur_row][1] = printer.child.get_text()
        except:
            import traceback
            traceback.print_exc(file = sys.stderr)
            print "editing a row: should handle the error here"
    else:
        # add new row
        try:
            prnliststore.append((int(port.get_text()), printer.child.get_text()))
        except:
            import traceback
            traceback.print_exc(file = sys.stderr)
            print "adding a row: should handle the error here"
    interface.get_widget("notebook1").set_current_page(0)

def on_deletebutton_clicked(*args):
    printerlist = interface.get_widget("printerlist")
    model, sel = printerlist.get_selection().get_selected_rows()
    try:
        sel = sel[0][0]
    except:
        return
    del prnliststore[sel]

def on_savebutton_clicked(*args):
    configuration = rpsconf.createconfig()
    configuration["spooldir"] = spooldir.get_text()
    configuration["logfile"] = logfile.get_text()
    for i in range(len(prnliststore)):
        configuration["printer"].append("%d, %s" 
            % (prnliststore[i][0], prnliststore[i][1]))
    rpsconf.saveconfig(configuration)

def on_prn_cancelbutton_clicked(*args):
    global edit_mode
    interface.get_widget("notebook1").set_current_page(0)

interface.signal_autoconnect(locals())

printerlist = interface.get_widget("printerlist")

cell0 = gtk.CellRendererText()
col0 = gtk.TreeViewColumn("Port", cell0, text = 0)
printerlist.append_column(col0)

cell1 = gtk.CellRendererText()
col1 = gtk.TreeViewColumn("Printer", cell1, text = 1)
printerlist.append_column(col1)

prnliststore = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
printerlist.set_model(prnliststore)

prnliststore.set_sort_column_id(0, gtk.SORT_ASCENDING)

prnqlabel = interface.get_widget("prnqlabel")

printer = interface.get_widget("printername")
prnpulldown = gtk.ListStore(gobject.TYPE_STRING)
printer.set_model(prnpulldown)
printer.set_text_column(0)

# load the configuration.

configuration = rpsconf.loadconfig()

spooldir = interface.get_widget("spooldir")

try:
    spooldir.set_text(configuration["spooldir"])
except:
    spooldir.set_text("")

logfile = interface.get_widget("logfile")

try:
    logfile.set_text(configuration["logfile"])
except:
    logfile.set_text("")

for row in configuration["printer"]:
    try:
        port, pname = string.split(row, ",", maxsplit = 1)
        port = int(port.strip())
        pname = pname.strip()
    except:
        print "Error Parsing Printer Configuration <%s>" % row
        continue
    prnliststore.append((port, pname))

# run it!

gtk.main()

###########################################################################
# end of file.
###########################################################################

"""
printserver.py -- Raw Print Server Core Module
"""

###########################################################################
# printserver.py -- Raw Print Server Core Module
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

###########################################################################
# Module Imports
###########################################################################

import socket, asyncore, os, sys, string
import spooler, logger

###########################################################################
# Variable Initialization
###########################################################################

# jobnumber is global because multiple server contexts may share it
jobnumber = 0

JOBNAME = "RawPrintJob%05d.prn"

servers = []

###########################################################################
# Class Definitions
###########################################################################


class print_server(asyncore.dispatcher):

    def __init__(self, addr, port, printer):
        self.addr = addr
        self.port = port
        self.printer = printer
        print "Starting Printer <%s> on port %d" \
            % (self.printer.printer_name, self.port)
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((addr, port))
        self.listen(5)

    def writable(self):
        return 0

    def readable(self):
        return self.accepting

    def handle_read(self):
        pass

    def handle_connect(self):
        pass

    def handle_accept(self):
        global jobnumber
        try:
            conn, addr = self.accept()
        except:
            print "Error, Accept Failed!"
            return
        jobnumber += 1
        handler = print_handler(conn, addr, self, jobnumber)

    def handle_close(self):
        print "Stopping Printer <%s> on port %d" \
            % (self.printer.printer_name, self.port)
        self.close()


class print_handler(asyncore.dispatcher):

    def __init__(self, conn, addr, server, jobnumber):
        asyncore.dispatcher.__init__(self, sock = conn)
        self.addr = addr
        self.server = server
        self.jobname = JOBNAME % jobnumber
        self.fp = open(self.jobname, "wb")
        print "Receiving Job from %s for Printer <%s> (Spool File %s)" \
            % (addr, self.server.printer.printer_name, self.jobname)

    def handle_read(self):
        data = self.recv(8192)
        if self.fp:
            self.fp.write(data)

    def writable(self):
        return 0

    def handle_write(self):
        pass

    def handle_close(self):
        print "Printer <%s>: Printing Job %s" \
            % (self.server.printer.printer_name, self.jobname)
        if self.fp:
            self.fp.close()
            self.fp = None
        fp = open(self.jobname, "rb")
        self.server.printer.sendjob(fp)
        fp.close()
        try:
            os.remove(self.jobname)
        except:
            print "Can't Remove <%s>" % self.jobname
        self.close()


def mainloop(config):

    if config["spooldir"]:
        os.chdir(config["spooldir"])

    for i in range(len(config["printer"])):
        args = string.split(config["printer"][i], ",", maxsplit = 1)
        prn = args[1].strip()
        port = int(args[0].strip())
        p = print_server('', 
            port, spooler.printer(prn))
        servers.append(p)

    try:
        try:
            asyncore.loop(timeout = 4.0)
        except KeyboardInterrupt:
            pass
    finally:
        print "Print Server Exit"


def terminate(*args):
    for s in servers:
        s.handle_close()


def setuplog(logfn):
    if not logfn:
        logfn = "rps.log"
    log = logger.LogFile(open(logfn, "a"))
    sys.stderr = sys.stdout = log


###########################################################################
# end of file.
###########################################################################

#!/usr/bin/python

"""
RawPrintServer.py -- Raw Print Server Main Module
"""

###########################################################################
# RawPrintServer.py -- Raw Print Server Main Module
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

import asyncore, printserver, spooler, rpsconf, os, signal

# configuration loading errors need to be handled before becoming a daemon
config = rpsconf.loadconfig()

# set up our log file before daemonizing
printserver.setuplog(config["logfile"])

###########################################################################
# become a daemon task -- standard method

pid = os.fork()

if (pid == 0): # child
    os.setsid()
    pid = os.fork()

    if (pid == 0): # child, final daemon process
        if config["spooldir"]:
            os.chdir(config["spooldir"])
            # don't do that twice!
            config["spooldir"] = None
        else:
            # config is missing; need a safe place to call "home"
            os.chdir("/tmp")
        os.umask(022)
    else:
        os._exit(0)
else:
    os._exit(0)

for fd in range(0, 2):
    try:
        os.close(fd)
    except OSError:
        pass

# note that the Pythonic standard IO will be redirected below
os.open("/dev/null", os.O_RDWR)
os.dup2(0, 1)
os.dup2(0, 2)

###########################################################################
# fire up the server task

print "\nRaw Print Server Startup: PID =", os.getpid()

# we want to clean up and finish the last jobs if we can
signal.signal(signal.SIGTERM, printserver.terminate)

printserver.mainloop(config)


###########################################################################
# end of file.
###########################################################################

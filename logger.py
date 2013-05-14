"""
logger.py -- Raw Print Server Logging Module

This module provides a convenient file-like object (writing only)
which dates output lines automatically.

There is also a public function, logtime(), which returns the current
date in the format used by the LogFile class.
"""

###########################################################################
# logger.py -- Raw Print Server Logging Module
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

__version__ = "1.1"

import sys, time, string

def logtime():
    return time.strftime("[%Y/%m/%d %H:%M:%S]", \
        time.localtime(time.time()))

class LogFile:
    def __init__(self,file):
        self.file = file
        self.remaining = ""
    def write(self, s):
        if type(s) is type(""):
            if s:
                cont = ""

                l = string.split(self.remaining + s, "\n")
                self.remaining = ""

                # if there are more than one item in the list,
                # and the last item is not "", the last part
                # did not end "\n" and will go into remaining.

                if len(l) > 1:
                    if l[-1] != "":
                        self.remaining = l[-1]
                    del l[-1]
                elif len(l) == 1:
                    self.remaining = l[0]
                    l = []

                for i in l:
                    if i:
                        self.file.write(logtime() + " " + cont + i + "\n")
                    else:
                        self.file.write("\n")
                    cont = ": "
            self.file.flush()
        else:
            raise TypeError, "invalid data for write() method"
    def close(self):
        return self.file.close()

###########################################################################
# Test Rig
###########################################################################

if __name__ == "__main__":
    pass

###########################################################################
# end of file.
###########################################################################

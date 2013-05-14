"""
spooler.py -- Raw Print Server Spooler Access Module
"""

###########################################################################
# spooler.py -- Raw Print Server Spooler Access Module
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

import sys

class base_printer:
    def __init__(self, printer_name = None):
        self.printer_name = printer_name

if sys.platform == "win32":

    import win32print

    def listprinters():
        prnlst = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
        prnlst = map(lambda x: x[2], prnlst)
        return prnlst

    class printer(base_printer):
        def sendjob(self, fp, title = "Raw Print Server Job"):
            hprinter = win32print.OpenPrinter(self.printer_name)
            hjob = win32print.StartDocPrinter(hprinter, 1, (title, None, "RAW"))
            try:
                blk = fp.read(8192)
                while blk:
                    win32print.WritePrinter(hprinter, blk)
                    blk = fp.read(8192)
            except:
                import traceback
                traceback.print_exc(file = sys.stdout)
            win32print.EndDocPrinter(hprinter)
            win32print.ClosePrinter(hprinter)

else:

    import os

    def listprinters():
        return None

    class printer(base_printer):
        def sendjob(self, fp, title = None):
            # title is irrelevant here
            out = os.popen("lpr -P'%s' >/dev/null 2>&1" \
                % self.printer_name, "wb")
            blk = fp.read(8192)
            while blk:
                out.write(blk)
                blk = fp.read(8192)
            rc = out.close()
            if rc is not None:
                print "Error: lpr returns %02x" % rc


###########################################################################
# Test Rig
###########################################################################

if __name__ == "__main__":
    print listprinters()

###########################################################################
# end of file.
###########################################################################

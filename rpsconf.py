"""
rpsconf.py -- Raw Print Server Config File Handler
"""

###########################################################################
# rpsconf.py -- Raw Print Server Config File Handler
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

import sys, os, string

try:
    # look for the user's preferred configuration file

    configfile = os.environ["RPSCONF"]

except KeyError:
    # don't have it, so let's think up a reasonable default

    if sys.platform == "win32":
        configfile = r"C:\Windows\System32\rpsrv.conf"
    else:
        configfile = "/etc/rpsrv.conf"

cfgskel = {
    "spooldir": None,
    "logfile": None,
    "printer": [ ],
}


def createconfig():
    """
    createconfig(): create an empty configuration 
                    dictionary based on the skeleton.
    """
    cfg = { }

    # dang this is ugly.  need to use a more generic object copier.
    # need to read the manual.
    for k in cfgskel.keys():
        if cfgskel[k] is None:
            cfg[k] = None
        else:
            cfg[k] = [ ]

    return cfg


def loadconfig(fn = None):
    """
    loadconfig(fn):  load configuration from the named file.  if the
                     name isn't given, load the config from the default
                     location.  returns a dictionary containing the
                     configuration settings.  errors are printed to
                     stdout but the configuration is created anyway.
    """

    cfg = createconfig()

    if fn is None:
        fn = configfile
    
    try:
        fp = open(fn, "r")
    except:
        return cfg

    lines = fp.readlines()
    fp.close()

    for i in range(len(lines)):
        l = lines[i].strip()
        if l and l[0] != '#':
            try:
                cmd, arg = string.split(l, "=", maxsplit = 1)
            except:
                print "Parse Error in <%s> at line %s" % (fn, i)
                continue
            cmd = cmd.strip()
            arg = arg.strip()
            if not cfg.has_key(cmd):
                print "Illegal Command <%s> in <%s> at line %d" % (cmd, fn, i)
                continue
            if type(cfg[cmd]) is type([]):
                cfg[cmd].append(arg)
            elif cfg[cmd] is not None:
                print "Duplicate Command <%s> in <%s> at line %d" % (cmd, fn, i)
                continue
            else:
                cfg[cmd] = arg

    return cfg


def saveconfig(cfg, fn = None):
    """
    saveconfig(cfg, fn): save given configuration dictionary to named file.
    """
    
    if fn is None:
        fn = configfile

    fp = open(fn, "w")

    for k in cfg.keys():
        if type(cfg[k]) is type([]):
            for elem in cfg[k]:
                fp.write("%s = %s\n" % (k, elem))
        elif cfg[k] is not None:
            fp.write("%s = %s\n" % (k, cfg[k]))

    fp.close()


###########################################################################
# end of file.
###########################################################################

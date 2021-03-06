# -*- coding: utf-8 -*-

"""
fortune.py

A script that tells fortune messages, using the system's fortune command.
"""

from threading import Timer
from subprocess import Popen, PIPE
import re

class Fortune(object):

    NAME = "fortune"
    PARAMS = [('int', "length")]
    HELP = "!fortune [category] - Receive a fortune cookie from an optional "\
           "category"

    def __init__(self, length):
        if length < 0:
            length = 0
        self.length = length

    def on_pubmsg(self, source, channel, text):
        args = text.split()
        if not args or args[0] != "!fortune":
            return
        category = args[1] if len(args) > 1 else None
        return self.get_fortune(category)

    def get_fortune(self, category):
        cmd = ["fortune", "-sn", str(self.length)]
        if category:
            #Sanitize
            category = category.split()[0]
            category = "".join([c for c in category if c.isalnum()])
            cmd.append(category)
        proc = Popen(cmd, stderr=PIPE, stdout=PIPE)
        def killproc():
            if proc.poll() == None:
                try:
                    proc.kill()
                except:
                    pass
        timeout = Timer(0.5, killproc)
        timeout.start()
        res, _ = proc.communicate()
        timeout.cancel()
        if not res:
            res = "ERROR: Fortune not found"
        else:
            res = res.decode("latin1")
            res = res.strip()
            res = re.sub(r"[ \t\r\n]+", " ", res)
        return res

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE
import time


def notify(message):
    os.system("terminal-notifier -sound default -title Cisco VPN '' -message " + message )


# Set up the process
p = Popen("./state.sh", stdout=PIPE, close_fds=True)
while True:
    for lines_nums in xrange(1, 7):
        inline = p.stdout.readline()
        if "Disconnected" in inline:
            notify('Disconnected')

    time.sleep(30)


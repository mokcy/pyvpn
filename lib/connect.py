#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from subprocess import Popen, PIPE
from os.path import expanduser
import pexpect

home = expanduser("~")

def notify(message):
    os.system("terminal-notifier -sound default -title Cisco VPN '' -message " + message)


def disconnect():
    os.system("/opt/cisco/anyconnect/bin/vpn disconnect")


def connection(address, vpngroup, username, password):
    child = pexpect.spawn('/opt/cisco/anyconnect/bin/vpn connect ' + address, maxread=2000)
    child.logfile = sys.stdout
    child.expect('Group: \[.*\]')
    child.sendline(vpngroup)
    child.expect('Username: \[.*\]')
    child.sendline(username)
    child.expect('Password:')
    child.logfile = None
    child.sendline(password)
    child.logfile = sys.stdout
    child.expect('  >> notice: Establishing VPN session...')
    child.expect('  >> state: Connected')


def is_connect():
    global p, lines_nums, inline
    p = Popen(["/opt/cisco/anyconnect/bin/vpn", "state"], stdout=PIPE, close_fds=True)
    for lines_nums in xrange(1, 7):
        inline = p.stdout.readline()
        if "state: Connected" in inline:
            notify("Connected")
            return True
        elif "state: Disconnected" in inline:
            notify("Disconnected")
            return False


def read_config():
    text_file = open(home + "/.uap", "r")
    lines = text_file.read().split('\n')
    return lines


def main():
    while True:
        if not is_connect():
            configure = read_config()
            connection(configure[0], '1', configure[1], configure[2])

        time.sleep(30)


if __name__ == '__main__':
    main()
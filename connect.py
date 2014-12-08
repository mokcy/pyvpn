#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from subprocess import Popen, PIPE

import pexpect


def notify(message):
    os.system("terminal-notifier -sound default -title Cisco VPN '' -message " + message)


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


def check_state():
    global p, lines_nums, inline
    # Set up the process
    p = Popen("./state.sh", stdout=PIPE, close_fds=True)
    while True:
        for lines_nums in xrange(1, 7):
            inline = p.stdout.readline()
            if "Disconnected" in inline:
                notify('Disconnected')

        time.sleep(30)


def read_config():
    text_file = open(".uap", "r")
    lines = text_file.read().split('\n')
    return lines


def main():
    configure = read_config()
    connection('mel-vpn.realestate.com.au', '1', configure[0], configure[1])
    # check_state()


if __name__ == '__main__':
    main()
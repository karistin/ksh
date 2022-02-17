#!/usr/bin/env python
import termios
import sys
import tty
from copy import deepcopy



def set_mode():
    fd = sys.stdin.fileno()
    new = termios.tcgetattr(fd)
    old = deepcopy(new)

    new[3] &= ~termios.ECHO
    # none echo mode

    new[3] &= ~termios.ICANON
    # noncannonical mode

    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0
    # blocking read
    try:
        # tty.setraw(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch 


def get_ch():
    ch = set_mode()
    # if ch == '\x1b[D':
    #     print("left")
    # elif ch =='\x1b[C':
    #     print ("right")
    # elif ch=='\x1b[A':
    #     print ("UP")
    # elif ch=='\x1b[B':
    #     print ("down")
    # else:
    sys.stdout.write(ch)
    sys.stdout.flush()
        # it will write everything in the buffer to the terminal,

if __name__=="__main__":
    # for i in range(20):
    while(True):
        get_ch()

#!/usr/bin/env python
import termios
import sys
from copy import deepcopy


def timeout_mode(new, fd):
    new[6][termios.VMIN] = 0
    new[6][termios.VTIME] = 1
    # read with timeout
    # why => time out 시 또는 1byte 입력시
    termios.tcsetattr(fd, termios.TCSADRAIN, new)
    ch = sys.stdin.read(1)

    if ch == "[":
        ch = sys.stdin.read(1)
        if ch == "B":    # down
            ch = ""
        elif ch == "C":  # right
            ch = u"\u001b[1C"
        elif ch == "A":  # up
            ch = ""
        elif ch == "D":  # left
            ch = u"\u001b[1D"
    return ch


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
    # Minbyte 가 입력될때 까지 계속 진행
    try:
        # tty.setraw(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch = timeout_mode(new, fd)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def get_ch():
    ch = set_mode()
    sys.stdout.write(ch)
    sys.stdout.flush()
    #  it will write everything in the buffer to the terminal,


if __name__ == "__main__":
    # for i in range(20):
    while(True):
        get_ch()

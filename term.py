#!/usr/bin/env python
import termios
import sys
from copy import deepcopy

write_pos = {'x': 0, 'y': 0}


def std_write_flush(val):
    sys.stdout.write(val)
    sys.stdout.flush()


def variable_setting(setting):
    fd = sys.stdin.fileno()
    new = termios.tcgetattr(fd)
    old = deepcopy(new)
    new[3] &= ~termios.ECHO
    # none echo mode

    new[3] &= ~termios.ICANON
    # noncannonical mode

    if setting == 'timeout':
        new[6][termios.VMIN] = 0
        new[6][termios.VTIME] = 1
        # read with timeout
        # time out 시 또는 1byte 입력시
    elif setting == 'blocking_read':
        new[6][termios.VMIN] = 1
        new[6][termios.VTIME] = 0
        # blocking read
        # Minbyte 가 입력될때 까지 계속 진행
    elif setting == 'default':
        pass
    return fd, new, old


def timeout_mode():
    fd, new, old = variable_setting('timeout')
    termios.tcsetattr(fd, termios.TCSADRAIN, new)
    try:
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def now_pos():
    fd, new, old = variable_setting('default')
    x, y = '', ''
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        std_write_flush(u'\u001b[6n')
        ch = sys.stdin.read(2)
        if ch == u'\u001b[':
            while True:
                ch = sys.stdin.read(1)
                if ch == ';':
                    break
                y += ch
            while True:
                ch = sys.stdin.read(1)
                if ch == 'R':
                    break
                x += ch
        else:
            x, y = 0, 0
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return int(x), int(y)


def blocking_mode():
    fd, new, old = variable_setting('blocking_read')
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def get_ch():
    ch = blocking_mode()
    if ch == '\x1b':  # ascii 127
        ch = timeout_mode()
        if ch == '[':
            ch = sys.stdin.read(1)
            if ch == 'B':    # down
                ch = ''
            elif ch == 'C':  # right
                pos_x, pos_y = now_pos()
                if pos_x < write_pos['x']:
                    ch = u'\u001b[1C'
                else:
                    ch = ''
            elif ch == 'A':  # up
                ch = ''
            elif ch == 'D':  # left
                ch = u'\u001b[1D'
            std_write_flush(ch)
    elif ch == '\x7f':  # ord(ch) == 127
        std_write_flush(u'\u001b[1D\u001b[1P')
        write_pos['x'] = write_pos['x'] - 1
    else:
        std_write_flush(ch)
        write_pos['x'], write_pos['y'] = now_pos()


if __name__ == "__main__":
    while True:
        get_ch()

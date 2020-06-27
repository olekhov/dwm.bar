#!/usr/bin/env python3

import signal
import time
from pid import PidFile
import sys

import alsaaudio


#fontawesome
batsym=['','','','','']
charging='\uf0e7'
tempsym=["\uf2cb", "\uf2ca", "\uf2c9", "\uf2c8", "\uf2c7"]
def sound_bar():

    vol_low = ''
    vol_med = ''
    vol_hi = ''
    vol_mute = ''
    m=alsaaudio.Mixer()
    vol = m.getvolume()[0]
    mute = m.getmute()[0]
    print(f"{vol}%", end='')
    if mute:
        print(vol_mute,end='')
    else:
        if vol < 30:
            print(vol_low, end='')
        elif vol<70:
            print(vol_med, end='')
        else:
            print(vol_hi, end='')
    pass

def power_bar():
    print(f"\x1b[38;2;255;255;0m{charging}", end='')
    #print(f"\x1b[38;2;255;0;0m {charging}", end='')
    #print(charging,end='')
    print(f"\x1b[38;2;0;0;255m", end='')
    for x in batsym:
        print(x, end='')
    pass

def refbar():
    sound_bar()
    print(" ", end='')
    power_bar()
    pass


def refbar_signal(signal,frame):
    refbar()


refbar()
sys.exit(0)

signal.signal(signal.SIGRTMIN+8, refbar_signal)

with PidFile(pidname="/tmp/dwmbar.pid") as p:
    print(p.pidname)
    print(p.piddir)
    while True:
        refbar()
        time.sleep(30)

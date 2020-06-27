#!/usr/bin/env python3

import signal
import time
from pid import PidFile
import sys
import datetime
import psutil
import pdb

import alsaaudio
import subprocess
import locale

#fontawesome
batsym=['','','','','']
volsym=['\uf026', '\uf027', '\uf028']
vol_mute = ''

charging='\uf0e7'
tempsym=["\uf2cb", "\uf2ca", "\uf2c9", "\uf2c8", "\uf2c7"]

hourglass='\uf250'

memsym='\uf538'
chipsym='\uf2db'

col_green ="\x1b[38;2;0;255;0m"
col_lime  ="\x1b[38;2;128;255;0m"
col_yellow="\x1b[38;2;255;255;0m"
col_orange="\x1b[38;2;255;128;0m"
col_red   ="\x1b[38;2;255;0;0m"

cols=[col_green, col_lime, col_yellow, col_orange, col_red]
col_reset="\x1b[0m"

def sound_bar():
    m=alsaaudio.Mixer()
    vol = m.getvolume()[0]
    mute = m.getmute()[0]
    res=f"{vol:2}%{vol_mute if mute else volsym[int(vol/34)]}"
    return res

def mem_bar():
    mem = psutil.virtual_memory()
    return f"{memsym}{mem.percent}"

def cpu_bar():
    cpu = psutil.cpu_percent()
    col = cols [ int(cpu/21) ]
    return f"{col}{chipsym}{cpu:02.0f}%{col_reset}"

def secs2h(s):
    if s<0:
        return '\uf534'
    mm,ss = divmod(s,60)
    hh,mm = divmod(mm,60)
    return f"{hh:02}:{mm:02}"

def temperature_bar():
    t=psutil.sensors_temperatures()
    zs=list(zip(tempsym, cols))
    laptop="\uf109"

    ta=t['acpitz'][0]
    # 20.. ta.critical
    ta_level=int( (ta.current - 20-1) / (ta.critical - 20) * 5)
    res=f"{zs[ta_level][1]}{laptop}{zs[ta_level][0]}{ta.current:2.0f}{col_reset}"

    tcpu=t['coretemp'][0]
    tcpu_level=int( (tcpu.current - 20-1) / (tcpu.critical - 20) * 5)
    res=res+f"{zs[tcpu_level][1]}{chipsym}{zs[tcpu_level][0]}{tcpu.current:2.0f}{col_reset}"
    return res


def power_bar():
    bat = psutil.sensors_battery()
    if bat.power_plugged :
        if bat.percent>99 :
            accol="\x1b[38;2;224;224;255m"
        else:
            accol="\x1b[38;2;255;255;0m"
    else :
        accol = "\x1b[38;2;0;0;0m"

    bc = list(zip (batsym, cols[::-1]))[ int(bat.percent/21) ]
    res=f"{accol}{charging}{col_reset}"
    res=res+f"{bc[1]}{bc[0]}{bat.percent:.0f}% "
    res=res+f"{hourglass}{secs2h(bat.secsleft)}{col_reset}"
    return res

def date_bar():
    #return datetime.datetime.now().strftime("%Y.%m.%d (%a) %H:%M")
    return datetime.datetime.now().strftime("%d %b (%a) %H:%M")

def build_bar():
    res=""
    res=res+" "+sound_bar()
    res=res+" "+temperature_bar()
    res=res+" "+cpu_bar()
    res=res+" "+mem_bar()
    res=res+" "+power_bar()
    res=res+" "+date_bar()
    return res

def refbar():
    s=build_bar()
    print(f"refreshing: {s}")
    subprocess.Popen(["xsetroot", "-name", s])
    pass


def refbar_signal(signal,frame):
    refbar()


def xsetroot_name(s):
    d=display.Display()

#pdb.set_trace()
#refbar()
#sys.exit(0)

locale.setlocale(locale.LC_ALL,'')

signal.signal(signal.SIGRTMIN+8, refbar_signal)

with PidFile(pidname="/tmp/dwmbar.pid") as p:
    print(p.pidname)
    print(p.piddir)
    while True:
        refbar()
        time.sleep(3)

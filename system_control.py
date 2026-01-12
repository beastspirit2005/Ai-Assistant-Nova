import os
import ctypes
import subprocess


def volume_up():
    
    for _ in range(5):
        ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)  


def volume_down():
    for _ in range(5):
        ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)  


def mute():
    ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)  


def unmute():
    ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)



def lock_system():
    ctypes.windll.user32.LockWorkStation()


def sleep_system():
    subprocess.call(
        ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def restart_system():
    os.system("shutdown /r /f /t 0")
    
    


def shutdown_system():
    os.system("shutdown /s /f /t 0")

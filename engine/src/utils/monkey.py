from re import I
from secrets import randbits
import pyautogui as gui
from time import sleep
from random import randint

from utils.log import error

gui.FAILSAFE = False

def pause(k=1000):
    t = randint(1, 100)/k
    sleep(t)

def click():
    gui.moveTo(200,200)
    gui.click()

def scroll(N=-100):
    gui.scroll(N)

def enter():
    gui.press('return')
    pause()

def space():
    gui.press('space')
    pause()

def next():
    gui.press('tab')
    pause()

def back():
    gui.hotkey('shift', 'tab')
    pause()

def arrow_down():
    gui.press('down')
    pause()

def arrow_up():
    gui.press('up')
    pause()

def save():
    gui.hotkey('cmd', 's')
    pause()

def press(key):
    gui.press(key)
    pause()

def email():
    error('OTP detected: Please verify the email manually -- press enter to continue')
    input()

def captcha():
    error('Captcha detected: Please solve the captcha manually -- press enter to continue')
    input()

def type(text):
    for char in text:
        gui.press(char)
        pause()
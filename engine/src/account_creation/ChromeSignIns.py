import sys
sys.path.append('..')
import utils.monkey as monkey
from utils.util import wait; 
import os
import pyautogui
import sys
sys.path.append('..')
from utils.util import wait
from browser.Selenium import Browser

def loadBrowser(userId):
    session = f'/{userId}'
    browser = Browser(session)
    driver = browser.getDriver()
    return driver

def createProflie(email, password, userId):
    driver = loadBrowser()
    wait(3)
    driver.get('https://accounts.google.com/ServiceLogin?service=chromiumsync')
    wait(3)
    # email
    monkey.next()
    wait(1)
    monkey.type(email)
    wait(1)
    monkey.enter() 
    wait(3)

    # password
    monkey.type(password)
    wait(1)
    monkey.enter()

    input()


import json
import constants
import pandas as pd

def checkProflies():
    file = f"{constants.SESSIONS_PATH}googles/Local State"
    with open(file, 'r') as f:
        data = json.load(f)
        data = data['profile']['info_cache']
        data = pd.DataFrame(data)
        data.to_csv('data.csv')


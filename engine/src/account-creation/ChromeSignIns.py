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


email = "aceap006@spartaaceap.com"
password = "hehehahahoho7"
userId = "aceap6"

def loadBrowser():
    session = 'googles/'
    browser = Browser(session)
    driver = browser.getDriver()
    return driver

def createProflie(email, password, userId):
    driver = loadBrowser()
    wait(3)

    # Add new user
    monkey.back()
    wait(0.5)
    monkey.back()
    wait(0.5)
    monkey.back()
    wait(0.5)
    monkey.space()

    # Signin
    wait(1)
    monkey.next()
    wait(0.5)
    monkey.space()

    # Email
    wait(1)
    monkey.type(email)
    wait(0.5)
    monkey.enter()

    # Password
    wait(1)
    monkey.type(password)
    wait(0.5)
    monkey.enter()

    # Im In
    wait(1)
    monkey.next()
    wait(0.5)
    monkey.space()

    # Ads
    wait(1)
    monkey.next()
    wait(0.5)
    monkey.next()
    wait(0.5)
    monkey.next()
    wait(0.5)
    monkey.space()

    # Profile
    wait(1)
    monkey.type(userId)
    wait(0.5)
    monkey.next()
    wait(0.5)
    monkey.next()
    wait(0.5)
    monkey.enter()

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


createProflie(email, password, userId)
checkProflies()
input()
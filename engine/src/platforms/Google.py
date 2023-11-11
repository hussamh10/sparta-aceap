from datetime import datetime
import sys
sys.path.append('..')

from time import sleep
from src.constants import USERS_PATH
from utils.log import pprint, error;
# from browser.Selenium import Browser
from browser.Selenium import Browser
import os
import constants
import pickle as pkl
from utils.log import debug, info, error
from utils.util import wait
import utils.monkey as monkey
import pandas as pd


# https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

class Google():
    def __init__(self):
        self.url = 'https://accounts.google.com/signin'
        self.users = dict()
    
    def loadUserData(self, users):
        # users = pd.read_csv(users)
        email = 'aceap003@spartaaceap.com'
        self.users[email] = dict()
        self.users[email]['password'] = 'hehehahehoho'
        self.users[email]['firstname'] = 'Ahmed'
        self.users[email]['lastname'] = 'Hussnain'

    def createUsers(self):
        for user in self.users:
            self.createUser(user)

    def loadBrowser(self):
        session = f'google_create'
        print(session)
        browser = Browser(session)
        self.driver = browser.getDriver()
        debug('Browser loaded')
        return self.driver

    def loadWebsite(self):
        self.driver.get(self.url)

    def createUser(self, user):
        email = user
        password = self.users[email]['password']
        firstname = self.users[email]['firstname']
        lastname = self.users[email]['lastname']

        self.loadBrowser()       
        wait(4)
        self.loadWebsite()
        wait(2)

        monkey.next()
        monkey.type(email)
        monkey.enter()
        input()
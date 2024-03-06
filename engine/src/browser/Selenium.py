import sys
from tkinter import W; sys.path.append('..')
from utils.log import *
import os
import pyautogui as gui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from time import sleep
import constants
import pickle as pkl
import utils.monkey as monkey

class Browser:
    def __init__(self, session):
        # CHROME UNDETECTED       
        self.session = session
        path = os.path.join(constants.SESSIONS_PATH, self.session)
        options = uc.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        self.driver = uc.Chrome(user_data_dir=path, options=options, use_subprocess=False)
        sleep(4)
        monkey.GotIt()
        sleep(2)
        monkey.GotIt()
        sleep(1)
        gui.hotkey('win', 'up')
        sleep(2)
        return 

        
        # SELENIUM
        self.session = session
        # self.service = Service(ChromeDriverManager("115.0.5763.0").install())
        self.service = Service(ChromeDriverManager().install())
        self.options = Options()
        self.loadOptions()
        self.loadSession()
        self.driver = uc.Chrome(service=self.service, options=self.options)
        # self.driver = uc.Chrome()
        self.anti_bot_detection()

    def anti_bot_detection(self):
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def getDriver(self):
        return self.driver

    def loadSession(self):
        path = os.path.join(constants.SESSIONS_PATH, self.session)
        debug(path)
        self.options.add_argument(f"user-data-dir={path}") 

    def loadOptions(self):
        self.options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 1}
        )
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("--disable-notifications")
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-blink-features=AutomationControlled')

        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)

def bot_test(session):
    # session = 'facebook-test'
    browser = Browser(session)
    d = browser.getDriver()
    url='https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php'
    d.get(url)
    sleep(5)
    # click button with class go
    d.find_elements('xpath', '//button[@class="go"]')[0].click()
    sleep(200)
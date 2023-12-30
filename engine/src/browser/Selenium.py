import sys
from tkinter import W; sys.path.append('..')
from utils.log import *
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from time import sleep
import constants
import pickle as pkl

class Browser:
    def __init__(self, session):
        self.session = session
        # self.service = Service(ChromeDriverManager("115.0.5763.0").install())
        self.service = Service(ChromeDriverManager().install())
        self.options = Options()
        self.loadOptions()
        self.loadSession()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.anti_bot_detection()
        # self.driver = uc.Chrome()

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
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        # self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
        # self.options.add_experimental_option("eSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        # self.options.add_argument('media.autoplay.default',0)
        # self.options.add_argument('media.default_volume',0)
        # self.options.add_argument('media.mediasource.enabled',1)
        # self.options.add_argument('media.mediasource.webm.enabled',1)
        # self.options.add_argument('media.mediasource.mp4.enabled',1)
        # self.options.add_argument('media.wmf.enabled',1) 
        # self.options.add_argument('media.mp4.enabled',1)
        # self.options.add_argument('media.webm.enabled',1)
        # self.options.add_argument('dom.webdriver.enabled','false')
        #self.options.add_argument('security.insecure_field_warning.contextual.enabled','1')

        # if proxyFlag:
        #     print("ProxyFlag: {} -----------  Port: {}".format(proxyFlag, port))
        #     self.options.add_argument('network.proxy.type', 1)
        #     self.options.add_argument('network.proxy.socks', '127.0.0.1')
        #     self.options.add_argument('network.proxy.socks_port', port)

        # self.options.add_argument('layers.acceleration.disabled','true')
        # self.options.add_argument('webgl.force-enabled','true')
        # self.options.add_argument('webgl.disabled','false')
        # self.options.add_argument('marionette.enabled','false')

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
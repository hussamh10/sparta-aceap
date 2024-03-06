from datetime import datetime
import signal
import sys
from time import sleep
from constants import USERS_PATH
from utils.log import pprint, error, log; sys.path.append('..')
from utils.util import wait
# from browser.Selenium import Browser
from browser.Selenium import Browser
from selenium.webdriver.common.by import By
import os
import constants
import pickle as pkl
from abc import ABC, abstractclassmethod
from utils.log import debug, info, error
from utils import monkey
from PIL import Image
import pyautogui as gui


# https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

class Platform(ABC):
    def __init__(self, platform, url, userId):
        self.platform = platform
        self.url = url
        self.userId = userId

    # @abstractclassmethod
    # def createUser(self, user):
    #     pass

    def loadBrowser(self):
        path = constants.SESSIONS_PATH
        if not os.path.exists(f'{path}{self.platform}'):
            os.mkdir(f'{path}{self.platform}')

        log(f'Loading browser for user: {self.userId}')
        id = self.userId
        path = os.path.join(constants.SESSIONS_PATH, id)

        if not os.path.exists(path):
            error(f'User {id} does not exist')
            os.mkdir(path)

        try:
            browser = Browser(id)
        except Exception as e:
            error(e)
            error('Could not load browser')
            debug('Trying again...')
            try:
                wait(3)
                browser = Browser(id)
            except Exception as e:
                error('Could not load browser again')
                raise e

        self.driver = browser.getDriver()
        return self.driver

    def quit(self):
        self.closeDriver()

    def loadWebsite(self):
        self.driver.get(self.url)

    def loadPage(self, url):
        self.driver.get(url)
    
    def chromeLogin(self):
        try:
            wait(1)
            screenWidth, screenHeight = gui.size()
            if screenWidth == 1920:
                monkey.click(x=1800, y=245)
            else:
                monkey.click(x=2300, y=230)
            return f'{self.userId}@spartaaceap.com'
        except Exception as e:
            print(e)
            return False
            pass

    def scrollTop(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scrollDown(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def searchTerm(self, term, bar=True):
        if bar:
            self._searchTermBar(term)
        else:
            self._searchTermUrl(term)

    def closeDriver(self):
        info('Closing browser')
        wait(1)
        self.driver.quit()
        wait(3)
        if hasattr(self.driver, "service") and getattr(self.driver.service, "process", None):
            self.driver.service.process.wait(3)
        try:
            # os.waitpid(self.driver.browser_pid, 0)
            os.kill(self.driver.browser_pid, signal.SIGTERM)
        except Exception as e:
            error('Could not close browser')
            error(e)
            try:
                os.system("taskkill /im chrome.exe /f")
            except Exception as e:
                error('Could not close browser again')
                error(e)

    def close(self):
        self.b

    @abstractclassmethod
    def loggedIn(self):
        pass
########################################################################################################################

# Search Platform
    @abstractclassmethod
    def _searchTermBar(self, term):
        pass

    @abstractclassmethod
    def _searchTermUrl(self, term):
        pass

# Navigate Platform   

    @abstractclassmethod
    def getHomePage(self):
        pass
    
# Interaction

    @abstractclassmethod
    def joinCommunity(self):
        pass

    @abstractclassmethod
    def followUser(self):
        pass

    @abstractclassmethod
    def openPost(self, already_opened=[]):
        pass

    @abstractclassmethod
    def likePost(self):
        pass

    @abstractclassmethod
    def getPagePosts(self, n=10):
        pass

    def TakeScreenshot(self, file):
        debug("Taking screenshot")
        self.driver.save_screenshot(file)
        debug(f'Screenshot saved: {file}')
        return True

    
    def screenshot(self, file):
        debug("Taking screenshot")
        self.driver.save_screenshot(file)
        debug(f'Screenshot saved: {file}')
        return True

    def fullScreenshot(self, file):
        debug("Taking screenshot")
        total_width = self.driver.execute_script("return document.body.offsetWidth")
        total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = self.driver.execute_script("return document.body.clientWidth")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        rectangles = []

        # first go all the way up
        self.driver.execute_script("window.scrollTo(0, 0)")       

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height
            if top_height > total_height:
                top_height = total_height
            while ii < total_width:
                top_width = ii + viewport_width
                if top_width > total_width:
                    top_width = total_width
                rectangles.append((ii, i, top_width, top_height))
                ii += viewport_width
            i += viewport_height
        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0
        for rectangle in rectangles:
            if not previous is None:
                self.driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                wait(0.2)
            file_name = "part_{0}.png".format(part)
            self.driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)
            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])
            stitched_image.paste(screenshot, offset)
            del screenshot
            os.remove(file_name)
            part += 1
            previous = rectangle
        stitched_image.save(file)
        debug('Screenshot saved...')
        wait(1)
        self.driver.execute_script("window.scrollTo(0, 0)")       
        return True
from datetime import datetime
import sys
from time import sleep
from src.constants import USERS_PATH
from utils.log import pprint, error; sys.path.append('..')
# from browser.Selenium import Browser
from browser.Selenium import Browser
import os
import constants
import pickle as pkl
from abc import ABC, abstractclassmethod
from utils.log import debug, info, error


# https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

class Platform(ABC):
    def __init__(self, platform, url, userId):
        self.platform = platform
        self.url = url
        self.userId = userId

    @abstractclassmethod
    def createUser(self, user):
        pass

    def loadBrowser(self):
        path = constants.SESSIONS_PATH
        # if not os.path.exists(f'{path}{self.platform}'):
        #     os.mkdir(f'{path}{self.platform}')

        id = self.userId

        path = os.path.join(constants.SESSIONS_PATH, id)

        if not os.path.exists(path):
            raise Exception(f'User {id} does not exist')
            os.mkdir(f'{path}{self.platform}/{id}')

        browser = Browser(path)
        self.driver = browser.getDriver()
        return self.driver

    def quit(self):
        self.driver.quit()

    def loadWebsite(self):
        self.driver.get(self.url)

    def loadPage(self, url):
        self.driver.get(url)
    
    def chromeLogin(self):
        try:
            element = self.driver.find_element("id", "credential_picker_container")
            element.click()
        except:
            pass
    
    def scrollDown(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def searchTerm(self, term, bar=True):
        """
        Search a term in the platform. There are
        two ways to search, using the search bar
        or using the search url.

        :param term: the search term
        :param bar: if true, uses search bar, else load the search url (True by default)
        :return: returns nothing
        """ 
       
        if bar:
            self._searchTermBar(term)
        else:
            self._searchTermUrl(term)

    # TODO fix this
    # def saveResults(self, results, when=''):
    #     username = self.user.name
    #     platform = self.platform
    #     interaction = self.user.interaction
    #     value = self.user.topic

    #     results['timestamp'] = str(datetime.now())
    #     results['username'] = username
    #     results['platform'] = platform
    #     results['interaction'] = interaction
    #     results['topic'] = value
    #     results['when'] = when

    #     dir = f'{constants.USERS_PATH}{username}/{platform}/{value}/{interaction}/'
    #     if not os.path.exists(dir):
    #         os.makedirs(dir)

    #     dir += results['timestamp']
    #     pkl.dump(results, open(dir, 'wb'))

    #     print(dir)
    #     if constants.DEBUG:
    #         print(results)
    #     return results

    def close(self):
        self.driver.close()

    def loggedIn(self):
        error('Not implemented -- sleeping')
        sleep(10000)
        return False

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

    def followUser(self):
        pass

    def readComments(self):
        pass

    # @abstractclassmethod
    def openPost(self):
        pass

    def stayOnPost(self, time=5):
        sleep(time)

    # @abstractclassmethod
    def likePost(self):
        pass

    # @abstractclassmethod
    def dislikePost(self):
        pass



# Record Observaions

    @abstractclassmethod
    def getPagePosts(self, n=10):
        pass
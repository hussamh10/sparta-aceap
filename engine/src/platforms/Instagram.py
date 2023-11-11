import sys; sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import constants

# https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

import constants


class Instagram(Platform):

    name = 'instagram'
    url='https://www.instagram.com'
    search_url='NONE'

    def __init__(self, user):
        super().__init__(Instagram.name, Instagram.url, user)

    def _searchTermUrl(self, term):
        error("No search url for instagram!, use search bar")
        # search_query = Instagram.search_url % (term)
        # self.loadPage(search_query)

    def _searchTermBar(self, term):
        search_bar = self._getSearchBar()
        search_bar.send_keys(term)
        sleep(3)

    def _getSearchBar(self):
        return self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
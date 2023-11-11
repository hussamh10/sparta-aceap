import sys; sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import constants

# REQUIRED CAPTCHA!
# https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

import constants

class TikTok(Platform):
    name = 'tiktok'
    url='https://www.tiktok.com'
    search_url='https://www.tiktok.com/search/user?q=%s'
    # Tiktok also adds the timestamp in front of the search like this: https://www.tiktok.com/search/user?q=abortion&t=1646274640529

    def __init__(self, user):
        super().__init__(TikTok.name, TikTok.url, user)

    def _searchTermUrl(self, term):
        search_query = TikTok.search_url % (term)
        self.loadPage(search_query)

    def _searchTermBar(self, term):
        search_bar = self._getSearchBar()
        print(search_bar)
        search_bar.send_keys(term)
        sleep(1)
        search_bar.send_keys(Keys.ENTER)

    def _getSearchBar(self):
        return self.driver.find_element(By.XPATH, "//input[@placeholder='Search accounts']")
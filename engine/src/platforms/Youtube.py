import sys; sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import constants
from constants import pprint
import utils.monkey as monkey

class Youtube(Platform):
    name = 'youtube'
    url='https://www.youtube.com'
    search_url='https://www.youtube.com/results?search_query=%s'

    def __init__(self, user):
        super().__init__(Youtube.name, Youtube.url, user)

    def createUser(self, profile):
        pass

    def _searchTermUrl(self, term):
        search_query = Youtube.search_url % (term)
        self.loadPage(search_query)

    def _searchTermBar(self, term):
        search_bar = self._getSearchBar()
        print(search_bar)
        search_bar.send_keys(term)
        sleep(1)
        search_bar.send_keys(Keys.ENTER)

    def _getSearchBar(self):
        return self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")

    def getHomePage():
        pass


    def followUser(self, channel=None, name=None):
        if channel:
            sleep(3)
            self.loadPage(channel['url'])
            sleep(2)
            elems = self.driver.find_elements(By.XPATH, '//yt-formatted-string[text()="Subscribe"]')
            elems[0].click()
        elif name:
            # search for channel
            pass
        else:
            raise Exception("No channel specified")
    
    def openChannel(self):
        sleep(1)
        filters = self.driver.find_element(By.XPATH, '//tp-yt-paper-button[@aria-label="Search filters"]')
        filters.click()
        sleep(1)
        channels = self.driver.find_element(By.XPATH, '//yt-formatted-string[text()="Channel"]')
        channels.click()
        

    def joinCommunity(self):
        raise Exception("No communities in Youtube")

    def getPagePosts(self):
        sleep(3)
        videos = []
        # Names
        titles = self.driver.find_elements(By.XPATH, "//a[@id='video-title']")
        channels = self.driver.find_elements(By.XPATH, "//div[@id='channel-info']")

        position = 0
        for title, channel in zip(titles, channels):
            video = dict()
            video['position'] = position
            video['name'] = title.text
            video['url'] = title.get_attribute('href')
            video['channel'] = channel.text
            videos.append(video)
            position += 1

        for video in videos:
            print(video)

        return videos


    def openPost(self, video=None, position=None):
        if video:
            self.loadPage(video['url'])
        elif position:
            videos = self.getPagePosts()
            self.loadPage(videos[position]['url'])
        else:
            raise Exception("No video specified")

    def likePost(self):
        sleep(5)
        elems = self.driver.find_elements(By.XPATH, '//yt-icon[@class="style-scope ytd-toggle-button-renderer"]')
        print(len(elems))
        elems[0].click()
        sleep(10000)


    def dislikePost(self):
        sleep(5)
        elems = self.driver.find_elements(By.XPATH, '//yt-icon[@class="style-scope ytd-toggle-button-renderer"]')
        print(len(elems))
        elems[1].click()
        sleep(10000)

    def readComments(self):
        sleep(5)
        monkey.click()
        monkey.scroll()
        pass











        
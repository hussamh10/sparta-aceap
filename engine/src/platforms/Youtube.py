import sys

from utils.util import wait; sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import constants
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
        debug(search_bar)
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

    def getIdfromUrl(self, url):
        return url.split('&')[0]


    def _getPostsResults(self):
        wait(3)
        results = self.driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
        videos = []
        for i, res in enumerate(results):
            video = dict()
            video['position'] = i
            video['name'] = res.find_element(By.ID, 'video-title').text
            url = res.find_element(By.ID, 'video-title').get_attribute('href')
            video['id'] = self.getIdfromUrl(url)
            video['elem'] = res
            videos.append(video)

        return videos




    def getPagePosts(self):
        sleep(3)
        raise Exception("Not implemented")
        videos = []
        # Names
        videos = self.driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
        debug(videos)
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
            debug(video)

        return videos

    def getPost(self, video):
        self.loadPage(video['url'])
        sleep(2)
        video['id'] = self.driver.current_url.split('v=')[1]
        return video

    def isAd(self):
        try:
            ad = self.driver.find_element(By.XPATH, '//div[@class="ad-interrupting"]')
            if ad:
                return True
            return False
        except Exception as e:
            return False
        # press  button with class ytp-ad-skip-button-modern ytp-button


    def openPost(self, already_opened=[]):
        videos = self._getPostsResults()
        for video in videos:
            if video['id'] in already_opened:
                debug('Already opened: ' + video['id'])
                continue
            video['elem'].click()
            wait(3)
            if self.isAd():
                error("IS AD")
                wait(10)
            return

    def likeable(self):
        # check if likeable
        like_buttons = self.driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
        like_button = like_buttons[0]
        # get title of button inside element
        unlikes = like_button.find_elements(By.XPATH, '//button[@title="Unlike"]')
        likes = like_button.find_elements(By.XPATH, '//button[@title="I like this"]')
        debug(f"LIKES: {len(likes)}, UNLIKES: {len(unlikes)}")
        if len(likes) > 0:
            return True
        if len(unlikes) > 0:
            return False
        error('No like buttons found')
        return True


    def likePost(self):
        videos = self._getPostsResults()
        wait(2)
        for v in range(len(videos)):
            video = videos[v]
            video['elem'].click()
            wait(3)
            if self.isAd():
                error("IS AD")
                wait(10)
            if self.likeable():
                like_buttons = self.driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
                like_button = like_buttons[0]
                like = like_button.find_elements(By.XPATH, '//button[@title="I like this"]')[0]
                like.click()
                wait(3)
                return
            else:
                debug('Already liked')
                self.driver.back()
                wait(3)



    def dislikePost(self):
        sleep(5)
        elems = self.driver.find_elements(By.XPATH, '//yt-icon[@class="style-scope ytd-toggle-button-renderer"]')
        debug(len(elems))
        elems[1].click()
        sleep(10000)

    def readComments(self):
        sleep(5)
        monkey.click()
        monkey.scroll()
        pass











        
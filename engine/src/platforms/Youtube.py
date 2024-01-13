import sys

from utils.util import wait; sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import constants
import utils.monkey as monkey
from innertube import InnerTube

class MyTube():
    def __init__(self):
        self.tube = InnerTube("WEB")

    def getVideoInfo(self, video_id):
        try:    
            data = self.tube.player(video_id=video_id)
            data = data['videoDetails']
            video = dict()
            video['id'] = video_id
            video['title'] = data['title']
            video['channel'] = data['author']
            video['length'] = data['lengthSeconds']
            video['views'] = data['viewCount']
            return video
        except Exception as e:
            error('InnerTube error')
            error(f"{e}: {video_id}")
            video = {'id': video_id, 'title': '', 'channel': '', 'length': '', 'views': ''}
            return video

    
        

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

    def loggedIn(self):
        # if not logged in, there is an "a" tag with aria-label="Sign In"
        try:
            self.driver.find_element(By.XPATH, '//a[@aria-label="Sign in"]')
            return False
        except Exception as e:
            debug('Already logged in')
            self.turnOnHistory()
            return True

    def getHomePage(self):
        home = self.driver.find_element(By.XPATH, '//a[@title="YouTube Home"]')
        home.click()
        wait(2)


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
        if "&" in url:
            url = url.split('&')[0]
        if 'v=' in url:
            url = url.split('v=')[1]
        return url


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


    def turnOnHistory(self):
        debug('Turning on history')
        self.driver.get('https://www.youtube.com/feed/history')
        wait(2)
        try:
            button = self.driver.find_element(By.XPATH, '//button[@aria-label="Turn on watch history"]')
            button.click()
            wait(1)
            button = self.driver.find_element(By.XPATH, '//button[@aria-label="Turn on"]')
            button.click()
            wait(1)
        except Exception as e:
            debug('Already turned on history')
            pass




    def getPagePosts(self, posts_n=30):
        video_elems = self.driver.find_elements(By.XPATH, '//a[@id="video-title-link"]')
        tube = MyTube()

        videos = []
        ids = []
        for i, elem in enumerate(video_elems):
            video = dict()
            video['id'] = elem.get_attribute('href').split('v=')[1]
            if video['id'] in ids:
                continue

            video['position'] = i
            video_info = tube.getVideoInfo(video['id'])
            video['title'] = video_info['title']
            video['channel'] = video_info['channel']
            video['length'] = video_info['length']
            video['views'] = video_info['views']
            info(video['title'][:30])
            ids.append(video['id'])
            videos.append(video)

        return videos



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
        tube = MyTube()
        for video in videos:
            if video['id'] in already_opened:
                debug('Already opened: ' + video['id'])
                continue
            video['elem'].click()
            wait(3)
            if self.isAd():
                error("IS AD")
                wait(10)
            video_info = tube.getVideoInfo(video['id'])
            return video_info


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
        tube = MyTube()
        wait(2)
        opened = []
        for v in range(len(videos)):
            video = videos[v]
            video['elem'].click()
            video_info = tube.getVideoInfo(video['id'])
            opened.append(video_info)
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
                return video_info, opened
            else:
                debug('Already liked')
                self.driver.back()
                wait(3)

        return None, opened



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











        
import sys

from utils.util import convertStringToNumber; sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import constants
import utils.monkey as monkey

class Twitter(Platform):

    name = 'twitter'
    url='https://www.twitter.com'
    search_url='https://twitter.com/search?q=%s&src=typed_query'
    home_url='https://twitter.com/home'
    creation_url='https://twitter.com/i/flow/signup'

    def __init__(self, user):
        super().__init__(Twitter.name, Twitter.url, user)


    def createUserGoogle(self, profile):
        self.loadPage(Twitter.creation_url)
        sleep(3)
        monkey.next()
        monkey.next()
        monkey.space()
        sleep(3)
        monkey.type(profile['email'])
        monkey.enter()
        sleep(3)
        monkey.type(profile['password'])
        monkey.enter()
        sleep(3000)
        error('Not implemented: createUserGoogle')

    def createUser(self, profile):
        # self.createUserGoogle(profile)
        self.loadPage(Twitter.creation_url)
        # sleep(3)
        # btn = self.driver.find_element(By.XPATH, '//span[text()="Create account"]')
        # btn.click()
        # sleep(3)
        # monkey.click()
        # btn = self.driver.find_element(By.XPATH, '//input[@autocomplete="name"]')
        # btn.click()
        # sleep(2)
        # fname = profile['firstname']
        # lname = profile['lastname']
        # monkey.type(f'{fname} {lname}')
        # btn = self.driver.find_element(By.XPATH, '//span[text()="Use email instead"]')
        # btn.click()
        # sleep(1)
        # monkey.back()
        # monkey.type(profile['email'])
        # monkey.next()
        # monkey.next()
        # DOB = profile['DOB'].split(',')
        # monkey.type(DOB[0])
        # monkey.next()
        # monkey.type(DOB[1])
        # monkey.next()
        # monkey.type(DOB[2])
        # sleep(1)
        # btn = self.driver.find_element(By.XPATH, '//span[text()="Next"]')
        # btn.click()
        # sleep(2)
        # btn = self.driver.find_element(By.XPATH, '//span[text()="Next"]')
        # btn.click()
        # sleep(2)
        # btn = self.driver.find_element(By.XPATH, '//span[text()="Sign up"]')
        # btn.click()
        # sleep(10)
        monkey.email()
        return True

    def isAd(self, tweet):
        ads = tweet.find_elements(By.XPATH, './/span[text()="Ad"]')
        if len(ads) > 0:
            return True
        return False

    def isLiked(self, tweet):
        likeds = tweet.find_elements(By.XPATH, './/div[@data-testid="unlike"]')
        if len(likeds) > 0:
            return True
        return False

    def likable(self):
        likeds = self.driver.find_elements(By.XPATH, '//div[@aria-label="Liked"]')
        if len(likeds) > 0:
            return False
        return True

    def likePost(self):
        sleep(3)
        tweets = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        num_tweets = len(tweets)
        opened = []       
        liked = None
        for i in range(num_tweets):
            sleep(1)
            tweets = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            if i >= len(tweets):
                self.scrollDown()
                sleep(2)
                self.scrollDown()
                tweets = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            tweet = tweets[i]
            post = self.getPost(tweet)
            post['position'] = i

            tweet_text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
            tweet_text.click()
            sleep(2)
            debug('opened')
            opened.append(post)

            if post['isAd']:
                debug('is ad')
                continue

            if self.likable():
                like = self.driver.find_element(By.XPATH, '//div[@aria-label="Like"]')
                like.click()
                liked = post.copy()
                debug('liked')
                return liked, opened

            back = self.driver.find_elements(By.XPATH, '//div[@aria-label="Back"]')
            if len(back) > 0:
                back[0].click()
            else:
                raise Exception('Could not find back button')

            sleep(2)

        return liked, opened
    
    
    def _searchTermUrl(self, term):
        search_query = Twitter.search_url % (term)
        self.loadPage(search_query)

    def _searchTermBar(self, term):
        search_bar = self._getSearchBar()
        search_bar.send_keys(term)
        sleep(3)
        search_bar.send_keys(Keys.ENTER)

    def _getSearchBar(self):
        bar = self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        sleep(1)
        return bar


    def getHomePage(self):
        self.loadPage(Twitter.home_url)

    def isFollowed(self, user):
        following = user.find_elements(By.XPATH, './/span[text()="Following"]')
        if len(following) > 0:
            return True
        return False

    def followUser(self):
        # select span with text People
        # click on it
        sleep(3)
        people = self.driver.find_element(By.XPATH, '//span[text()="People"]')
        people.click()
        sleep(2)

        users = self.driver.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')
        
        for user in users:
            username = ''
            links = user.find_elements(By.XPATH, './/a[@role="link"]')
            for link in links:
                link = link.get_attribute('href')
                twitter_header = 'https://twitter.com'
                if twitter_header in link:
                    link = link.replace(twitter_header, '')
                print(link)
                if link.count('/') == 1:
                    username = link.replace('/', '')

            if self.isFollowed(user):
                debug(f'Already followed {username}')
                continue

            follow_button = user.find_element(By.XPATH, './/span[text()="Follow"]')
            follow_button.click()
            debug(f'Followed {username}')
            return username

        raise Exception('Could not find user to follow')


    def getPost(self, tweet):
        post = dict()
        links = tweet.find_elements(By.XPATH, './/a[@role="link"]')
        for link in links:
            link = link.get_attribute('href')
            if '/analytics' in link and 'status' in link:
                if 'id' not in post:
                    post['id'] = '/'.join(link.split('/')[:-1])
                if 'username' not in post:
                    post['username'] = link.split('/')[-4]

        try:
            post['text'] = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        except:
            post['text'] = ''
            error('Could not find text')
        post['isAd'] = self.isAd(tweet)

        group = tweet.find_element(By.XPATH, './/div[@role="group"]')
        group = group.text.split('\n')

        if len(group) != 4:
            group = tweet.find_element(By.XPATH, './/div[@role="group"]')
            group = group.text.split('\n')

        debug(post['id'])           
        replies = tweet.find_element(By.XPATH, './/div[@data-testid="reply"]').text
        post['comments'] = convertStringToNumber(replies)
        
        retweets = tweet.find_element(By.XPATH, './/div[@data-testid="retweet"]').text
        post['retweets'] = convertStringToNumber(retweets)

        _liked = self.isLiked(tweet)
        if _liked:
            likes = tweet.find_element(By.XPATH, './/div[@data-testid="unlike"]').text
        else:
            likes = tweet.find_element(By.XPATH, './/div[@data-testid="like"]').text
        post['likes'] = convertStringToNumber(likes)

        post['views'] = convertStringToNumber(group[-1])
        
        #has video
        post['attachment'] = 'none'

        videos = tweet.find_elements(By.XPATH, './/div[@data-testid="videoComponent"]')
        if len(videos) > 0:
            post['attachment'] = 'video'

        images = tweet.find_elements(By.XPATH, './/div[@aria-label="Image"]')
        if len(images) > 0:
            post['attachment'] = 'image'

        external_links = tweet.find_elements(By.XPATH, './/a[@rel="noopener"]')
        if len(external_links) > 0:
            external_link = external_links[0].get_attribute('href')
            post['attachment'] = 'external'
            post['external_link'] = external_link
        
        print(post)
        return post

    def getPagePosts(self, n):
        tweets = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        posts = []
        for i, tweet in enumerate(tweets):
            post = self.getPost(tweet)
            post['position'] = i
            posts.append(post)

        return posts

    def isJoined(self, l):
        joined = l.find_elements(By.XPATH, './/div[@aria-label="Following"]')
        if len(joined) > 0:
            return True
        return False


    def joinCommunity(self):
        sleep(3)
        people = self.driver.find_elements(By.XPATH, '//span[text()="Lists"]')[1]
        people.click()
        sleep(2)
        input('whats happened')

        lists = self.driver.find_elements(By.XPATH, '//div[@data-testid="listCell"]')
        
        for l in lists:
            text = l.text.split('\n')
            for i in text:
                debug(i)

            listname = text[0]

            if self.isJoined(l):
                debug(f'Already followed {listname}')
                continue

            join_button = l.find_element(By.XPATH, './/div[@aria-label="Follow"]')
            join_button.click()
            debug(f'Followed {listname}')
            return listname

        raise Exception('Could not find list to join')
        pass
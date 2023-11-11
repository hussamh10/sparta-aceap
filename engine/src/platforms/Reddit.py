from abc import abstractclassmethod
import sys
from tkinter import W
sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import pickle as pkl
from datetime import datetime
import pandas as pd
from constants import pprint
import constants
import utils.monkey as monkey

import praw


import constants
from selenium.webdriver.common.action_chains import ActionChains

# Get reddit posts using PRAW


class RedditPRAW():

    def __init__(self):
        self.reddit_client = praw.Reddit(
            client_id="iG8E0avK8fPxRQ",
            client_secret="2D1FD6YhH0RjTKWaRJmV3ChW_Bw",
            user_agent="sparta_bot",
        )
        
    def getPost(self, id):
        res = dict()
        submission = self.reddit_client.submission(id)
        res['id'] = id
        res['title'] = submission.title
        res['author'] = submission.author.name
        res['subreddit'] = submission.subreddit.display_name
        res['num_comments'] = submission.num_comments
        res['score'] = submission.score
        res['selftext'] = submission.selftext
        res['url'] = submission.url

        return res


class Reddit(Platform):
    name = 'reddit'
    url='https://www.reddit.com'
    search_url='https://www.reddit.com/search/?q=%s'
    creation_url='https://www.reddit.com/register/'

    def __init__(self, userId):
        super().__init__(Reddit.name, Reddit.url, userId)

    def createUser(self, profile):
        self.loadPage(Reddit.creation_url)
        sleep(3)
        monkey.click()
        btn = self.driver.find_element(By.XPATH, '//input[@name="email"]')
        btn.click()
        debug('clicking email')
        sleep(1)
        monkey.type(f'{profile["email"]}')
        debug('typing email')
        sleep(1)
        btn = self.driver.find_element(By.XPATH, '//button[@data-step="email"]')
        btn.click()
        sleep(3)
        btn = self.driver.find_element(By.XPATH, '//input[@name="username"]')
        btn.click()
        debug('clicking username')
        monkey.type(f'{profile["username"]}')
        debug('typing username')
        monkey.next()
        monkey.type(f'{profile["password"]}')
        debug('typing password')
        monkey.captcha()
        error('Click on create account button -- Press enter to continue')
        input()
        return True

    def _searchTermUrl(self, term):
        search_query = Reddit.search_url % (term)
        self.loadPage(search_query)

    def loggedIn(self):
        try:
            self.driver.find_element(By.XPATH, '//a[text()="Log In"]').click()
            return False
        except:
            return True

    def _searchTermBar(self, term):
        sleep(2.2)
        search_bar = self._getSearchBar()
        print(search_bar)
        search_bar.send_keys(term)
        sleep(1)
        search_bar.send_keys(Keys.ENTER)

    def _getSearchBar(self):
        # return self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        return self.driver.find_element(By.ID, "header-search-bar")

    def _getPostsResults(self):
        results = self.driver.find_element(By.XPATH, "//div[@data-testid='posts-list']")
        results = results.find_elements(By.XPATH, "//div[@data-testid='post-container']")
        
        posts = []
        for i, result in enumerate(results):
            post = dict()
            post['position'] = i
            post['id'] = result.get_attribute('id')
            post['elem'] = result
            posts.append(post)

        return posts

        # for post in posts:
        #     post['elem'].click()
        #     sleep(1000)

        # results = results.text
        # lines = results.split('\n')

        # c = []
        # data = []
        # i = 0
        # for line in lines:
        #     c.append(line)
        #     i+=1 
        #     if i % 4 == 0:
        #         data.append(c)
        #         c = []

        # subreddits = dict()
        # i = 1
        # for c in data:
        #     subreddits[c[0]] = {'Rank': i, 'Members': c[1], 'Description': c[2], 'Joined': c[3]}
        #     status = c[3]
        #     if status == 'Join':
        #         subreddits[c[0]]['Joined'] = False
        #     else:
        #         subreddits[c[0]]['Joined'] = True
        #     i += 1

        # results = {'subreddits': subreddits}
        # return results

    def _getCommunityResults(self):
        results = self.driver.find_element(By.XPATH, "//div[@data-testid='communities-list']")
        results = results.text
        lines = results.split('\n')

        c = []
        data = []
        i = 0
        for line in lines:
            c.append(line)
            i+=1 
            if i % 4 == 0:
                data.append(c)
                c = []

        subreddits = dict()
        i = 1
        for c in data:
            subreddits[c[0]] = {'Rank': i, 'Members': c[1], 'Description': c[2], 'Joined': c[3]}
            status = c[3]
            if status == 'Join':
                subreddits[c[0]]['Joined'] = False
            else:
                subreddits[c[0]]['Joined'] = True
            i += 1

        results = {'subreddits': subreddits}
        return results

    def _joinNthSubreddit(self, N=0):
        sleep(1)
        profiles = self.driver.find_elements(By.XPATH, '//a[@data-testid="subreddit-link"]')
        for i in profiles:
            if 'Joined' not in i.text:
                if 'Join' in i.text:
                    community = i.get_attribute('href')[:-1].split('/')[-1]
                    join = i.find_element(By.XPATH, '//button[text()="Join"]')
                    debug(community)
                    join.click()
                    break
        return community
        # joined = len(self.driver.find_elements(By.XPATH, '//span[text()="Joined"]'))
        # debug(joined)
        # subreddits = self.driver.find_elements(By.XPATH, '//button[text()="Join"]')
        # subreddit = subreddits[N]
        # debug(subreddits)
        # names = self.driver.find_elements(By.TAG_NAME, 'h6')
        # name = names[N+joined].text
        # subreddit.click()
        # return name

    def _getPeopleResults(self):
        results = self.driver.find_element(By.XPATH, "//div[@data-testid='people-list']")
        results = results.text
        lines = results.split('\n')
        c = []
        data = []
        i = 0
        for line in lines:
            c.append(line)
            i+=1 
            if i % 4 == 0:
                data.append(c)
                c = []

        people = dict()
        i = 1
        for c in data:
            people[c[0]] = {'Rank': i, 'Karma': c[1], 'Description': c[2], 'Followed': c[3]}
            status = c[3]
            if status == 'Follow':
                people[c[0]]['Followed'] = False
            else:
                people[c[0]]['Followed'] = True
            i += 1

        results = {'people': people}
        return results

    def loadWebsite(self):
        super().loadWebsite()
        # check if aria-label='Close' is present
        # if it is, click it
        # if not, continue

        sleep(5)
        if len(self.driver.find_elements(By.XPATH, '//button[@aria-label="Close"]')):
            self.driver.find_element(By.XPATH, '//button[@aria-label="Close"]')




    def _joinNthUser(self, N=0):
        sleep(1)
        profiles = self.driver.find_elements(By.XPATH, '//a[@data-testid="profile-link"]')
        for i in profiles:
            if 'Following' not in i.text:
                if 'Follow' in i.text:
                    user = i.get_attribute('href')
                    follow = i.find_element(By.XPATH, '//button[text()="Follow"]')
                    debug(user)
                    follow.click()
                    break

        sleep(3000)
        followed = len(self.driver.find_elements(By.XPATH, '//span[text()="Following"]'))
        debug(followed)
        people = self.driver.find_elements(By.XPATH, '//button[text()="Follow"]')
        user = people[N]
        debug(followed)
        names = self.driver.find_elements(By.TAG_NAME, 'h6')
        for name in names:
            debug(name.text)
        name = names[N+followed].text
        debug(name)
        # user.click()
        return name

    def followUser(self):
        error('ERROR')
        sleep(1)
        people = self.driver.find_element(By.XPATH, '//button[text()="People"]')
        people.click()
        sleep(2)

        results = self._getPeopleResults()
        user = self._joinNthUser(0)
        return user
        # return community
        
    def joinCommunity(self):
        sleep(1)
        communities = self.driver.find_element(By.XPATH, '//button[text()="Communities"]')
        communities.click()
        sleep(2)
        results = self._getCommunityResults()

        community = self._joinNthSubreddit(0)
        return community

    def getHomePage(self):
        sleep(1)
        home = self.driver.find_element(By.XPATH, '//a[@aria-label="Home"]')
        home.click()

    def _getPostId(self, links):
        ids = []
        for link in links:
            link = link.split('/comments/')[1].split('/')[0]
            ids.append(link)
        return ids

    def getPostInfo(self, id):
        api = RedditPRAW()
        try:
            post = api.getPost(id)
        except:
            error('ERROR GETTING POST FROM PRAW')
            post = {'id': id, 'title': '', 'author': '', 'subreddit': '', 'num_comments': '', 'score': '', 'selftext': '', 'url': ''}
        return post

    def getPagePosts(self, n=10):
        pprint('Getting posts from page')
        sleep(1)
        posts = self.driver.find_elements(By.XPATH, '//div[@data-testid="post-container"]')

        posts_urls = []

        for post in posts:
            try:
                url = post.find_element(By.XPATH, './/a[@data-click-id="body"]').get_attribute('href')           
                posts_urls.append(url)
            except:
                pass

        posts_ids = self._getPostId(posts_urls)
        posts = []

        api = RedditPRAW()

        pprint('Getting posts from PRAW')
        i = 0
        for post in posts_ids[:n]:
            pprint(post)
            try:
                post = api.getPost(post)
            except:
                error('ERROR GETTING POST FROM PRAW')
                pass
            post['position'] = i
            posts.append(post)
            i += 1
        # self.saveResults(posts, 'homepage_posts')

        return posts

    #TODO CHANGE THIS TO POST TO LOCATION?
    def openPost(self, already_opened=[]):
        sleep(2)
        posts = self.driver.find_element(By.XPATH, '//button[text()="Posts"]')
        posts.click()
        sleep(1)
        posts = self._getPostsResults()
        
        for post in posts:
            sleep(0.3)
            if post['id'] in already_opened:
                debug('Already opened: ' + post['id'])
            else:
                post['elem'].click()
                opened = post
                return opened
        sleep(1)

    def likePost(self):
        posts = self.driver.find_element(By.XPATH, '//button[text()="Posts"]')
        posts.click()
        sleep(1)
        posts = self._getPostsResults()
        opened = []
        
        for i, post in enumerate(posts):
            sleep(2)
            post['elem'].click()
            post_info = self.getPostInfo(post['id'])
            post_info['position'] = i
            opened.append(post_info)
            sleep(2)
            dislike = self.driver.find_element(By.XPATH, '//button[@aria-label="downvote"]')
            like = self.driver.find_element(By.XPATH, '//button[@aria-label="upvote"]')
            if dislike.get_attribute('aria-pressed') == 'true':
                debug('already disliked')
                close = self.driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                close.click()
            elif like.get_attribute('aria-pressed') == 'true':
                debug('already liked')
                close = self.driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                close.click()
            else:
                like.click()
                debug(f"liked post {post['id']}")
                return post_info, opened
        
        error('ERROR LIKING POST')
        return None, opened

    def dislikePost(self):
        posts = self.driver.find_element(By.XPATH, '//button[text()="Posts"]')
        posts.click()
        sleep(1)
        posts = self._getPostsResults()
        opened = []
        
        for i, post in enumerate(posts):
            sleep(2)
            post['elem'].click()
            post_info = self.getPostInfo(post['id'])
            post_info['position'] = i
            opened.append(post_info)
            sleep(2)
            dislike = self.driver.find_element(By.XPATH, '//button[@aria-label="downvote"]')
            like = self.driver.find_element(By.XPATH, '//button[@aria-label="upvote"]')
            if dislike.get_attribute('aria-pressed') == 'true':
                debug('already disliked')
                close = self.driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                close.click()
            elif like.get_attribute('aria-pressed') == 'true':
                debug('already liked')
                close = self.driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                close.click()
            else:
                dislike.click()
                debug(f"disliked post {post['id']}")
                return post_info, opened
        
        error('ERROR LIKING POST')
        return None, opened


    def comment(self, content, already_commented):
        posts = self.driver.find_element(By.XPATH, '//button[text()="Posts"]')
        posts.click()
        sleep(3)
        posts = self._getPostsResults()

        for post in posts:
            if post['id'] in already_commented:
                debug('Already commented: ' + post['id'])
            else:
                post['elem'].click()
                sleep(3)
                comment = self.driver.find_element(By.XPATH, '//div[@role="textbox"]')
                comment.send_keys(content)
                print(content)
                super().scrollDown()
                sleep(3)
                submit = self.driver.find_element(By.XPATH, '//button[text()="Comment"]')
                submit.click()
                debug(f"commented on post {post['id']}")
                return post

        error('ERROR COMMENTING POST')
        return None

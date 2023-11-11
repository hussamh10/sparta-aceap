import sqlite3
import sys
from time import sleep
from unittest import findTestCases
from users.User import User
from platforms.Reddit import Reddit
from uuid import uuid4 as uid
import pandas as pd

from utils.log import debug, error, pprint, info
sys.path.append('..')

class RedditUser(User):
    def __init__(self):
        pass

    def createUser(self):
        self.platform = Reddit(self.info['id'])
        super().createUser()

    def loadUser(self, id="", username=""):
        self._loadInfo(id, username)
        self.platform = Reddit(self.info['id'])
        super().loadUser()


    def joinCommunity(self, community, search):
        """
        Joins the first (joinable) subreddit after search
        """
        self.addState('join', community, '')
        if search:
            sleep(2)
            self.platform.searchTerm(community)
            debug('Term searched')

        else:
            error('TODO: non-searched join')

        self.platform.joinCommunity()

    def getPosts(self, scrolls):
        """
        Scrolls down the page and gets all the posts
        """
        
        for i in range(scrolls):
            self.platform.scrollDown()
            sleep(3)

        posts = self.platform.getPagePosts()
        print(posts)
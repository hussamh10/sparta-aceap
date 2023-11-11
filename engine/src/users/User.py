from abc import abstractclassmethod
from time import sleep, time
import pandas as pd
import sqlite3
import sys
from unittest import findTestCases
from uuid import uuid4 as uid
import pickle as pkl
import os
from constants import *

from utils.log import debug, info, error

sys.path.append('..')


class Observation():
    def __init__(self):
        pass

    # def dumpHTML(self, html):
    #     self.htmlid = str(uid())
    #     # save the html of the page
    #     pkl.dump(html, open(self.htmlid + '.html', 'wb'))

class Signal():
    def __init__(self, action, content, user, platform, info, experiment):
        self.id = str(uid())
        self.action = action
        self.content = content
        self.time = time()
        self.info = info
        self.user = user
        self.platform = platform
        self.experiment = experiment
        self.save()

    def save(self):
        # TODO: create table
        conn = sqlite3.connect('aceap.db')
        c = conn.cursor()
        c.execute("INSERT INTO signals VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            self.id, self.action, self.content, self.time, self.user, self.platform, self.info, self.experiment
        ))
        conn.commit()
        conn.close()


# state = {'num': 0, 'action': '', 'topic': '', 'info': '', 'time': 0}

class User:
    def __init__(self, platform):
        self.Platform = platform
        self.signals = []
        pass

    def addSignal(self, action, content, info='', experiment=''):
        signal = Signal(
            action = action,
            content = content,
            info = info,
            user = self.info['id'],
            platform = self.info['platform'], 
            experiment = experiment
        )
        debug('Signal: %s, %s, %s, %s' % (signal.action, signal.content, signal.info, signal.experiment))
        self.signals.append(signal.id)

    def create(self, platform, firstname, lastname,
        email, username, password, phone, DOB, gender):
        
        if self._userExists(username, platform):
            error('User already exists')
            return
        self.info = dict()
        self.info["id"] = str(uid())
        self.info["platform"] = platform
        self.info["firstname"] = firstname
        self.info["lastname"] = lastname
        self.info["email"] = email
        self.info["username"] = username
        self.info["password"] = password
        self.info["phone"] = phone
        self.info["DOB"] = DOB
        self.info["gender"] = gender
        self.createUser()

    def createUser(self):
        self.platform = self.Platform(self.info['id'])

        self.platform.loadBrowser()
        self.platform.loadWebsite()
        if self.platform.createUser(self.info):
            debug('User created')
        else:
            raise Exception('User not created')
        
        self.save()
        debug('User saved')
        self.addSignal('create', 'user', '')

    def loadUser(self, id="", username=""):
        self._loadInfo(id, username)
        debug(self.info)
        if self.info['platform'] != self.Platform.__name__:
            raise Exception('Platform mismatch')
        self.platform = self.Platform(self.info['id'])
        self.platform.loadBrowser()
        self.platform.loadWebsite()

        error("IMPLEMENT LOGIN CHECK")
        # if self.platform.loggedIn():
        #     info('User logged in')
        # else:
        #     raise Exception('User not logged in')

    def _loadSignals(self):
        # TODO load signals
        pass

    def test(self):
        self.platform.loadWebsite()
        print(self.platform)
  
    def _loadInfo(self, id="", username=""):
        if username != "":
            self.info = self._getUserByUsername(username)
            return
        if id != "":
            raise Exception("Not implemented")
            self.info = self._getUserById(id)
            return
        raise Exception("No id or username provided")
        
    def _userExists(self, username, platform):
        conn = sqlite3.connect('aceap.db')
        c = conn.cursor()
        df = pd.read_sql_query("SELECT * FROM profiles WHERE username = '%s' AND platform = '%s'" % (username, platform), conn)
        conn.close()
        return len(df) > 0

        
    def _getUserByUsername(self, username):
        conn = sqlite3.connect('aceap.db')
        c = conn.cursor()
        df = pd.read_sql_query("SELECT * FROM profiles WHERE username = '%s'" % (username), conn)
        conn.close()
        if len(df) == 0:
            raise Exception('User not found')
        return df.to_dict('index')[0]
  
    def followUser(self, topic, experiment):
        """
        Searches and follows the first user
        TODO: Search alternative
        """ 
        sleep(2)
        self.search(topic)
        debug('Term searched')
        user = self.platform.followUser()
        self.addSignal('follow-user', user, info=f'searched-{topic}', experiment=experiment)
        sleep(3)
        pass
  

    def getOpenedPosts(self):
        conn = sqlite3.connect('aceap.db')
        df = pd.read_sql_query("SELECT * FROM signals WHERE action = 'open-post' AND user = '%s'" % (self.info['id']), conn)
        conn.close()
        posts = list(df['content'])
        return posts

    def openPost(self, topic, experiment):
        """
        Searches and likes the first post
        """
        sleep(2)
        self.search(topic)
        debug('Term searched')
        opened_posts = self.getOpenedPosts()
        print(opened_posts)
        post = self.platform.openPost(already_opened=opened_posts)
        self.addSignal('open-post', post['id'], info=f'searched-{topic}', experiment=experiment)


    def readComments(self, topic, experiment):
        debug("searching")
        sleep(2)
        self.search(topic)
        debug('Term searched')
        post, opened = self.platform.readComments()

        print(opened)
        self.addPosts(opened, str(uid()))

        for open in opened:
            self.addSignal('open-post', open['id'], info=f'searched-{topic}', experiment=experiment)

        if post != None:
            self.addSignal('read-comments', post['id'], info=f'searched-{topic}', experiment=experiment)

    def likePost(self, topic, experiment):
        """
        TODO: like disliked posts?
        Searches and likes the first unliked post
        """
        debug("searching")
        sleep(2)
        self.search(topic)
        debug('Term searched')
        post, opened = self.platform.likePost()

        print(opened)
        self.addPosts(opened, str(uid()))

        for open in opened:
            self.addSignal('open-post', open['id'], info=f'searched-{topic}', experiment=experiment)

        if post != None:
            self.addSignal('like-post', post['id'], info=f'searched-{topic}', experiment=experiment)


    def dislikePost(self, topic, experiment):
        """
        TODO: dislike liked posts?
        Searches and dislikes the first post
        """
        sleep(2)
        self.search(topic)
        debug('Term searched')
        post, opened = self.platform.dislikePost()

        for open in opened:
            self.addSignal('open-post', open['id'], info=f'searched-{topic}', experiment=experiment)

        if post != None:
             self.addSignal('dislike-post', post['id'], info=f'searched-{topic}', experiment=experiment)

  
    def joinCommunity(self, topic, experiment):
        """
        Searches and joins the first group
        TODO: Not join private groups
        TODO if search
        """
        print(self.platform)
        sleep(2)
        self.search(topic)
        debug('Term searched')
        community = self.platform.joinCommunity()
        self.addCommunities([community], str(uid()))
        self.addSignal('join-community', community['group_id'], info=f'searched-{topic}', experiment=experiment)
        pass

    def addCommunities(self, community, id):
        conn = sqlite3.connect("aceap.db")
        table = f'{self.info["platform"]}-communities'
        df = pd.DataFrame(community)
        print(df)
        df['record-id'] = id
        df.to_sql(table, conn, if_exists="append")
        conn.close()

    def addPosts(self, posts, id):
        conn = sqlite3.connect("aceap.db")
        table = f'{self.info["platform"]}-posts'
        df = pd.DataFrame(posts)
        print(df)
        df['record-id'] = id
        df.to_sql(table, conn, if_exists="append")
        conn.close()

    def recordHome(self, experiment, scrolls=5, posts_n=10):
        self.goHome()
        sleep(2)
        posts = self.getPosts(scrolls, posts_n)
        id = str(uid())
        self.addSignal('record', 'home', info=f'{id}', experiment=experiment)
        self.addPosts(posts, id)

    def goHome(self):
        self.platform.getHomePage()
        sleep(3.2)

    def save(self):
        # save profile to sqlite table
        conn = sqlite3.connect("aceap.db")
        df = pd.DataFrame.from_dict(self.info, orient='index').T
        df = df.set_index('id')
        df.to_sql("profiles", conn, if_exists="append")
        conn.close()

    def getPosts(self, scrolls, posts_n=10):
        """
        Scrolls down the page and gets all the posts
        """
        #CHANGE
        scrolls = scrolls
        
        for i in range(scrolls):
            self.platform.scrollDown()
            sleep(2)

        posts = self.platform.getPagePosts(posts_n)
        return posts

    def search(self, key):
        self.platform.searchTerm(key)
        self.addSignal('search', key, '')


    # def getReadCommentPosts(self):
    #     conn = sqlite3.connect('aceap.db')
    #     df = pd.read_sql_query("SELECT * FROM signals WHERE action = 'read-comments' AND user = '%s'" % (self.info['id']), conn)
    #     conn.close()
    #     posts = list(df['content'])
    #     return posts

    def getCommentedPosts(self):
        conn = sqlite3.connect('aceap.db')
        df = pd.read_sql_query("SELECT * FROM signals WHERE action = 'comment' AND user = '%s'" % (self.info['id']), conn)
        conn.close()
        posts = list(df['content'])
        return posts

    def comment(self, topic, content, experiment):
        """
        Searches and comments the first post
        """
        sleep(2)
        self.search(topic)
        debug('Term searched')
        already_commented = self.getCommentedPosts()
        post = self.platform.comment(content, already_commented=already_commented)

        if post != None:
             self.addSignal('open-post', post['id'], info=f'searched-{topic}', experiment=experiment)
             self.addSignal('comment', post['id'], info=f'searched-{topic}, comment: {content}', experiment=experiment)

    def scrollDown(self, num=1):
        for i in range(num):
            self.platform.scrollDown()

    def quit(self):
        self.platform.quit()
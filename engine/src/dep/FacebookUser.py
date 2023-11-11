import sqlite3
import sys
from time import sleep
from users.User import User
from platforms.Facebook import Facebook
from uuid import uuid4 as uid
import pandas as pd

from utils.log import debug, error, pprint, info
sys.path.append('..')

class FacebookUser(User):
    def __init__(self):
        pass

    def createUser(self):
        self.platform = Facebook(self.info['id'])
        super().createUser()

    def loadUser(self, id="", username=""):
        self._loadInfo(id, username)
        self.platform = Facebook(self.info['id'])
        super().loadUser()

    def joinCommunity(self, community):
        """
        Searches and joins the first facebook group
        TODO: Not join private groups
        """
        sleep(2)
        self.platform.searchTerm(community)
        debug('Term searched')
        self.platform.joinCommunity()

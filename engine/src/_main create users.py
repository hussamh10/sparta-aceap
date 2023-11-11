from abc import ABC, abstractclassmethod, abstractmethod
from re import A
from Experiment import Experiment
from users.User import User
# from users.RedditUser import RedditUser
# from users.FacebookUser import FacebookUser
import constants
from time import sleep
from platforms.Twitter import Twitter
# from platforms.Reddit import Reddit
# from platforms.Facebook import Facebook
import numpy as np
import utils.monkey as monkey
from utils.log import debug
import sqlite3
from constants import *
import pickle as pkl


if __name__ == '__main__':
    ids = list(range(1000, 1011))
    for i in ids:
        username = f'aceap{i}'
        email = f'aceap{i}@gmail.com'

        user = User(Twitter)

        user.create('Twitter',
            'Ahmed',
            'Hussnain',
            email,
            username,
            'hehahahahoho',
            '3199349328',
            'Dec,19,1995',
            'M')
from abc import ABC, abstractclassmethod, abstractmethod
import sqlite3
from Experiment import Experiment
from users.User import User
from time import sleep
from platforms.Facebook import Facebook
from utils.log import debug
from constants import *
import pandas as pd


EXPERIMENT='facebook-test'
# user = User(Facebook)
# user.create('Facebook', 'Ahmed', 'Aceap',
#     'aceap0001@gmail.com', 'aceap0001@gmail.com', 'hehehahahoho', '3199309438', '18/12/1995', 'Male')

N = 1
intention = 'nothing'
belief = 'epl'
username = 'aceap0001@gmail.com'

# debug(f'{intention} {belief} {username}')
exp = Experiment(intention, belief, username, Facebook, '', EXPERIMENT, N=N)
exp.runExperiment()
# sleep(2)
# exp.quit()
# sleep(3)


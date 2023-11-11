from abc import ABC, abstractclassmethod, abstractmethod
import sqlite3
from Experiment import Experiment
from users.User import User
from time import sleep
from platforms.Reddit import Reddit
from utils.log import debug
from constants import *
import pandas as pd

EXPERIMENT='pilotv1-gaming-day-99'

def already_joined(username):
    conn = sqlite3.connect('aceap.db')
    df = pd.read_sql_query("SELECT * FROM profiles WHERE username = '%s'" % (username), conn)
    userid = list(df['id'])[0]
    df = pd.read_sql_query("SELECT * FROM signals WHERE action = 'join' AND user = '%s'" % (userid), conn)
    conn.close()
    return len(df) > 0

def already_recorded(username):
    conn = sqlite3.connect('aceap.db')
    df = pd.read_sql_query("SELECT * FROM profiles WHERE username = '%s'" % (username), conn)
    userid = list(df['id'])[0]
    df = pd.read_sql_query("SELECT * FROM signals WHERE action = 'record' AND user = '%s'" % (userid), conn)
    conn.close()
    return len(df) > 0
   

def controlJoin(username, intention, belief, N):
    debug(f'no join {username}')
    exp = Experiment('nothing', 'nothing', username, Reddit, '', EXPERIMENT)
    exp.runExperiment()
    sleep(2)
    exp.quit()
    sleep(3)

def joinCommunity(username, intention, belief, N):
    debug(f'{intention} {belief} {username}')
    exp = Experiment(intention, belief, username, Reddit, '', EXPERIMENT, N=N)
    exp.runExperiment()
    sleep(2)
    exp.quit()
    sleep(3)

def recordHome(users):
    for username in users['treatment'] + users['control']:
        debug(f'Recording Initial Home: {username}')
        # if username in ['aceap1001', 'aceap1002', 'aceap1003', 'aceap1000', 'aceap1005', 'aceap1006', 'aceap1007', 'aceap1008', 'aceap1009']:
        #     debug(f'Already exists: {username}')
        #     continue
        exp = Experiment('nothing', 'record-only', username, Reddit, '', EXPERIMENT)
        exp.runExperiment()
        sleep(2)
        exp.quit()
        sleep(3)

def recordInitialHome(users):
    for username in users['treatment'] + users['control']:
        debug(f'Recording Initial Home: {username}')
        if already_recorded(username):
            debug(f'Already exists: {username}')
            continue
        exp = Experiment('nothing', 'record-only', username, Reddit, '', EXPERIMENT)
        exp.runExperiment()
        sleep(2)
        exp.quit()
        sleep(3)


if __name__ == '__main__':
    # Tusers = []
    Tusers = ['aceap1001', 'aceap1002', 'aceap1003', 'aceap1000', 'aceap1005']
    Cusers = ['aceap1006', 'aceap1007', 'aceap1008', 'aceap1009', 'aceap1010']

    intention = 'nothing'
    belief = 'gaming'

    users = dict()
    users['treatment'] = Tusers
    users['control'] = Cusers

    recordInitialHome(users)

    for user in users['treatment']:
        joinCommunity(user, intention, belief, N=5)

    for user in users['control']:
        controlJoin(user, intention, belief, N=5)


    recordHome(users)
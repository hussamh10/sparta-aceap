from abc import ABC, abstractclassmethod, abstractmethod
from re import A
from Experiment import Experiment
from users.User import User
# from users.RedditUser import RedditUser
# from users.FacebookUser import FacebookUser
import constants
from time import sleep
from platforms.Twitter import Twitter
from platforms.Reddit import Reddit
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

        user = User(Reddit)

        user.create('Reddit',
            'Ahmed',
            'Hussnain',
            email,
            username,
            'hehahahahoho',
            '3199349328',
            'Dec,19,1995',
            'M')

    


    # user = User(Reddit)
    # email = 'aceap1001@gmail.com'


    # user.create('Reddit',
    #     'Ahmed',
    #     'Hussnain',
    #     email,
    #     username,
    #     'hehahahahoho',
    #     '3199349328',
    #     'Dec,19,1995',
    #     'M')

    # debug('Created User')
    # # sleep(4)

    # username = 'aceap1001'
    # exp = Experiment('nothing', 'record-only', username, Reddit, '')
    # exp.runExperiment()
    # debug('END experiment 1')

if __name__ == '__main0__':
    results = pkl.load(open('temp.pkl', 'rb'))
    breaks = ['Add friend', 'Cancel request', '']
    print(results)


if __name__ == '__main__1':
    exp = Experiment('nothing', 'epl', 'aceap0002this', Reddit, '')
    exp.runExperiment()
    debug('END experiment 1')
    sleep(3)
    exp = Experiment('nothing', 'epl', 'aceap00013name', Reddit, '', 'HAHAHAHHAA this cannot be happening!!')
    exp.runExperiment()
    debug('END experiment 2')

    # exp = Experiment('follow', 'nfl', 'aceap00013name', Reddit, '')
    # exp.runExperiment()
    # debug('END experiment 2')

if __name__ == '__main_2_':
    user = User(Reddit)

    username = 'aceap0002this'
    email = 'aceap0002@gmail.com'

    # user.create('Reddit',
    #     'Ahmed',
    #     'Hussain',
    #     email,
    #     username,
    #     'hehahahahoho',
    #     '3199309328',
    #     'Dec,19,1995',
    #     'M')
    user.loadUser(username=username)
    user.followUser('nfl')



if __name__ == '__main__1':
    user = User(Reddit)

    username = 'aceap0002_4'
    email = 'aceap0002+4@gmail.com'

    user.create('Reddit',
        'Ahmed',
        'Hussain',
        email,
        username,
        'hehahahahoho',
        '3199309328',
        'Dec,19,1995',
        'M')
    user.loadUser(username=username)

    # user.test()
    # sleep(9993)
    # user.getPosts(scrolls=3)
    # sleep(3999)
    # user.openPost('vrwv8s')
    sleep(2)
    user.followUser('nfl')
    debug('END')
    sleep(10000)



    # user.createUser()
    # f = Youtube(user)
    # f.loadBrowser()
    # f.loadWebsite()
    # f.searchTerm('epl')
    # videos = f.getPagePosts()
    # video = videos[0]
    # f.openPost(video)
    # f.followUser({'url': 'https://www.youtube.com/channel/UCJ5v_MCY6GNUBTO8-D3XoAg'})
    # sleep(10000)
    # # f.createUser(profile)

    # # f = Reddit(user)
    # # f.loadBrowser()
    # # sleep(2)
    # # f.loadWebsite()
    # # sleep(4)
    # # # f.searchTerm(user.topic, bar=True)
    # # # f.joinChannel(save=False)
    # # # f.scrollDown()
    # # # sleep(20)
    # # # # posts = f.getPagePosts()
    # # # for post in posts:
    # # #     for item in post:
    # # #         print(f'{item}: {post[item]}')

    # # post = 'vrwv8s'

    # # f.openPost(post)
    # # f.stayOnPost()S
    # # f.dislikePost()






    # run = True

    # while(run):
    #     a = input()
    #     if a == 'q':
    #         run = False

    # f.close()

    # # f.likePost()
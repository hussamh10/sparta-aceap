import json
import os
import pickle as pkl
from time import time
import pandas as pd


import sqlite3 as sql
from account_creation.GoogleAccounts import GoogleAccount
from account_creation.GoogleWorkspace import GoogleWorkspace
from constants import getPlatform
from experiment.Trial import Trial
from utils.log import debug, error, info, log
from utils import shuffleIP as IP

class Logger():
    def __init__(self, path, platform, experiment_id):
        self.file_name = os.path.join(path, platform, 'log.db')
        if not os.path.exists(os.path.join(path, platform)):
            os.makedirs(os.path.join(path, platform))
        if not os.path.isfile(self.file_name):
            db = sql.connect(self.file_name)
            query = '''CREATE TABLE "logs" (
                "user"	TEXT,
                "platform"	TEXT,
                "time"	REAL,
                "tick"	INTEGER,
                "action"	TEXT,
                "topic"	TEXT,
                "dump"	TEXT,
                "screenshot"	TEXT
            )'''
            db.execute(query)
            db.commit()
            db.close()
    
    def log(self, user, platform, tick, action, topic, dump, screenshot=''):
        db = sql.connect(self.file_name)
        t = time()
        query = f'''INSERT INTO logs VALUES (
            '{user}',
            '{platform}',
            {t},
            {tick},
            '{action}',
            '{topic}',
            '{dump}', 
            '{screenshot}'
        )'''
        db.execute(query)
        db.commit()
        db.close()

    def get_observation(self, user, tick):   
        db = sql.connect(self.file_name)
        df = pd.read_sql_query(f"SELECT * FROM logs WHERE user='{user}' AND action='observe' AND tick={tick}", db)
        df = df.to_dict('records')
        observations = []
        for record in df:
            try:
                obs = record['dump']
                obs = pd.read_pickle(obs)
                if obs == []:
                    continue
                observations.append(obs)
            except Exception as e:
                error(e)
                continue
        
        # return the observation with the most data
        try:
            obs = max(observations, key=lambda x: len(x))
        except Exception as e:
            error(e)
            obs = []
        return obs

    def get_treatments(self, user):
        db = sql.connect(self.file_name)
        df = pd.read_sql_query(f"SELECT * FROM logs WHERE user='{user}' AND action!='observe'", db)
        df = df.drop_duplicates(subset=['tick'])
        df = df.set_index('tick')
        treatments = df.to_dict('index')
        for treatment in treatments:
            dump_path = treatments[treatment]['dump']
            if not os.path.exists(dump_path):
                treatments[treatment]['dump'] = {}
            else:
                treatments[treatment]['dump'] = pkl.load(open(treatments[treatment]['dump'], 'rb'))
        return treatments

class Subject():
    def __init__(self):
        self.tick = 0
        pass

    def load(self, name):
        with open(name, 'rb') as file:
            loaded_object = pkl.load(file)
            self.__dict__.update(loaded_object.__dict__)

    def save(self):
        if not os.path.exists(os.path.join(self.path, self.platform)):
            os.makedirs(os.path.join(self.path, self.platform))
        file = os.path.join(self.path, self.platform, self.id)
        pkl.dump(self, open(file, 'wb'))

    def create(self, path, platform, name, action, topic, replicate, experiment_id):
        self.path = path
        self.platform = platform
        self.id = name
        self.action = action
        self.topic = topic
        self.replicate = replicate
        self.experiment_id = experiment_id

        self.signied_id = False
        self.chrome_assigned = False
        self.platform_signin = False
        self.chrome = None
        self.email = None
        self.chromeid = None
        self.tick = 0

        self.save()

    def __str__(self):
        return f'{self.id}'
    
    def assignChrome(self):
        GW = GoogleWorkspace()
        self.email, self.chrome = GW.getUser(self.platform, self.experiment_id)
        debug(f'\t\t\t Assigning {self.chrome} chrome for {self.id}')
        self.chromeid = self.chrome
        GW.userAssigned(self.email, self.platform)
        self.chrome_assigned = True
        self.save()
        return


    def platformSignIn(self):
        self.Platform = getPlatform(self.platform)
        trial = Trial(self.action, self.topic, self.chromeid, self.Platform, self.experiment_id)
        file = os.path.join(self.path, f'{self.id}_{self.platform}.png')
        try:
            trial.signUpUser()
        except Exception as e:
            error(e)
            trial.closeDriver()
            return
        self.platform_signin = True
        trial.closeDriver()
        self.save()

    def checkChromeSignin(self):
        GW = GoogleWorkspace()
        signed = GW.checkChromeSignedIn(self.email)
        return signed
    
    def chromeSignIn(self):
        GW = GoogleWorkspace()
        GW.chromeSignIn(self.email)

    def checkSignin(self):
        trial = Trial(self.action, self.topic, self.chromeid, self.Platform, self.experiment_id)
        try:
            signed = trial.checkSignin()
        except Exception as e:
            error(e)
            trial.closeDriver()
            return False
        trial.closeDriver()
        return signed

    def save_dump(self, d, record):
        i = int(time())
        dump_path = os.path.join(self.path, record, self.platform, f'{i}.pkl')
        if not os.path.exists(os.path.join(self.path, record, self.platform)):
            os.makedirs(os.path.join(self.path, record, self.platform))
        pkl.dump(d, open(dump_path, 'wb'))
        return dump_path

    def observe(self, pre=False):
        trial = Trial(self.action, self.topic, self.chromeid, self.Platform, self.experiment_id)
        trial.loadUser()
        try:
            dump, screenshot = trial.observe()
        except Exception as e:
            error(e)
            trial.closeDriver()
            return

        trial.closeDriver()
        dump_path = self.save_dump(dump, 'observations')
        # random id
        if pre:
            tick = self.tick - 0.25
        else:
            tick = self.tick + 0.25

        logger = Logger(self.path, self.platform, self.experiment_id)
        logger.log(self.id, self.platform, tick, 'observe', 'home', dump_path, screenshot)
        self.save()
        
    def vanilla(self):
        trial = Trial('vanilla', self.topic, self.chromeid, self.Platform, self.experiment_id)
        trial.loadUser()
        dump = trial.runExperiment()
        trial.closeDriver()
        dump_path = self.save_dump(dump, 'vanillas')
        logger = Logger(self.path, self.platform, self.experiment_id)
        logger.log(self.id, self.platform, self.tick, self.action, self.topic, dump_path)

    def treatment(self):
        trial = Trial(self.action, self.topic, self.chromeid, self.Platform, self.experiment_id)
        trial.loadUser()
        try:
            dump = trial.runExperiment()
        except Exception as e:
            error(e)
            trial.closeDriver()
            return
        trial.closeDriver()
        dump_path = self.save_dump(dump, 'treatments')
        logger = Logger(self.path, self.platform, self.experiment_id)
        logger.log(self.id, self.platform, self.tick, self.action, self.topic, dump_path)


    def incrementTick(self):
        self.tick += 1
        self.save()

    def get_observations(self, tick):
        pre = tick - 0.25
        post = tick + 0.25
        logger = Logger(self.path, self.platform, self.experiment_id)
        pre = logger.get_observation(self.id, pre)
        post = logger.get_observation(self.id, post)
        return pre, post

    def get_treatments(self):
        logger = Logger(self.path, self.platform, self.experiment_id)
        return logger.get_treatments(self.id)
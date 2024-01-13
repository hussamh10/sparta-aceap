import pickle as pkl
import pandas as pd
import json
import sqlite3 as sql

from experiment.Experiment import Experiment
from experiment.Subject import Subject

def uploadResults(platform):
    config_file = 'config.json'
    config = json.load(open(config_file, 'r'))
    experiment = Experiment(config_file, platform)
    subjects = experiment.get_subjects()

    users = []
    for user in subjects:
        treatments = user.get_treatments()
        for tick in treatments:
            pre, post = user.get_observations(tick)
            treatments[tick]['pre'] = pre
            treatments[tick]['post'] = post

        users.append(treatments)

    pkl.dump(users, open(f'{platform}-results.pkl', 'wb'))

    return users
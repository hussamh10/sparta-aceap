from utils.log import debug
from platforms.Reddit import Reddit
from experiment_setup import create_user_csv, create_users_google
import account_creation.database as DB
from trial import Trial

import json


config = json.load(open('config.json', 'r'))
status = json.load(open('status.json', 'r'))

total_users = config['treatments'] + config['controls']
if status['google_signin'] == False:
    users = create_user_csv(total_users, config['email_template'], config['experiment_id'])
    input("UPLOAD CSV TO WORKSPACE")
    create_users_google(users)

users = DB.get_google_accounts(config['experiment_id'])

# ===============================
print(users)

debug('Experiment Begins')
# Experiment 
user_ids = list(users.keys())
treatments = user_ids[config['treatments']:]
controls = user_ids[:config['treatments']]

platforms = config['platforms']
action = config['action']
topic = config['topic']
experiment_id = config['experiment_id']
experiment_name = config['experiment_name']

# ===============================

# def Experiment(platform, treatment, controls, action, topic, experiment_id,
# experiment_name):

for treatment in treatments[2:]:
    platform = Reddit
    trial = Trial(action, topic, treatment, platform, experiment_name)
    trial.signUpUser()
    

for treatment in controls:
    platform = Reddit
    trial = Trial(action, topic, treatment, platform, experiment_name)
    trial.signUpUser()

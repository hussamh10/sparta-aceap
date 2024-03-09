from utils.log import debug
from platforms.Reddit import Reddit
from platforms.Twitter import Twitter
from experiment_setup import create_user_csv, create_users_google
from account_creation.database import DB
from experiment.trial import Trial
from utils.shuffleIP import shuffle

import json

config = json.load(open('config.json', 'r'))
db = DB('experiments.db', config['experiment_id'])

total_users = config['treatments'] + config['controls']

if not db.users_exists(total_users):
    users = create_user_csv(total_users, config['email_template'], config['experiment_id'])
    input("*** Upload CSV to Google Admin and press enter to continue... ***")
    db.add_google_accounts(users)

else: 
    users = db.get_google_accounts()

create_users_google(users, db)

users = db.get_google_accounts()

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

platform = Reddit
for treatment in treatments:
    trial = Trial(action, topic, treatment, platform, experiment_name)
    if not db.is_signed_in(platform, treatment):
        debug(f"Signing up user: {treatment}")
        trial.signUpUser()
        db.update_signin(platform, treatment)
    trial.runExperiment()
    shuffle()

for control in controls:
    trial = Trial(action, topic, control, platform, experiment_name)
    if not db.is_signed_in(platform, control):
        debug(f"Signing up user: {control}")
        trial.signUpUser()
        db.update_signin(platform, control)
    trial.runExperiment()
    shuffle()


#
    
actions = [1, 2, 3, 4]
topics = [1, 2, 3, 4]

number_of_users = get_number_of_users()
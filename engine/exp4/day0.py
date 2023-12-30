import json
from experiment.Experiment import Experiment
from account_creation.GoogleWorkspace import GoogleWorkspace

config = json.load(open('config.json', 'r'))
platforms = config['platforms']
print(config)

subject_names = []
for treatment in config['treatments']:
    for replicate in range(config['replication']):
        action = treatment['action']
        topic = treatment['topic']
        name = f'{action}_{topic}_{replicate}' 
        subject_names.append(name)

# do we need to create Google Users for these:
GW = GoogleWorkspace()
if GW.needUsers(config):
    GW.createUsers(config)

for platform in platforms:
    experiment = Experiment('config.json', platform)
    experiment.initiate()
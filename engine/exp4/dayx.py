import json
from experiment.Experiment import Experiment

config = json.load(open('config.json', 'r'))
platforms = config['platforms']

for platform in platforms:
    experiment = Experiment('config.json', platform)
    experiment.initiate()
    experiment.run()
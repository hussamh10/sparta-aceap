import json
from experiment.Experiment import Experiment
from experiment.Record import uploadResults

config = json.load(open('config.json', 'r'))
platforms = config['platforms']

for platform in platforms:
    try:
        uploadResults(platform)
    except Exception as e:
        print(e)
        pass

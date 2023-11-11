DIR = '/Users/hussam/Desktop/Projects/ACEAP/engine'
SESSIONS_PATH = f'{DIR}/data/sessions/'
USERS_PATH = f'{DIR}/data/users/'


SEARCH_COMMUNITIES = 'search_communities'
DEBUG = True

def pprint(obj):
    if DEBUG:
        print(f'DEBUG -- {obj}')
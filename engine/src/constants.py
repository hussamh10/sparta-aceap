import os

# Determine the base directory based on the operating system
if os.name == 'nt':  # Windows
    BASE_DIR = 'C:\\Path\\To\\Your\\Windows\\Directory'
elif os.name == 'posix':  # Unix-like systems (Linux, macOS)
    BASE_DIR = '/Users/hussam/Desktop/Projects/ACEAP/engine'

# Set the paths using os.path.join for OS compatibility
SESSIONS_PATH = os.path.join(BASE_DIR, 'data', 'sessions')
USERS_PATH = os.path.join(BASE_DIR, 'data', 'users')

SEARCH_COMMUNITIES = 'search_communities'

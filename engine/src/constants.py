import os

# Determine the base directory based on the operating system
if os.name == 'nt':  # Windows
    BASE_DIR = "C:\\Users\\hussa\\Desktop\\sparta-aceap\\engine"
    DATA_DIR = "C:\\Users\\hussa\\Desktop\\sparta-aceap\\engine\\data"
elif os.name == 'posix':  # Unix-like systems (Linux, macOS)
    BASE_DIR = '/Users/hussam/Desktop/Projects/ACEAP/engine'
    DATA_DIR = '/Users/hussam/Desktop/Projects/ACEAP/engine/data'

# Set the paths using os.path.join for OS compatibility
SESSIONS_PATH = os.path.join(BASE_DIR, 'data', 'sessions')
USERS_PATH = os.path.join(BASE_DIR, 'data', 'users')
SEARCH_COMMUNITIES = 'search_communities'

DATABASE = os.path.join(BASE_DIR, 'data', 'aceap.db')


def getPlatform(platform_name):
    platform_name = platform_name.lower()
    if platform_name == 'reddit':
        from platforms.Reddit import Reddit
        return Reddit
    elif platform_name == 'facebook':
        from platforms.Facebook import Facebook
        return Facebook
    elif platform_name == 'instagram':
        from platforms.Instagram import Instagram
        return Instagram
    elif platform_name == 'twitter':
        from platforms.Twitter import Twitter
        return Twitter
    elif platform_name == 'youtube':
        from platforms.Youtube import Youtube
        return Youtube
    elif platform_name == 'tiktok':
        from platforms.TikTok import TikTok
        return TikTok
    else:
        raise Exception('Platform not supported')

import sys
sys.path.append('../src')
from utils.util import wait
from platforms.Youtube import Youtube
from platforms.TikTok import TikTok
from utils.log import debug


yt = TikTok('xp3aceap0')
yt.loadBrowser()
yt.loadWebsite()
input()
debug('searching')
yt.searchTerm('football')
input()
debug('liking')
input()
yt.likePost()
debug('END')
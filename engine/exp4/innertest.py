from innertube import InnerTube, Client
from pprint import pprint

video_id = 'zL3wWykAKfs' # Still Woozy - Goodie Bag

ios = InnerTube("WEB")

data = ios.player(video_id=video_id)

pprint(data['playerAds'])
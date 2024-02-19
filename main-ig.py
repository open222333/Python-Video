from src.instagram import InstagramClawler
from src import IG_USERNAME, IG_PASSWORD
import json
import os

with open(os.path.join('conf', 'ig.json'), 'r') as f:
	info = json.loads(f.read())

for account in info:
	# print(account)
	ic = InstagramClawler(account)
	# ic.download_user_videos(IG_USERNAME, IG_PASSWORD)
	ic.move_to_dir()

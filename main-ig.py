from src.instagram import InstagramClawler
import json
import os

with open(os.path.join('conf', 'ig.json'), 'r') as f:
    info = json.dumps(f.read())

for account in info:
    ic = InstagramClawler(account)
    ic.download_user_videos()

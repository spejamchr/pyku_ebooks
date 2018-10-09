
import os
import json
import random
import twitter

from pyku_ebooks import PykuEbooks

KEYS_PATH = os.path.join(os.path.dirname(__file__), "keys.json")

try:
    with open(KEYS_PATH, "r") as f:
        keys = json.loads(f.read())
except FileNotFoundError:
    print("""Could not find the keys.json file. Copy keys.example.json to
    keys.json and fill in the correct values""")

api = twitter.Api(consumer_key=keys['consumer_key'],
                  consumer_secret=keys['consumer_secret'],
                  access_token_key=keys['access_token_key'],
                  access_token_secret=keys['access_token_secret'])

if random.random() > 0.5:
    haiku = PykuEbooks(4, "r/ocPoetry", "posts").haiku()
else:
    haiku = PykuEbooks(4, "r/WritingPrompts", "comments").haiku()

api.PostUpdate(haiku)

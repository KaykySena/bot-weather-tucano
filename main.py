import requests
import requests_oauthlib

import json
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#from dotenv import load_dotenv

from weather import get_weather
from twitter import create_tweet, post_tweet

# Local development
# Initialize environment variables
#load_dotenv()

# Write credentials to credentials.json file
with open("credentials.json", "w") as file:
    file.write(os.environ["FIREBASE_CREDENTIALS"])

# Authenticate Firebase's Realtime Database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL': os.environ["FIREBASE_DATABASE_URL"]
	})

# Open Firebase's Realtime Database
ref = db.reference("/")


# Post a tweet containing the current weather conditions in Tucano, Bahia
def main():
    tweet = create_tweet(get_weather())
    payload = {"text": "{}".format(tweet)}
    return post_tweet(payload, refresh_token())


# Refresh bot's twitter profile access token
def refresh_token():
    session = requests_oauthlib.OAuth2Session()
    token = session.refresh_token(
        token_url="https://api.twitter.com/2/oauth2/token",
        auth=(os.environ["TWITTER_CLIENT_ID"], os.environ["TWITTER_CLIENT_SECRET"]),
        refresh_token=json.loads(ref.get())["refresh_token"]
    )
    ref.set(json.dumps(token))
    return token


if __name__=="__main__":
    main()
import requests

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

# Set up Firebase's Realtime Database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(
    cred, 
    {'databaseURL': os.environ["FIREBASE_DATABASE_URL"]},
    )

ref = db.reference("/")

# Post a tweet containing the current weather conditions in Tucano, Bahia
def main():
    tweet = create_tweet(get_weather())
    payload = {"text": "{}".format(tweet)}
    return post_tweet(payload, refresh_token())


# Return new bot's Twitter account access token
def refresh_token():
    # Refresh access token
    token = requests.request(
        "POST",
        "https://api.twitter.com/2/oauth2/token",
        params={
            "refresh_token": ref.get()["refresh_token"],
            "grant_type": "refresh_token",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        auth=(os.environ["TWITTER_CLIENT_ID"], os.environ["TWITTER_CLIENT_SECRET"]),
    )

    # Store new access token in the database
    ref.set(token.json())
    return token.json()


if __name__=="__main__":
    main()

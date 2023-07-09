import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from PKCE import create_code_verifier, create_code_challenge
from weather import get_weather
from twitter import create_tweet, post_tweet

#from dotenv import load_dotenv

import requests

from flask import Flask, request, redirect

app = Flask(__name__)

#load_dotenv()

# Set up Firebase's Realtime Database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(
        cred, 
        {'databaseURL': os.environ["FIREBASE_DATABASE_URL"]}
    )

ref = db.reference("/")

code_verifier = create_code_verifier()
code_challenge = create_code_challenge(code_verifier)

@app.route("/")
def authorization():
    # Get authorization URL
    req = requests.Request(
        "GET",
        "https://twitter.com/i/oauth2/authorize",
        params={
            "response_type": "code",
            "client_id": os.environ["TWITTER_CLIENT_ID"],
            "redirect_uri": os.environ["TWITTER_REDIRECT_URI"],
            "scope": "tweet.read tweet.write users.read offline.access",
            "state": "state",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        },
    ).prepare()

    # Redirect user to authorization URL
    return redirect(req.url)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    # Get access token and refresh token from bot's Twitter account
    token = requests.request(
        "POST",
        "https://api.twitter.com/2/oauth2/token",
        params={
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": os.environ["TWITTER_REDIRECT_URI"],
            "code_verifier": code_verifier,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        auth=(os.environ["TWITTER_CLIENT_ID"], os.environ["TWITTER_CLIENT_SECRET"]),
    )

    # Store tokens in the database
    ref.set(token.json())
    return token.json()


if __name__=="__main__":
    app.run()
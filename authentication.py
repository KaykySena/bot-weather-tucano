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
from requests_oauthlib import OAuth2Session, TokenUpdated

from flask import Flask, request, redirect, session, url_for, render_template

app = Flask(__name__)
app.secret_key = os.urandom(50)

# Local development
# Initialize environment variables
#load_dotenv()

# Sets up Firebase's Realtime Database
cred = credentials.Certificate('credentials.json')
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL': os.environ["FIREBASE_DATABASE_URL"]
	})

ref = db.reference("/")

client_id = os.environ.get("TWITTER_CLIENT_ID")
client_secret = os.environ.get("TWITTER_CLIENT_SECRET")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
redirect_uri = os.environ.get("TWITTER_REDIRECT_URI")

scopes = ["tweet.read", "tweet.write", "users.read", "offline.access"]

code_verifier = create_code_verifier()
code_challenge = create_code_challenge(code_verifier)

@app.route("/")
def demo():
    global oauth
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
    authorization_url, state = oauth.authorization_url(
        auth_url, 
        code_challenge=code_challenge, 
        code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    if session["oauth_state"] != request.args["state"]:
        return abort(403)

    token = oauth.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code=request.args["code"],
        code_verifier=code_verifier
    )

    tweet = create_tweet(get_weather())
    payload = {"text": "{}".format(tweet)}
    ref.set(json.dumps(token))
    response = post_tweet(payload, token).json()
    return response
    

if __name__ == "__main__":
    app.run()

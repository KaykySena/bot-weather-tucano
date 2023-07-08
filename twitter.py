import requests

# Generate tweet in a given format
def create_tweet(response):
    return "{}\n🌡️ Temperatura: {} °C\n💧 Umidade: {}%\n💨 Vento: {} m/s".format(
                response["weather"][0]["description"].capitalize(), 
                response["main"]["temp"], 
                response["main"]["humidity"], 
                response["wind"]["speed"]
            )


# Post a tweet
def post_tweet(payload, token):
    return requests.request(
        "POST",
        "https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        }
    )
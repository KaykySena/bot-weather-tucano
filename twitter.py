import requests
import time

# Generate tweet in a given format
def create_tweet(response):
    weather = response["weather"][0]["main"]
    current_time = response["dt"] + response["timezone"]

    return "{}\n🌡️ Temperatura: {} °C\n💧 Umidade: {}%\n💨 Vento: {} m/s".format(
                get_emoji(weather, current_time) + " " + response["weather"][0]["description"].capitalize(), 
                response["main"]["temp"], 
                response["main"]["humidity"], 
                response["wind"]["speed"]
            )


# Return an emoji related to the weather condition
def get_emoji(weather, current_time):
    mapping = {
        "Thunderstorm": "🌩️",
        "Drizzle": "🌧️",
        "Rain": "🌧️",
        "Snow": "🌨️",
        "Clouds": "☁️"
    }

    isDay = time.gmtime(current_time).tm_hour in range(6, 18)

    if weather in mapping.keys():
        return mapping[weather]
    elif weather == "Clear":
        return "☀️" if isDay else "🌑"
    return "🌫️"


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
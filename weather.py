import requests
import json
import os
#from dotenv import load_dotenv

#load_dotenv()

# Return the current weather data in JSON format
def get_weather():
    return requests.get(("https://api.openweathermap.org/data/2.5/weather?id=3445983&appid={}&units=metric&lang=pt_br").format(os.environ["OPENWEATHER_API_KEY"])).json()

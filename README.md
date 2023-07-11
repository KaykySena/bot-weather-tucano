# bot-weather-tucano
[Tempo em Tucano](https://twitter.com/tempotucano) is a an automated Twitter profile who updates you about the weather in Tucano, a small town in the countryside of Brazil, every hour.

[An image of @tempotucano Twitter profile](/assets/Tempo%20em%20Tucano.png)

## Summary
In case you want to start exploring the Twitter API, the authentication process is the first step, so, I built a web application using Flask, a simple Python web framework, to fetch an access token for the bot's Twitter profile via [OAuth 2.0 Authorization Code Flow with PKCE](https://developer.twitter.com/en/docs/authentication/oauth-2-0/user-access-token). 

Moreover, I chose Firebase's Realtime Database to store the refresh token and, then, generate a new access token without prompting the user to give an authorization again since the access token was only valid for 2 hours.

About the tweets in itself, the weather data was obtained, free of charge, from OpenWeather API professional colection and then parsed to create the text of the tweet.

At last, GitHub Actions permited me to automate the enterity of this process to be done on a hourly basis thanks to its [schedule event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule).

## Files

### actions.yml
A GitHub Actions workflow which runs main.py every hour at minute 50[^1].

[^1]: A strategy to minimize delay since minute 0 is a common choice and, thus, GitHub Actions server is too congested. 

### requirements.txt

requirements.txt file contains the list of Python packages required to create the GitHub Actions' runner environment for main.py.

### weather.py
weather.py provide get_weather() function that requests OpenWeather API endpoint "https://api.openweathermap.org/data/2.5/weather" and return a string in JSON format of the current weather data.

### twitter.py

twitter.py provides three functions, two are meant to format the tweet text and, the other one, to post it.

### PKCE.py

PKCE.py provide methods to generate both code verifier and code challenge for PKCE extension of OAuth 2.0 Authorization Code flow.

### authentication.py

authentication.py implements OAuth 2.0 Authorization Code Flow with PKCE using Flask framework and store the fetched tokens in the Firebase's Realtime Database.

### main.py

main.py refresh the access token for the bot's Twitter profile, store it in the database and, then, post the tweet with the most recent weather data retrieved from OpenWeather API.

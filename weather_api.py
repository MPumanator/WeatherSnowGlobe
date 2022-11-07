import json
import requests
import datetime as datetime

token = ""
lat = ""
lon = ""

api_request_url_onecall = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid={token}&units=metric"


def get_weather_forecast():

    data = requests.get(api_request_url_onecall)
    readable_json = json.loads(data.content)
    print(data.text)

    def print_time(timestamp):
        print(datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S'))
        return

    # https://openweathermap.org/weather-conditions
    # you can use this mapping table to tailor the weather conditions
    # for example, you may consider 10% clouds to be "Clear" and 25% clouds or more to be "Cloudy"...

    def weather_lookup(id):
        if id in range(800, 803):  # we consider below 50% clouds to be "Clear"...
            return "Clear"
        elif id in range(803, 805):
            return "Clouds"
        elif id in range(700, 800):
            return "Mist"
        elif id in range(600, 700):
            return "Snow"
        elif id in range(500, 600):
            return "Rain"
        elif id in range(300, 400):
            return "Rain"
        elif id in range(200, 300):
            return "Thunderstorm"
        else:
            return "Mist"

    #  current time
    print_time(readable_json["current"]["dt"])
    print(readable_json["current"]["weather"][0]["main"])
    print(readable_json["current"]["weather"][0]["id"])
    current_weather = (weather_lookup(readable_json["current"]["weather"][0]["id"]))
    print(current_weather)
    
    weather_list = [current_weather]
    return weather_list

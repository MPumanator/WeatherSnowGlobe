from weather_api import get_weather_forecast

import time
import RPi.GPIO as GPIO
import datetime as datetime

GPIO.cleanup()

button_pin = 17
led1 = 27

io.setup(led1, io.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class Timer:
    value = 0
    max_value = (10 * 60) * 5

    def __init__(self):
        pass

    def reset(self):
        self.value = 0

    def tick(self):
        refresh = False

        if self.value >= Timer.max_value:
            self.reset()
            refresh = True

        self.value += 1
        time.sleep(0.09)
        return refresh


def weather_toggle(current_weather_displayed):
    if current_weather_displayed >= max_weather_displayable:
        current_weather_displayed = 0
    else:
        current_weather_displayed += 1
    return current_weather_displayed

global last_refreshed_weather
last_refreshed_weather = datetime.datetime.now()
weather_list = get_weather_forecast() 

def refresh_weather_data(current_weather_displayed, weather_list):
    global last_refreshed_weather
    the_time = datetime.datetime.now()
    print(f"last refresh: {last_refreshed_weather} - time now: {the_time}")
    if the_time >= last_refreshed_weather + datetime.timedelta(minutes=20):
        print("getting new weather from API")
        weather_list = get_weather_forecast()
        last_refreshed_weather = the_time
    else:
        print("using old data, no refresh needed")
    weathers = [
        {"time": "Now", "weather": weather_list[0]},
    ]
    weather_to_display = weathers[current_weather_displayed]
    return weather_to_display, weather_list


def get_input():
    if GPIO.input(button_pin) == GPIO.LOW:
        return True
    else:
        return False


def update_display(weather_to_display):
    print(f"{current_weather_displayed} - {weather_to_display['time']}: {weather_to_display['weather']}")
    #print_servo(servo_2, (weather_to_display["weather"]))
    if ("weather" == "snow"):
        io.output(led1, True)
    else:
        io.output(led1, False)


if __name__ == '__main__':

    current_weather_displayed = 0  # make weather display the current weather the first time
    weather_to_display, weather_list = refresh_weather_data(current_weather_displayed, weather_list)
    update_display(weather_to_display)
    max_weather_displayable = 5
    
    timer = Timer()
    print("Ready")
    while True:

        if get_input() is True:
            timer.reset()
            current_weather_displayed = weather_toggle(current_weather_displayed)
            weather_to_display, weather_list = refresh_weather_data(current_weather_displayed, weather_list)
            update_display(weather_to_display)

        refresh = timer.tick()

        #print(timer.value)
        if refresh is True:
            current_weather_displayed = weather_toggle(current_weather_displayed)
            weather_to_display, weather_list = refresh_weather_data(current_weather_displayed, weather_list)
            update_display(weather_to_display)

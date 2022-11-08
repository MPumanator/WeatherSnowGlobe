import requests

API Key = "50594282ceba8954fc461d77cf5792ed"
lat = "43.255"
lon = "-79.843"

url = https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

res = requests.get(url)
data = res.json()

weather = data['weather']['main']

print('Weather : {}'.format(main))

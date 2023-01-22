import sys
import requests

cities = {}
for city in sys.stdin:
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}&format=json"
    response = requests.get(geocoder_request)
    json_response = response.json()
    coords = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()[1]
    cities[float(coords)] = city
print(cities[min(cities.keys())])

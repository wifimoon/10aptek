import requests


def get_size(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lw = list(map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split()))
    up = list(map(float, toponym['boundedBy']['Envelope']['upperCorner'].split()))
    delta1 = str(up[0] - lw[0])
    delta2 = str(up[1] - lw[1])
    return delta1, delta2
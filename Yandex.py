import sys
from io import BytesIO
import requests
from PIL import Image

from cords import get_cords
from distance import lonlat_distance
from size import get_size


address = " ".join(sys.argv[1:])
address_ll = get_cords(address)

search_api_server = "https://search-maps.yandex.ru/v1/"

search_params = {
    "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)

if not response:
    print('Ошибка в запросе')

apteca_coodrinates = []
json_response = response.json()

for i in json_response['features'][:10]:
    cl = 'bl'
    if 'круглосуточно' in i['properties']['CompanyMetaData']['Hours']['text']:
        cl= 'gn'
    elif i['properties']['CompanyMetaData']['Hours']['text'] == '':
        cl = 'gr'
    apteca_coodrinates.append(",".join(list(map(str, i['geometry']['coordinates']))) + ',pm' + cl + 's')

map_params = {
    "l": "map",
    "pt": '~'.join(apteca_coodrinates)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"

response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(response.content)).show()
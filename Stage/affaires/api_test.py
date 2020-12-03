import json
import os
import requests


def get_shipsgo():
    url = requests.get('https://shipsgo.com/api/ContainerService/PostCustomContainerForm/')
    r = requests.get(url, headers={'Authorization': 'Bearer %s' % os.getenv('DO_ACCESS_TOKEN')})
    shipsgo = r.json()
    shipsgo_list = []
    for i in range(len(shipsgo['shipsgo'])):
        shipsgo_list.append(shipsgo['shipsgo'][i])
    return shipsgo_list

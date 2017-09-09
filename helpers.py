import json
import requests

from settings import ASSETS


def get_valid_assets():
    for i in _query('https://api.coinmarketcap.com/v1/ticker/?limit=300', None):
        ASSETS[i['symbol'].upper()] = {
            'id': i['id'],
            'name': i['name'],
        }


def _query(url, header):
    r = requests.post(url, data=header)
    if r.status_code != 200:
        r = requests.get(url, data=header)
    if r.status_code == 200:
        return json.loads(r.text)


class CoinNotFound(Exception):
    pass

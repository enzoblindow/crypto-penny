import sys
sys.path.insert(0, '/Users/Enzo/Desktop/CryptoClass')

from exceptions import CoinNotFound
from helpers import _query
from helpers import get_valid_assets

from settings import ASSETS


class Coin():
    """One Coin to rule them all."""

    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.validate()

    def validate(self):
        if len(ASSETS) == 0:
            get_valid_assets()
        if self.symbol in ASSETS.keys():
            asset = ASSETS[self.symbol]
            self.id = asset['id']
            self.name = asset['name']
        else:
            raise CoinNotFound('Could not find coin {}'.format(self.symbol))


class Pair():
    """Two coins make one pair."""

    def __init__(self, pair):
        self.pair = pair.upper()
        self.make_coins()
        self.fetch()

    def make_coins(self):
        try:
            self.base = Coin(self.pair[:3])
            i = 3
        except CoinNotFound:
            self.base = Coin(self.pair[:4])
            i = 4
        try:
            self.target = Coin(self.pair[i:i+3])
        except CoinNotFound:
            self.target = Coin(self.pair[i:i+4])

    def fetch(self):
        url = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'\
              .format(self.base.id, self.target.symbol)
        response = _query(url, None)[0]
        self.volume_usd = int(float(response['24h_volume_usd']))
        self.market_cap_usd = int(float(response['market_cap_usd']))
        self.available_supply = int(float(response['available_supply']))
        self.total_supply = int(float(response['total_supply']))
        self.percent_change_1h = float(response['percent_change_1h'])
        self.percent_change_24h = float(response['percent_change_24h'])
        self.percent_change_7d = float(response['percent_change_7d'])
        self.last_updated = response['last_updated']
        self.price = round(float(response['price_{}'.format(self.target.symbol.lower())]), 2)
        self.volume = round(float(response['24h_volume_{}'.format(self.target.symbol.lower())]), 2)
        self.market_cap = round(float(response['market_cap_{}'.format(self.target.symbol.lower())]), 2)

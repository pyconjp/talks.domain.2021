import json
from urllib.request import urlopen


def fetch_data(url):
    with urlopen(url) as res:
        return json.load(res)

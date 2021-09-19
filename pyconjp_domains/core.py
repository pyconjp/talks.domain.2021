import json
from urllib.request import urlopen


def fetch_data(url):
    with urlopen(url) as res:
        return json.load(res)


def is_included(title):
    patterns = ["Venue open", "スペシャルブース紹介", "Ask the speaker", "Break"]
    for pattern in patterns:
        if title.startswith(pattern):
            return False
    return True


def filter_sessions(sessions):
    """タイムテーブルに載せるsessionだけに絞り込む"""
    return filter(lambda d: is_included(d["title"]), sessions)

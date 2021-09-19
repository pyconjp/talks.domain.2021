import json
from urllib.request import urlopen

from pyconjp_domains.talks import Speaker


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


def create_room_id_name_map(room_data):
    return {d["id"]: d["name"] for d in room_data}


def create_speaker_id_map(speaker_data):
    return {d["id"]: Speaker(d["fullName"], d["bio"]) for d in speaker_data}


def create_category_id_value_map(category_data):
    return {
        item["id"]: item["name"] for d in category_data for item in d["items"]
    }

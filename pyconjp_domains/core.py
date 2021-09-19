import json
from collections import defaultdict
from datetime import datetime
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


def date_from_string(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S").date()


def create_date_string_to_slot_number_map(date_strings):
    date_string_to_slot_number_map = {}

    date_to_strings_map = defaultdict(list)
    for date_string in date_strings:
        date = date_from_string(date_string)
        date_to_strings_map[date].append(date_string)

    for date_strings in date_to_strings_map.values():
        date_string_to_slot_number_map.update(
            {s: i for i, s in enumerate(sorted(date_strings), start=1)}
        )

    return date_string_to_slot_number_map

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

from pyconjp_domains.constants import SESSIONIZE_DATETIME_FORMAT
from pyconjp_domains.talks import Category, Slot, Speaker


class CategoryFactory:
    def __init__(self, item_id_to_category_title, item_id_to_name):
        self._item_id_to_category_title = item_id_to_category_title
        self._item_id_to_name = item_id_to_name

    def create(self, values: list[int], is_plenary: bool) -> Category:
        track, level = None, None
        speaking_language, slide_language = None, None
        for value in values:
            category = self._item_id_to_category_title[value]
            if category == "Track":
                track = self._item_id_to_name[value]
            elif category == "Level":
                level = self._item_id_to_name[value]
            elif category == "Language":
                speaking_language = self._item_id_to_name[value]
            elif category == "発表資料の言語 / Language of presentation material":
                slide_language = self._item_id_to_name[value]
        level = "All" if is_plenary else level
        return Category(track, level, speaking_language, slide_language)

    @classmethod
    def from_(cls, categories_raw_data):
        item_id_to_category_title = cls._create_item_id_to_category_title_map(
            categories_raw_data
        )
        item_id_to_name = cls._create_item_id_to_name_map(categories_raw_data)
        return cls(item_id_to_category_title, item_id_to_name)

    @staticmethod
    def _create_item_id_to_category_title_map(categories_raw_data):
        return {
            item["id"]: d["title"]
            for d in categories_raw_data
            for item in d["items"]
        }

    @staticmethod
    def _create_item_id_to_name_map(categories_raw_data):
        return {
            item["id"]: item["name"]
            for d in categories_raw_data
            for item in d["items"]
        }


class SlotFactory:
    def __init__(self, room_id_to_name, starts_at_to_slot_number):
        self._room_id_to_name = room_id_to_name
        self._starts_at_to_slot_number = starts_at_to_slot_number

    def create(self, starts_at: str, room_id: int) -> Slot:
        return Slot.create(
            self._room_id_to_name[room_id],
            starts_at,
            # モーダル表示しないトークは、CSVのno (=talk.slot_number) を0にする
            self._starts_at_to_slot_number.get(starts_at, 0),
        )

    @classmethod
    def from_(cls, rooms_raw_data, starts_at_strings) -> SlotFactory:
        room_id_to_name = cls._create_room_id_to_name_map(rooms_raw_data)
        starts_at_to_slot_number = (
            cls._create_datetime_string_to_slot_number_map(starts_at_strings)
        )
        return cls(room_id_to_name, starts_at_to_slot_number)

    @staticmethod
    def date_from_string(string: str) -> date:
        return datetime.strptime(string, SESSIONIZE_DATETIME_FORMAT).date()

    @staticmethod
    def _create_room_id_to_name_map(rooms_raw_data):
        return {d["id"]: d["name"] for d in rooms_raw_data}

    @staticmethod
    def _create_datetime_string_to_slot_number_map(datetime_strings):
        date_string_to_slot_number_map = {}

        date_to_strings_map = defaultdict(list)
        for datetime_string in datetime_strings:
            date = SlotFactory.date_from_string(datetime_string)
            date_to_strings_map[date].append(datetime_string)

        for datetime_strings_per_date in date_to_strings_map.values():
            date_string_to_slot_number_map.update(
                {
                    s: i
                    for i, s in enumerate(
                        sorted(datetime_strings_per_date), start=1
                    )
                }
            )

        return date_string_to_slot_number_map


class SpeakerFactory:
    def __init__(self, id_to_raw_data_map):
        self._id_to_raw_data_map = id_to_raw_data_map

    def create(self, speaker_id: str) -> Speaker:
        speaker_data = self._id_to_raw_data_map[speaker_id]
        return Speaker(speaker_data["fullName"], speaker_data["bio"])

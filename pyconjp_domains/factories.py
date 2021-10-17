from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

from pyconjp_domains.constants import SESSIONIZE_DATETIME_FORMAT
from pyconjp_domains.talks import (
    Category,
    QuestionAnswer,
    ScheduledTalk,
    Slot,
    Speaker,
)


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


class QuestionAnswerFactory:
    def __init__(self, question_value_to_id_map):
        self._question_value_to_id_map = question_value_to_id_map

    def create(self, question_answers_data) -> QuestionAnswer:
        question_id_to_answer_map = {
            d["questionId"]: d["answerValue"] for d in question_answers_data
        }
        elevator_pitch = question_id_to_answer_map.get(
            self._question_value_to_id_map["Elevator Pitch"]
        )
        prior_knowledge = question_id_to_answer_map.get(
            self._question_value_to_id_map["オーディエンスに求める前提知識"]
        )
        take_away = question_id_to_answer_map.get(
            self._question_value_to_id_map["オーディエンスが持って帰れる具体的な知識やノウハウ"]
        )
        return QuestionAnswer(elevator_pitch, prior_knowledge, take_away)

    @classmethod
    def from_(cls, questions_raw_data) -> QuestionAnswerFactory:
        question_value_to_id_map = {
            d["question"]: d["id"] for d in questions_raw_data
        }
        return cls(question_value_to_id_map)


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

    @classmethod
    def from_(cls, speakers_raw_data) -> SpeakerFactory:
        id_to_raw_data_map = {data["id"]: data for data in speakers_raw_data}
        return cls(id_to_raw_data_map)


class ScheduledTalkFactory:
    def __init__(
        self,
        category_factory: CategoryFactory,
        question_answer_factory: QuestionAnswerFactory,
        speaker_factory: SpeakerFactory,
        slot_factory: SlotFactory,
    ):
        self._category_factory = category_factory
        self._question_answer_factory = question_answer_factory
        self._speaker_factory = speaker_factory
        self._slot_factory = slot_factory

    @staticmethod
    def calculate_duration_min(start: str, end: str) -> int:
        start_datetime = datetime.strptime(start, SESSIONIZE_DATETIME_FORMAT)
        end_datetime = datetime.strptime(end, SESSIONIZE_DATETIME_FORMAT)
        duration = end_datetime - start_datetime
        return duration.seconds // 60

    def create(self, session) -> ScheduledTalk:
        slot = self._slot_factory.create(
            session["startsAt"], session["roomId"]
        )
        duration_min = self.calculate_duration_min(
            session["startsAt"], session["endsAt"]
        )
        return ScheduledTalk(
            session["id"],
            session["title"],
            session["description"],
            None,
            None,
            [],
            slot,
            duration_min,
        )

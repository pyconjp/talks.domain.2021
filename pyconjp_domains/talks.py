from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime, time


def get_single_choice_category_value(category: dict) -> str:
    """sessionizeのAPIの返り値から単一選択項目の選択値を返す"""
    return category["categoryItems"][0]["name"]


@dataclass
class Speaker:
    name: str
    profile: str | None = None


@dataclass
class Category:
    track: str | None
    level: str | None
    speaking_language: str | None
    slide_language: str | None

    @staticmethod
    def flatten_raw_json(categories: list[dict]) -> dict[str, str]:
        """sessionizeのAPIの返り値のうち、ネストしたcategoriesフィールドをパースして平坦にする"""
        for category in categories:
            if category["name"] == "Track":
                track = get_single_choice_category_value(category)
                continue
            if category["name"] == "Level":
                level = get_single_choice_category_value(category)
                continue
            if category["name"] == "Language":
                speaking_language = get_single_choice_category_value(category)
                continue
            if (
                category["name"]
                == "発表資料の言語 / Language of presentation material"
            ):
                slide_language = get_single_choice_category_value(category)
                continue
        return {
            "track": track,
            "level": level,
            "speaking_language": speaking_language,
            "slide_language": slide_language,
        }

    @classmethod
    def from_raw_json(cls, categories):
        return cls(**cls.flatten_raw_json(categories))


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


@dataclass
class QuestionAnswer:
    elevator_pitch: str | None
    audience_prior_knowledge: str | None
    audience_take_away: str | None

    @staticmethod
    def flatten_raw_json(question_answers: list[dict]) -> dict[str, str]:
        for qa in question_answers:
            if qa["question"] == "Elevator Pitch":
                elevator_pitch = qa["answer"]
                continue
            if qa["question"] == "オーディエンスに求める前提知識":
                audience_prior_knowledge = qa["answer"]
                continue
            if qa["question"] == "オーディエンスが持って帰れる具体的な知識やノウハウ":
                audience_take_away = qa["answer"]
                continue
        return {
            "elevator_pitch": elevator_pitch,
            "audience_prior_knowledge": audience_prior_knowledge,
            "audience_take_away": audience_take_away,
        }

    @classmethod
    def from_raw_json(cls, question_answers):
        return cls(**cls.flatten_raw_json(question_answers))


@dataclass
class Talk:
    id: int | str
    title: str
    description: str | None
    category: Category | None
    answer: QuestionAnswer | None
    speakers: list[Speaker]

    @property
    def track(self):
        return self.category.track if self.category else None

    @property
    def level(self):
        return self.category.level if self.category else None

    @property
    def speaking_language(self):
        return self.category.speaking_language if self.category else None

    @property
    def slide_language(self):
        return self.category.slide_language if self.category else None

    @property
    def elevator_pitch(self):
        return self.answer.elevator_pitch if self.answer else None

    @property
    def prior_knowledge(self):
        return self.answer.audience_prior_knowledge if self.answer else None

    @property
    def take_away(self):
        return self.answer.audience_take_away if self.answer else None

    @property
    def speaker_names(self):
        return [spaeker.name for spaeker in self.speakers]

    @property
    def speaker_profiles(self):
        return [speaker.profile for speaker in self.speakers]

    def as_list(self, fields):
        return [getattr(self, field) for field in fields]


@dataclass
class Talks(Sequence):
    talks: list[Talk]

    def __len__(self):
        return len(self.talks)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(self.talks[key])
        return self.talks[key]

    @classmethod
    def from_raw_json(cls, data):
        talks = []
        for session in data:
            speakers = [
                Speaker(speaker["name"]) for speaker in session["speakers"]
            ]
            category = Category.from_raw_json(session["categories"])
            question_answers = QuestionAnswer.from_raw_json(
                session["questionAnswers"]
            )
            talk = Talk(
                int(session["id"]),
                session["title"],
                session["description"],
                category,
                question_answers,
                speakers,
            )
            talks.append(talk)
        return cls(sorted(talks, key=lambda t: t.id))

    def filter_by(self, request: dict) -> "Talks":
        talks = self.talks
        if request["tracks"]:
            talks = [t for t in talks if t.category.track in request["tracks"]]
        if request["levels"]:
            talks = [t for t in talks if t.category.level in request["levels"]]
        if request["keywords"]:
            # AND検索。case-insensitive。
            # タイトル・エレベータピッチ・前提知識・持ち帰れるものの部分文字列か（詳細は使っていない）
            for keyword in request["keywords"]:
                talks = [
                    t
                    for t in talks
                    if keyword
                    in "\n".join(
                        [
                            t.title,
                            t.answer.elevator_pitch,
                            t.answer.audience_prior_knowledge,
                            t.answer.audience_take_away,
                        ]
                    ).lower()
                ]
        if request["is_english_only"]:
            talks = [
                t
                for t in talks
                # speaking_language は Japanese / English
                if t.category.speaking_language == "English"
                # slide_language は Japanese only / English only / Both
                or t.category.slide_language != "Japanese only"
            ]
        return self.__class__(talks)


@dataclass
class Slot:
    room: str
    day: date
    start: time
    number: int

    @classmethod
    def create(cls, room: str, start_datetime_str: str, number: int):
        start_datetime = datetime.strptime(
            start_datetime_str, "%Y-%m-%dT%H:%M:%S"
        )
        return cls(room, start_datetime.date(), start_datetime.time(), number)


class SlotFactory:
    def __init__(self, room_id_to_name, start_to_slot_number):
        self._room_id_to_name = room_id_to_name
        self._start_to_slot_number = start_to_slot_number

    def create(self, starts_at: str, room_id: int) -> Slot:
        return Slot.create(
            self._room_id_to_name[room_id],
            starts_at,
            self._start_to_slot_number[starts_at],
        )


@dataclass
class ScheduledTalk(Talk):
    slot: Slot
    duration_min: int
    slide_url: str | None = None
    recording_url: str | None = None

    @property
    def room(self):
        return self.slot.room

    @property
    def day(self):
        return self.slot.day

    @property
    def start_time(self):
        return self.slot.start

    @property
    def slot_number(self):
        return self.slot.number


@dataclass
class ScheduledTalks(Sequence):
    talks: list[ScheduledTalk]

    def __len__(self):
        return len(self.talks)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(self.talks[key])
        return self.talks[key]

    def sorted(self):
        return self.__class__(
            sorted(self.talks, key=lambda t: (t.day, t.slot_number, t.room))
        )

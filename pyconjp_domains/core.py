import json
from collections import defaultdict
from datetime import datetime
from urllib.request import urlopen

from pyconjp_domains.talks import (
    Category,
    QuestionAnswer,
    ScheduledTalk,
    ScheduledTalks,
    Slot,
    Speaker,
)


def fetch_data(url):
    with urlopen(url) as res:
        return json.load(res)


def is_included(title):
    # 休憩時間はタイムテーブルに含めない
    patterns = ["スペシャルブース", "Ask the speaker", "Break"]
    for pattern in patterns:
        if title.startswith(pattern):
            return False
    return True


def filter_sessions(sessions):
    """タイムテーブルに載せるsessionだけに絞り込む"""
    return filter(lambda d: is_included(d["title"]), sessions)


def _filter_with_modal_sessions(sessions):
    """タイムテーブルでモーダル表示するsessionだけに絞り込む"""
    # 「Venue open / 開場」だけモーダル表示しない
    for session in sessions:
        if "開場" not in session["title"]:
            yield session


def create_room_id_name_map(room_data):
    return {d["id"]: d["name"] for d in room_data}


def create_speaker_id_map(speaker_data):
    return {d["id"]: Speaker(d["fullName"], d["bio"]) for d in speaker_data}


def create_category_id_value_map(category_data):
    return {
        item["id"]: item["name"] for d in category_data for item in d["items"]
    }


def create_question_value_id_map(question_data):
    return {d["question"]: d["id"] for d in question_data}


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


def create_talks_from_data(data):
    room_id_name_map = create_room_id_name_map(data["rooms"])
    speaker_id_map = create_speaker_id_map(data["speakers"])
    category_id_value_map = create_category_id_value_map(data["categories"])
    question_value_id_map = create_question_value_id_map(data["questions"])

    sessions = list(filter_sessions(data["sessions"]))
    start_to_slot_number_map = create_date_string_to_slot_number_map(
        set(s["startsAt"] for s in _filter_with_modal_sessions(sessions))
    )
    talks = []
    for session in sessions:
        slot = Slot.create(
            room_id_name_map[session["roomId"]],
            session["startsAt"],
            # モーダル表示しないトークは、CSVのno (=talk.slot_number) を0にする
            start_to_slot_number_map.get(session["startsAt"], 0),
        )
        if session["isServiceSession"]:
            talk = ScheduledTalk(
                session["id"],
                session["title"],
                session["description"],
                None,
                None,
                [],
                slot,
            )
        else:
            question_id_answer_map = {
                d["questionId"]: d["answerValue"]
                for d in session["questionAnswers"]
            }
            talk = ScheduledTalk(
                session["id"],
                session["title"],
                session["description"],
                Category(
                    *(
                        category_id_value_map[category_id]
                        for category_id in session["categoryItems"]
                    )
                ),
                QuestionAnswer(
                    question_id_answer_map[
                        question_value_id_map["Elevator Pitch"]
                    ],
                    question_id_answer_map[
                        question_value_id_map["オーディエンスに求める前提知識"]
                    ],
                    question_id_answer_map[
                        question_value_id_map["オーディエンスが持って帰れる具体的な知識やノウハウ"]
                    ],
                ),
                [
                    speaker_id_map[speaker_id]
                    for speaker_id in session["speakers"]
                ],
                slot,
                # Workaround: Use live URL as slide URL
                session["liveUrl"],
                session["recordingUrl"],
            )
        talks.append(talk)

    return ScheduledTalks(talks)


def fetch_talks(url):
    data = fetch_data(url)
    return create_talks_from_data(data)

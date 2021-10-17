import json
from datetime import datetime
from urllib.request import urlopen

from pyconjp_domains.constants import SESSIONIZE_DATETIME_FORMAT
from pyconjp_domains.factories import (
    CategoryFactory,
    SlotFactory,
    SpeakerFactory,
)
from pyconjp_domains.talks import QuestionAnswer, ScheduledTalk, ScheduledTalks


def fetch_data(url):
    with urlopen(url) as res:
        return json.load(res)


def is_included(title):
    # 休憩時間はタイムテーブルに含めない
    patterns = ["スペシャルブース訪問", "Ask the speaker", "Break"]
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


def create_question_value_id_map(question_data):
    return {d["question"]: d["id"] for d in question_data}


def calculate_duration_min(start: str, end: str) -> int:
    start_datetime = datetime.strptime(start, SESSIONIZE_DATETIME_FORMAT)
    end_datetime = datetime.strptime(end, SESSIONIZE_DATETIME_FORMAT)
    duration = end_datetime - start_datetime
    return duration.seconds // 60


def create_talks_from_data(data):
    speaker_factory = SpeakerFactory.from_(data["speakers"])
    category_factory = CategoryFactory.from_(data["categories"])
    question_value_id_map = create_question_value_id_map(data["questions"])

    sessions = list(filter_sessions(data["sessions"]))
    slot_factory = SlotFactory.from_(
        data["rooms"],
        set(s["startsAt"] for s in _filter_with_modal_sessions(sessions)),
    )
    talks = []
    for session in sessions:
        slot = slot_factory.create(session["startsAt"], session["roomId"])
        duration_min = calculate_duration_min(
            session["startsAt"], session["endsAt"]
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
                duration_min,
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
                category_factory.create(
                    session["categoryItems"], session["isPlenumSession"]
                ),
                QuestionAnswer(
                    question_id_answer_map.get(
                        question_value_id_map["Elevator Pitch"]
                    ),
                    question_id_answer_map.get(
                        question_value_id_map["オーディエンスに求める前提知識"]
                    ),
                    question_id_answer_map.get(
                        question_value_id_map["オーディエンスが持って帰れる具体的な知識やノウハウ"]
                    ),
                ),
                [
                    speaker_factory.create(speaker_id)
                    for speaker_id in session["speakers"]
                ],
                slot,
                duration_min,
                # Workaround: Use live URL as slide URL
                session["liveUrl"],
                session["recordingUrl"],
            )
        talks.append(talk)

    return ScheduledTalks(talks)


def fetch_talks(url):
    data = fetch_data(url)
    return create_talks_from_data(data)

import json
from urllib.request import urlopen

from pyconjp_domains.factories import (
    CategoryFactory,
    QuestionAnswerFactory,
    ScheduledTalkFactory,
    SlotFactory,
    SpeakerFactory,
)
from pyconjp_domains.talks import ScheduledTalks


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


def create_talks_from_data(data):
    sessions = list(filter_sessions(data["sessions"]))

    category_factory = CategoryFactory.from_(data["categories"])
    question_answer_factory = QuestionAnswerFactory.from_(data["questions"])
    speaker_factory = SpeakerFactory.from_(data["speakers"])
    slot_factory = SlotFactory.from_(
        data["rooms"],
        set(s["startsAt"] for s in _filter_with_modal_sessions(sessions)),
    )
    talk_factory = ScheduledTalkFactory(
        category_factory,
        question_answer_factory,
        speaker_factory,
        slot_factory,
    )

    talks = []
    for session in sessions:
        talk = talk_factory.create(session)
        talks.append(talk)

    return ScheduledTalks(talks)


def fetch_talks(url):
    data = fetch_data(url)
    return create_talks_from_data(data)

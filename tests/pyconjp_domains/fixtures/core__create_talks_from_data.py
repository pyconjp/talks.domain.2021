"""このfixtureで表現しているタイムテーブル

Venue open / 開場  # 注: モーダルを出さないのでSlot.numberは振られない

Opening (Day 1)

Keynote: Day 1 キーノートスピーカー

トーク3, トーク2  # 注: id順なので返り値はトーク2, トーク3の順

トーク1, トーク4

Closing (Day 1)
"""

from datetime import date, time

from pyconjp_domains import talks as t

venue_open_uuid = "6a66fe7e-4a71-48b2-85ea-174d2ad98d92"
opening_uuid = "353ae2e0-b3fe-4a76-adf1-b85f612833d2"
keynote_uuid = "56c983c2-262e-4e4d-ba07-8f2496f2feba"
closing_uuid = "9e0b7d58-f102-4453-9fbe-f1bd5eb47183"

speaker1_uuid = "c6e3c83c-ef69-4203-882f-b9326e388e87"
speaker2_uuid = "f3777251-0201-4048-abaa-1d234700e441"
speaker3_uuid = "1b8d29d9-81c4-43a0-8794-76799d1a4abc"
speaker4_uuid = "0ead2886-0db3-44f2-ae29-2c2240adfc6b"

data = {
    "sessions": [
        {
            "id": venue_open_uuid,
            "title": "Venue open / 開場",
            "description": None,
            "startsAt": "2021-10-15T12:30:00",
            "isServiceSession": True,
            "speakers": [],
            "categoryItems": [],
            "questionAnswers": [],
            "roomId": 20030,
            "liveUrl": None,
            "recordingUrl": None,
        },
        {
            "id": opening_uuid,
            "title": "Opening (Day 1)",
            "description": "オープニング、盛り上がっていきましょう！",
            "startsAt": "2021-10-15T13:00:00",
            "isServiceSession": True,
            "speakers": [],
            "categoryItems": [],
            "questionAnswers": [],
            "roomId": 20030,
            "liveUrl": None,
            "recordingUrl": None,
        },
        {
            # TODO: service sessionでないsessionに変える可能性あり
            "id": keynote_uuid,
            "title": "Keynote: Day 1 キーノートスピーカー",
            "description": "〇〇で有名な氏による基調講演です",
            "startsAt": "2021-10-15T13:30:00",
            "isServiceSession": True,
            "speakers": [],
            "categoryItems": [],
            "questionAnswers": [],
            "roomId": 20030,
            "liveUrl": None,
            "recordingUrl": None,
        },
        {
            "id": "203012",
            "title": "トーク2",
            "description": "トーク2の\n詳細です",
            "startsAt": "2021-10-15T15:00:00",
            "isServiceSession": False,
            "speakers": [speaker2_uuid],
            "categoryItems": [80045, 80019, 80023, 80024],
            "questionAnswers": [
                {"questionId": 30014, "answerValue": "トーク2のエレベータピッチ"},
                {"questionId": 30016, "answerValue": "トーク2で持ち帰れるもの"},
                {"questionId": 30018, "answerValue": "トーク2の前提知識"},
            ],
            "roomId": 20007,
            "liveUrl": "",
            "recordingUrl": "",
        },
        {
            "id": "203023",
            "title": "トーク3",
            "description": "トーク3の\n詳細です",
            "startsAt": "2021-10-15T15:00:00",
            "isServiceSession": False,
            "speakers": [speaker3_uuid],
            "categoryItems": [80046, 80020, 80023, 80026],
            "questionAnswers": [
                {"questionId": 30014, "answerValue": "トーク3のエレベータピッチ"},
                {"questionId": 30016, "answerValue": "トーク3で持ち帰れるもの"},
                {"questionId": 30018, "answerValue": "トーク3の前提知識"},
            ],
            "roomId": 20001,
            "liveUrl": "",
            "recordingUrl": "",
        },
        {
            "id": "203001",
            "title": "トーク1",
            "description": "トーク1の\n詳細です",
            "startsAt": "2021-10-15T17:00:00",
            "isServiceSession": False,
            "speakers": [speaker1_uuid],
            "categoryItems": [80047, 80018, 80022, 80025],
            "questionAnswers": [
                {"questionId": 30014, "answerValue": "トーク1のエレベータピッチ"},
                {"questionId": 30016, "answerValue": "トーク1で持ち帰れるもの"},
                {"questionId": 30018, "answerValue": "トーク1の前提知識"},
            ],
            "roomId": 20001,
            "liveUrl": "",
            "recordingUrl": "",
        },
        {
            "id": "203034",
            "title": "トーク4",
            "description": "トーク4の\n詳細です",
            "startsAt": "2021-10-15T17:00:00",
            "isServiceSession": False,
            "speakers": [speaker4_uuid],
            "categoryItems": [80043, 80019, 80023, 80026],
            "questionAnswers": [
                {"questionId": 30014, "answerValue": "トーク4のエレベータピッチ"},
                {"questionId": 30016, "answerValue": "トーク4で持ち帰れるもの"},
                {"questionId": 30018, "answerValue": "トーク4の前提知識"},
            ],
            "roomId": 20007,
            "liveUrl": "",
            "recordingUrl": "",
        },
        {
            "id": closing_uuid,
            "title": "Closing (Day 1)",
            "description": None,
            "startsAt": "2021-10-15T18:45:00",
            "isServiceSession": True,
            "speakers": [],
            "categoryItems": [],
            "questionAnswers": [],
            "roomId": 20030,
            "liveUrl": None,
            "recordingUrl": None,
        },
    ],
    "speakers": [
        {"id": speaker1_uuid, "bio": "スピーカー1のプロフィール", "fullName": "スピーカー1"},
        {"id": speaker2_uuid, "bio": "プロフィール of スピーカー2", "fullName": "スピーカー2"},
        {"id": speaker3_uuid, "bio": "スピーカー3のプロフィール。", "fullName": "スピーカー3"},
        {"id": speaker4_uuid, "bio": "プロフィール・オブ・スピーカー4", "fullName": "スピーカー4"},
    ],
    "questions": [
        {"id": 30014, "question": "Elevator Pitch"},
        {"id": 30016, "question": "オーディエンスが持って帰れる具体的な知識やノウハウ"},
        {"id": 30018, "question": "オーディエンスに求める前提知識"},
    ],
    "categories": [
        {
            "id": 30011,
            "title": "Track",
            "items": [
                {"id": 80045, "name": "Python core and around"},
                {"id": 80046, "name": "Machine learning"},
                {"id": 80047, "name": "Web programming"},
                {"id": 80043, "name": "Visual / Game / Music"},
                {"id": 80050, "name": "Approaching to social problem"},
                {"id": 80028, "name": "Outside of Python language"},
                {"id": 80051, "name": "Only for fun or try new technique"},
                {
                    "id": 80017,
                    "name": (
                        "Anything else basically which doesn’t fall into "
                        "the types of topics above"
                    ),
                },
            ],
        },
        {
            "id": 30012,
            "title": "Level",
            "items": [
                {"id": 80018, "name": "Beginner"},
                {"id": 80019, "name": "Intermediate"},
                {"id": 80020, "name": "Advanced"},
                {"id": 80021, "name": "Expert"},
            ],
        },
        {
            "id": 30013,
            "title": "Language",
            "items": [
                {"id": 80022, "name": "English"},
                {"id": 80023, "name": "Japanese"},
            ],
        },
        {
            "id": 30015,
            "title": "発表資料の言語 / Language of presentation material",
            "items": [
                {"id": 80025, "name": "English only"},
                {"id": 80026, "name": "Japanese only"},
                {"id": 80024, "name": "Both"},
            ],
        },
    ],
    "rooms": [
        {"id": 20030, "name": "#pyconjp"},
        {"id": 20001, "name": "#pyconjp_1"},
        {"id": 20007, "name": "#pyconjp_2"},
    ],
}

the_day = date(2021, 10, 15)

expected = t.ScheduledTalks(
    [
        t.ScheduledTalk(
            venue_open_uuid,
            "Venue open / 開場",
            None,
            None,
            None,
            [],
            t.Slot("#pyconjp", the_day, time(12, 30), 0),
            30,
        ),
        t.ScheduledTalk(
            opening_uuid,
            "Opening (Day 1)",
            "オープニング、盛り上がっていきましょう！",
            None,
            None,
            [],
            t.Slot("#pyconjp", the_day, time(13, 0), 1),
            30,
        ),
        t.ScheduledTalk(
            keynote_uuid,
            "Keynote: Day 1 キーノートスピーカー",
            "〇〇で有名な氏による基調講演です",
            None,
            None,
            [],
            t.Slot("#pyconjp", the_day, time(13, 30), 2),
            60,
        ),
        t.ScheduledTalk(
            "203012",
            "トーク2",
            "トーク2の\n詳細です",
            t.Category(
                "Python core and around", "Intermediate", "Japanese", "Both"
            ),
            t.QuestionAnswer("トーク2のエレベータピッチ", "トーク2の前提知識", "トーク2で持ち帰れるもの"),
            [t.Speaker("スピーカー2", "プロフィール of スピーカー2")],
            t.Slot("#pyconjp_2", the_day, time(15, 0), 3),
            30,
        ),
        t.ScheduledTalk(
            "203023",
            "トーク3",
            "トーク3の\n詳細です",
            t.Category(
                "Machine learning", "Advanced", "Japanese", "Japanese only"
            ),
            t.QuestionAnswer("トーク3のエレベータピッチ", "トーク3の前提知識", "トーク3で持ち帰れるもの"),
            [t.Speaker("スピーカー3", "スピーカー3のプロフィール。")],
            t.Slot("#pyconjp_1", the_day, time(15, 0), 3),
            30,
        ),
        t.ScheduledTalk(
            "203001",
            "トーク1",
            "トーク1の\n詳細です",
            t.Category(
                "Web programming", "Beginner", "English", "English only"
            ),
            t.QuestionAnswer("トーク1のエレベータピッチ", "トーク1の前提知識", "トーク1で持ち帰れるもの"),
            [t.Speaker("スピーカー1", "スピーカー1のプロフィール")],
            t.Slot("#pyconjp_1", the_day, time(17, 0), 4),
            30,
        ),
        t.ScheduledTalk(
            "203034",
            "トーク4",
            "トーク4の\n詳細です",
            t.Category(
                "Visual / Game / Music",
                "Intermediate",
                "Japanese",
                "Japanese only",
            ),
            t.QuestionAnswer("トーク4のエレベータピッチ", "トーク4の前提知識", "トーク4で持ち帰れるもの"),
            [t.Speaker("スピーカー4", "プロフィール・オブ・スピーカー4")],
            t.Slot("#pyconjp_2", the_day, time(17, 0), 4),
            30,
        ),
        t.ScheduledTalk(
            closing_uuid,
            "Closing (Day 1)",
            None,
            None,
            None,
            [],
            t.Slot("#pyconjp", the_day, time(18, 45), 5),
            15,
        ),
    ]
)

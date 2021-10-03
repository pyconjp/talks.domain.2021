from datetime import date, time
from unittest import TestCase

from pyconjp_domains import talks as t


class CategoryTestCase(TestCase):
    def test_flatten_raw_json(self):
        categories = [
            {
                "name": "Track",
                "categoryItems": [{"name": "Python core and around"}],
            },
            {
                "name": "Level",
                "categoryItems": [{"name": "Intermediate"}],
            },
            {
                "name": "Language",
                "categoryItems": [{"name": "Japanese"}],
            },
            {
                "name": "発表資料の言語 / Language of presentation material",
                "categoryItems": [{"name": "Both"}],
            },
        ]
        expected = {
            "track": "Python core and around",
            "level": "Intermediate",
            "speaking_language": "Japanese",
            "slide_language": "Both",
        }

        actual = t.Category.flatten_raw_json(categories)

        self.assertEqual(actual, expected)


class CategoryFactoryTestCase(TestCase):
    def setUp(self):
        self.item_to_category_title = {
            80001: "Track",
            80002: "Track",
            80003: "Track",
            80004: "Track",
            80011: "Level",
            80012: "Level",
            80013: "Level",
            80021: "Language",
            80022: "Language",
            80031: "発表資料の言語 / Language of presentation material",
            80032: "発表資料の言語 / Language of presentation material",
        }
        self.category_id_to_name = {
            80001: "Track1",
            80002: "Track2",
            80003: "Track3",
            80004: "Track4",
            80011: "Level1",
            80012: "Level2",
            80013: "Level3",
            80021: "Language1",
            80022: "Language2",
            80031: "Slide Language1",
            80032: "Slide Language2",
        }

    def test_init(self):
        actual = t.CategoryFactory(
            self.item_to_category_title, self.category_id_to_name
        )

        self.assertEqual(
            actual.item_to_category_title, self.item_to_category_title
        )
        self.assertEqual(actual.category_id_to_name, self.category_id_to_name)

    def test_create_from_empty(self):
        sut = t.CategoryFactory(
            self.item_to_category_title, self.category_id_to_name
        )

        actual = sut.create([])

        expected = t.Category(None, None, None, None)
        self.assertEqual(actual, expected)

    def test_create_from_four_values(self):
        sut = t.CategoryFactory(
            self.item_to_category_title, self.category_id_to_name
        )

        actual = sut.create([80004, 80013, 80021, 80032])

        expected = t.Category(
            "Track4", "Level3", "Language1", "Slide Language2"
        )
        self.assertEqual(actual, expected)

    def test_create_from_under_four_values(self):
        sut = t.CategoryFactory(
            self.item_to_category_title, self.category_id_to_name
        )

        actual = sut.create([80013, 80022])

        expected = t.Category(None, "Level3", "Language2", None)
        self.assertEqual(actual, expected)

    def test_from_(self):
        categories_data = [
            {
                "id": 30061,
                "title": "Track",
                "items": [
                    {"id": 80001, "name": "Track1"},
                    {"id": 80002, "name": "Track2"},
                    {"id": 80003, "name": "Track3"},
                    {"id": 80004, "name": "Track4"},
                ],
            },
            {
                "id": 30062,
                "title": "Level",
                "items": [
                    {"id": 80011, "name": "Level1"},
                    {"id": 80012, "name": "Level2"},
                    {"id": 80013, "name": "Level3"},
                ],
            },
            {
                "id": 30063,
                "title": "Language",
                "items": [
                    {"id": 80021, "name": "Language1"},
                    {"id": 80022, "name": "Language2"},
                ],
            },
            {
                "id": 30064,
                "title": "発表資料の言語 / Language of presentation material",
                "items": [
                    {"id": 80031, "name": "Slide Language1"},
                    {"id": 80032, "name": "Slide Language2"},
                ],
            },
        ]

        actual = t.CategoryFactory.from_(categories_data)

        self.assertIsInstance(actual, t.CategoryFactory)
        self.assertEqual(
            actual.item_to_category_title, self.item_to_category_title
        )
        self.assertEqual(actual.category_id_to_name, self.category_id_to_name)


class QuestionAnswerTestCase(TestCase):
    def test_flatten_raw_json(self):
        question_answers = [
            {
                "question": "Elevator Pitch",
                "answer": "このトークはエレガントに示します",
            },
            {
                "question": "オーディエンスが持って帰れる具体的な知識やノウハウ",
                "answer": "〇〇をPythonで行う方法",
            },
            {
                "question": "オーディエンスに求める前提知識",
                "answer": "前提として、〇〇した経験。\r\nこれがあると理解しやすいでしょう",
            },
        ]
        expected = {
            "elevator_pitch": "このトークはエレガントに示します",
            "audience_prior_knowledge": "前提として、〇〇した経験。\r\nこれがあると理解しやすいでしょう",
            "audience_take_away": "〇〇をPythonで行う方法",
        }

        actual = t.QuestionAnswer.flatten_raw_json(question_answers)

        self.assertEqual(actual, expected)


class TalkTestCase(TestCase):
    def setUp(self):
        self.talk = t.Talk(
            123456,
            "Talkのプロパティのテスト",
            "テストテストテスト",
            t.Category(
                "Web programming",
                "Intermediate",
                "Japanese",
                "Japanese only",
            ),
            t.QuestionAnswer(
                "プロパティを作ります",
                "Pythonのunittestを使った経験",
                "テストを先に書いてRed\r\n実装してGreenという体験",
            ),
            [t.Speaker("すごい人", "いくつかのすごい経歴")],
        )

    def test_track(self):
        actual = self.talk.track

        self.assertEqual(actual, "Web programming")

    def test_level(self):
        actual = self.talk.level

        self.assertEqual(actual, "Intermediate")

    def test_speaking_language(self):
        actual = self.talk.speaking_language

        self.assertEqual(actual, "Japanese")

    def test_slide_language(self):
        actual = self.talk.slide_language

        self.assertEqual(actual, "Japanese only")

    def test_elevator_pitch(self):
        actual = self.talk.elevator_pitch

        self.assertEqual(actual, "プロパティを作ります")

    def test_prior_knowledge(self):
        actual = self.talk.prior_knowledge

        self.assertEqual(actual, "Pythonのunittestを使った経験")

    def test_take_away(self):
        actual = self.talk.take_away

        self.assertEqual(actual, "テストを先に書いてRed\r\n実装してGreenという体験")

    def test_speaker_names(self):
        actual = self.talk.speaker_names

        self.assertEqual(actual, ["すごい人"])

    def test_speaker_profiles(self):
        actual = self.talk.speaker_profiles

        self.assertEqual(actual, ["いくつかのすごい経歴"])


class TalksTestCase(TestCase):
    def test_from_raw_json(self):
        data = [
            {
                "questionAnswers": [
                    {
                        "question": "Elevator Pitch",
                        "answer": "エレガントに作ります",
                    },
                    {
                        "question": "オーディエンスが持って帰れる具体的な知識やノウハウ",
                        "answer": "テストを先に書いてRed\r\n実装してGreenという体験",
                    },
                    {
                        "question": "オーディエンスに求める前提知識",
                        "answer": "Pythonのunittestを使った経験",
                    },
                ],
                "id": 123456,
                "title": "Talksを作るテスト",
                "description": "テストテストテスト",
                "speakers": [{"name": "すごい人"}],
                "categories": [
                    {
                        "name": "Track",
                        "categoryItems": [{"name": "Machine learning"}],
                    },
                    {
                        "name": "Level",
                        "categoryItems": [{"name": "Advanced"}],
                    },
                    {
                        "name": "Language",
                        "categoryItems": [{"name": "English"}],
                    },
                    {
                        "name": "発表資料の言語 / Language of presentation material",
                        "categoryItems": [{"name": "English only"}],
                    },
                ],
            }
        ]
        expected = t.Talks(
            [
                t.Talk(
                    123456,
                    "Talksを作るテスト",
                    "テストテストテスト",
                    t.Category(
                        "Machine learning",
                        "Advanced",
                        "English",
                        "English only",
                    ),
                    t.QuestionAnswer(
                        "エレガントに作ります",
                        "Pythonのunittestを使った経験",
                        "テストを先に書いてRed\r\n実装してGreenという体験",
                    ),
                    [t.Speaker("すごい人")],
                )
            ]
        )

        actual = t.Talks.from_raw_json(data)

        self.assertEqual(actual, expected)


class ScheduledTalkTestCase(TestCase):
    def setUp(self):
        self.talk = t.ScheduledTalk(
            123456,
            "ScheduledTalkのプロパティのテスト",
            "テストプロパティテスト",
            t.Category(
                "Web programming",
                "beginner",
                "English",
                "Both",
            ),
            t.QuestionAnswer(
                "継承して属性を追加します",
                "Pythonのunittestを使った経験",
                "テストを先に書いてRed\r\n実装してGreenという体験",
            ),
            [t.Speaker("すごい人", "いくつかのすごい経歴")],
            t.Slot("#pyconjp_1", date(2021, 10, 15), time(13, 30), 2),
            30,
        )
        self.fields = [
            "id",
            "title",
            "room",
            "day",
            "slot_number",
            "elevator_pitch",
            "prior_knowledge",
            "take_away",
            "level",
            "track",
            "speaking_language",
            "slide_language",
            "description",
            "duration_min",
            "speaker_names",
            "speaker_profiles",
        ]

    def test_inheritance(self):
        self.assertIsInstance(self.talk, t.Talk)

    def test_room(self):
        actual = self.talk.room

        self.assertEqual(actual, "#pyconjp_1")

    def test_day(self):
        actual = self.talk.day

        self.assertEqual(actual, date(2021, 10, 15))

    def test_start_time(self):
        actual = self.talk.start_time

        self.assertEqual(actual, time(13, 30))

    def test_slot_number(self):
        actual = self.talk.slot_number

        self.assertEqual(actual, 2)

    def test_as_list(self):
        expected = [
            123456,
            "ScheduledTalkのプロパティのテスト",
            "#pyconjp_1",
            date(2021, 10, 15),
            2,
            "継承して属性を追加します",
            "Pythonのunittestを使った経験",
            "テストを先に書いてRed\r\n実装してGreenという体験",
            "beginner",
            "Web programming",
            "English",
            "Both",
            "テストプロパティテスト",
            30,
            ["すごい人"],
            ["いくつかのすごい経歴"],
        ]

        actual = self.talk.as_list(self.fields)

        self.assertEqual(actual, expected)

    def test_service_session_as_list(self):
        service_session = t.ScheduledTalk(
            "0b9f27cc-9da4-4010-9c8e-9d24d31956d4",
            "Opening (Day1)",
            None,
            None,
            None,
            [],
            t.Slot("plenary", date(2021, 10, 16), time(12, 40), 3),
            30,
        )
        expected = [
            "0b9f27cc-9da4-4010-9c8e-9d24d31956d4",
            "Opening (Day1)",
            "plenary",
            date(2021, 10, 16),
            3,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            30,
            [],
            [],
        ]

        actual = service_session.as_list(self.fields)

        self.assertEqual(actual, expected)


class SlotTestCase(TestCase):
    def test_create(self):
        start_datetime_str = "2021-10-15T15:00:00"
        expected = t.Slot("the_room", date(2021, 10, 15), time(15, 0), 2)

        actual = t.Slot.create("the_room", start_datetime_str, 2)

        self.assertEqual(actual, expected)


class ScheduledTalksTestCase(TestCase):
    def test_sorted(self):
        from .fixtures.talks__scheduled_talks__sorted import expected, talks

        actual = talks.sorted()

        self.assertEqual(actual, expected)

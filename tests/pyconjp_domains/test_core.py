from unittest import TestCase

import pyconjp_domains.core as c


class FilterSessionsTestCase(TestCase):
    def test_filter(self):
        sessions = [
            {"title": "Venue open"},
            {"title": "Opening (Day 1)"},
            {"title": "基調講演"},
            {"title": "スペシャルブース紹介"},
            {"title": "スペシャルブース訪問"},
            {"title": "スロット1・ルーム1のトーク"},
            {"title": "スロット1・ルーム2のトーク"},
            {"title": "Ask the speaker / スペシャルブース"},
            {"title": "スロット2・ルーム1のトーク"},
            {"title": "スロット2・ルーム2のトーク"},
            {"title": "Ask the speaker / スペシャルブース"},
            {"title": "Break"},
            {"title": "Lightning talks"},
            {"title": "Closing (Day1)"},
        ]
        expected = [
            {"title": "Venue open"},
            {"title": "Opening (Day 1)"},
            {"title": "基調講演"},
            {"title": "スロット1・ルーム1のトーク"},
            {"title": "スロット1・ルーム2のトーク"},
            {"title": "スロット2・ルーム1のトーク"},
            {"title": "スロット2・ルーム2のトーク"},
            {"title": "Lightning talks"},
            {"title": "Closing (Day1)"},
        ]

        actual = c.filter_sessions(sessions)

        self.assertEqual(list(actual), expected)


class CreateCategoryIdValueMapTestCase(TestCase):
    def test_create_map(self):
        data = [
            {
                "id": 101,
                "title": "Track",
                "items": [
                    {"id": 2001, "name": "Machine learning"},
                    {"id": 2003, "name": "Web programming"},
                ],
            },
            {
                "id": 123,
                "title": "言語",
                "items": [
                    {"id": 2105, "name": "English"},
                    {"id": 2108, "name": "Japanese"},
                ],
            },
        ]
        expected = {
            2001: "Machine learning",
            2003: "Web programming",
            2105: "English",
            2108: "Japanese",
        }

        actual = c.create_category_id_value_map(data)

        self.assertEqual(actual, expected)


class CreateDateStringToSlotNumberMapTestCase(TestCase):
    def test_create_map(self):
        date_strings = set(
            [
                "2021-10-15T15:00:00",
                "2021-10-15T16:00:00",
                "2021-10-16T15:50:00",
                "2021-10-16T13:50:00",
            ]
        )
        expected = {
            "2021-10-15T15:00:00": 1,
            "2021-10-15T16:00:00": 2,
            "2021-10-16T13:50:00": 1,
            "2021-10-16T15:50:00": 2,
        }

        actual = c.create_date_string_to_slot_number_map(date_strings)

        self.assertEqual(actual, expected)


class DateFromStringTestCase(TestCase):
    def test_return_date(self):
        from datetime import date

        strings = ["2021-10-15T15:00:00", "2021-10-16T15:50:00"]
        expected_dates = [date(2021, 10, 15), date(2021, 10, 16)]

        for string, expected in zip(strings, expected_dates):
            with self.subTest(string=string, expected=expected):
                actual = c.date_from_string(string)

                self.assertEqual(actual, expected)

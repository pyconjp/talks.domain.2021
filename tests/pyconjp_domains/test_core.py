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
            {"title": "スペシャルブース紹介"},
            {"title": "スロット1・ルーム1のトーク"},
            {"title": "スロット1・ルーム2のトーク"},
            {"title": "スロット2・ルーム1のトーク"},
            {"title": "スロット2・ルーム2のトーク"},
            {"title": "Lightning talks"},
            {"title": "Closing (Day1)"},
        ]

        actual = c.filter_sessions(sessions)

        self.assertEqual(list(actual), expected)


class CalculateDurationMinTestCase(TestCase):
    def test_calculate(self):
        start = "2021-10-15T17:00:00"
        end = "2021-10-15T17:30:00"

        actual = c.calculate_duration_min(start, end)

        self.assertEqual(actual, 30)


class CreateTalksFromDataTestCase(TestCase):
    def test_create_talks(self):
        from .fixtures.core__create_talks_from_data import data, expected

        actual = c.create_talks_from_data(data)

        self.assertEqual(actual, expected)

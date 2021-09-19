from unittest import TestCase

import pyconjp_domains.core as c


class FilterSessionsTestCase(TestCase):
    def test_filter(self):
        sessions = [
            {"title": "Venue open"},
            {"title": "Opening (Day 1)"},
            {"title": "基調講演"},
            {"title": "スペシャルブース紹介"},
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

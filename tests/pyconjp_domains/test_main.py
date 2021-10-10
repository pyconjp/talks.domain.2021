from unittest import TestCase

import pyconjp_domains.__main__ as m


class ParseFieldArgumentsTestCase(TestCase):
    def test_no_alias(self):
        arguments = ["id", "title", "slot_number"]

        actual = m.parse_field_arguments(arguments)

        expected = (
            ("id", "title", "slot_number"),
            ("id", "title", "slot_number"),
        )
        self.assertEqual(actual, expected)

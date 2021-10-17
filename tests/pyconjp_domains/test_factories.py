from datetime import date
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pyconjp_domains import factories as f
from pyconjp_domains.talks import ScheduledTalk


class CategoryFactoryTestCase(TestCase):
    def setUp(self):
        from .fixtures.factories__category_factory import (
            item_id_to_category_title,
            item_id_to_name,
        )

        self.item_id_to_category_title = item_id_to_category_title
        self.item_id_to_name = item_id_to_name

    def test_init(self):
        actual = f.CategoryFactory(
            self.item_id_to_category_title, self.item_id_to_name
        )

        self.assertEqual(
            actual._item_id_to_category_title, self.item_id_to_category_title
        )
        self.assertEqual(actual._item_id_to_name, self.item_id_to_name)

    def test_create(self):
        from .fixtures.factories__category_factory import (
            create_expecteds,
            create_parameters,
        )

        sut = f.CategoryFactory(
            self.item_id_to_category_title, self.item_id_to_name
        )

        for parameter, expected in zip(create_parameters, create_expecteds):
            with self.subTest(parameter=parameter, expected=expected):
                actual = sut.create(*parameter)

                self.assertEqual(actual, expected)

    def test_from_(self):
        from .fixtures.factories__category_factory import categories_raw_data

        actual = f.CategoryFactory.from_(categories_raw_data)

        self.assertIsInstance(actual, f.CategoryFactory)
        self.assertEqual(
            actual._item_id_to_category_title, self.item_id_to_category_title
        )
        self.assertEqual(actual._item_id_to_name, self.item_id_to_name)


class QuestionAnswerFactoryTestCase(TestCase):
    def setUp(self):
        from .fixtures.factories__question_answer_factory import (
            question_value_to_id_map,
        )

        self.question_value_to_id_map = question_value_to_id_map

    def test_init(self):
        actual = f.QuestionAnswerFactory(self.question_value_to_id_map)

        self.assertEqual(
            actual._question_value_to_id_map, self.question_value_to_id_map
        )

    def test_create(self):
        from .fixtures.factories__question_answer_factory import (
            create_expected,
            question_answers_data,
        )

        sut = f.QuestionAnswerFactory(self.question_value_to_id_map)

        actual = sut.create(question_answers_data)

        self.assertEqual(actual, create_expected)

    def test_from_(self):
        from .fixtures.factories__question_answer_factory import (
            questions_raw_data,
        )

        actual = f.QuestionAnswerFactory.from_(questions_raw_data)

        self.assertIsInstance(actual, f.QuestionAnswerFactory)
        self.assertEqual(
            actual._question_value_to_id_map, self.question_value_to_id_map
        )


class SlotFactoryTestCase(TestCase):
    def setUp(self):
        from .fixtures.factories__slot_factory import (
            room_id_to_name,
            starts_at_to_slot_number,
        )

        self.room_id_to_name = room_id_to_name
        self.starts_at_to_slot_number = starts_at_to_slot_number

    def test_init(self):
        actual = f.SlotFactory(
            self.room_id_to_name, self.starts_at_to_slot_number
        )

        self.assertEqual(actual._room_id_to_name, self.room_id_to_name)
        self.assertEqual(
            actual._starts_at_to_slot_number, self.starts_at_to_slot_number
        )

    @patch("pyconjp_domains.talks.Slot.create")
    def test_create(self, slot_create):
        from .fixtures.factories__slot_factory import (
            create_assert_calls,
            create_parameters,
        )

        sut = f.SlotFactory(
            self.room_id_to_name, self.starts_at_to_slot_number
        )

        for parameter, assert_call in zip(
            create_parameters, create_assert_calls
        ):
            with self.subTest(parameter=parameter, assert_call=assert_call):
                actual = sut.create(*parameter)

                self.assertEqual(actual, slot_create.return_value)
                slot_create.assert_called_once_with(*assert_call)
                slot_create.reset_mock()

    def test_from_(self):
        from .fixtures.factories__slot_factory import (
            rooms_raw_data,
            starts_at_strings,
        )

        actual = f.SlotFactory.from_(rooms_raw_data, starts_at_strings)

        self.assertIsInstance(actual, f.SlotFactory)
        self.assertEqual(actual._room_id_to_name, self.room_id_to_name)
        self.assertEqual(
            actual._starts_at_to_slot_number, self.starts_at_to_slot_number
        )

    def test_date_from_string(self):
        strings = ["2021-10-15T15:00:00", "2021-10-16T15:50:00"]
        expected_dates = [date(2021, 10, 15), date(2021, 10, 16)]

        for string, expected in zip(strings, expected_dates):
            with self.subTest(string=string, expected=expected):
                actual = f.SlotFactory.date_from_string(string)

                self.assertEqual(actual, expected)

    def test__create_datetime_string_to_slot_number_map(self):
        datetime_strings = set(
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

        actual = f.SlotFactory._create_datetime_string_to_slot_number_map(
            datetime_strings
        )

        self.assertEqual(actual, expected)


class SpeakerFactoryTestCase(TestCase):
    def setUp(self):
        from .fixtures.factories__speaker_factory import id_to_raw_data_map

        self.id_to_raw_data_map = id_to_raw_data_map

    def test_init(self):
        actual = f.SpeakerFactory(self.id_to_raw_data_map)

        self.assertEqual(actual._id_to_raw_data_map, self.id_to_raw_data_map)

    def test_create(self):
        from .fixtures.factories__speaker_factory import (
            create_expected,
            create_target_id,
        )

        sut = f.SpeakerFactory(self.id_to_raw_data_map)

        actual = sut.create(create_target_id)

        self.assertEqual(actual, create_expected)

    def test_from_(self):
        from .fixtures.factories__speaker_factory import speakers_raw_data

        actual = f.SpeakerFactory.from_(speakers_raw_data)

        self.assertIsInstance(actual, f.SpeakerFactory)
        self.assertEqual(actual._id_to_raw_data_map, self.id_to_raw_data_map)


class ScheduledTalkFactoryTestCase(TestCase):
    def setUp(self):
        self.category_factory = MagicMock(spec=f.CategoryFactory)
        self.question_answer_factory = MagicMock(spec=f.QuestionAnswerFactory)
        self.speaker_factory = MagicMock(spec=f.SpeakerFactory)
        self.slot_factory = MagicMock(spec=f.SlotFactory)

        self.sut = f.ScheduledTalkFactory(
            self.category_factory,
            self.question_answer_factory,
            self.speaker_factory,
            self.slot_factory,
        )

    def test_init(self):
        actual = self.sut

        self.assertEqual(actual._category_factory, self.category_factory)
        self.assertEqual(
            actual._question_answer_factory, self.question_answer_factory
        )
        self.assertEqual(actual._speaker_factory, self.speaker_factory)
        self.assertEqual(actual._slot_factory, self.slot_factory)

    def test_calculate_duration_min(self):
        start = "2021-10-15T17:00:00"
        end = "2021-10-15T17:30:00"

        actual = f.ScheduledTalkFactory.calculate_duration_min(start, end)

        self.assertEqual(actual, 30)

    @patch(
        "pyconjp_domains.factories.ScheduledTalkFactory.calculate_duration_min"
    )
    def test_create_service_session(self, calculate_duration_min):
        from .fixtures.factories__scheduled_talk_factory import (
            expected_service_session_kwargs,
            service_session_data,
        )

        expected = ScheduledTalk(
            **expected_service_session_kwargs,
            slot=self.slot_factory.create.return_value,
            duration_min=calculate_duration_min.return_value,
        )

        actual = self.sut.create(service_session_data)

        self.assertEqual(actual, expected)
        self.slot_factory.create.assert_called_once_with(
            service_session_data["startsAt"], service_session_data["roomId"]
        )
        calculate_duration_min.assert_called_once_with(
            service_session_data["startsAt"], service_session_data["endsAt"]
        )

from datetime import date, time

from pyconjp_domains import talks as t

talks = t.ScheduledTalks(
    [
        t.ScheduledTalk(
            "101",
            "トーク1",
            "",
            None,
            None,
            [],
            t.Slot("room2", date(2021, 10, 15), time(16, 0), 3),
            30,
        ),
        t.ScheduledTalk(
            "102",
            "トーク2",
            "",
            None,
            None,
            [],
            t.Slot("room1", date(2021, 10, 15), time(16, 0), 3),
            30,
        ),
        t.ScheduledTalk(
            "103",
            "トーク3",
            "",
            None,
            None,
            [],
            t.Slot("room", date(2021, 10, 16), time(14, 0), 1),
            30,
        ),
        t.ScheduledTalk(
            "104",
            "トーク4",
            "",
            None,
            None,
            [],
            t.Slot("room", date(2021, 10, 15), time(14, 0), 1),
            30,
        ),
    ]
)
expected = t.ScheduledTalks(
    [
        t.ScheduledTalk(
            "104",
            "トーク4",
            "",
            None,
            None,
            [],
            t.Slot("room", date(2021, 10, 15), time(14, 0), 1),
            30,
        ),
        t.ScheduledTalk(
            "102",
            "トーク2",
            "",
            None,
            None,
            [],
            t.Slot("room1", date(2021, 10, 15), time(16, 0), 3),
            30,
        ),
        t.ScheduledTalk(
            "101",
            "トーク1",
            "",
            None,
            None,
            [],
            t.Slot("room2", date(2021, 10, 15), time(16, 0), 3),
            30,
        ),
        t.ScheduledTalk(
            "103",
            "トーク3",
            "",
            None,
            None,
            [],
            t.Slot("room", date(2021, 10, 16), time(14, 0), 1),
            30,
        ),
    ]
)

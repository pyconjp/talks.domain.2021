rooms_raw_data = [
    {"id": 20010, "name": "#pyconjp"},
    {"id": 20001, "name": "#pyconjp_1"},
]
starts_at_strings = set(
    ("2021-10-15T13:00:00", "2021-10-15T13:30:00", "2021-10-15T14:30:00")
)

room_id_to_name = {20010: "#pyconjp", 20001: "#pyconjp_1"}
starts_at_to_slot_number = {
    "2021-10-15T13:00:00": 1,
    "2021-10-15T13:30:00": 2,
    "2021-10-15T14:30:00": 3,
}

create_parameters = (
    ("2021-10-15T13:30:00", 20010),
    ("2021-10-15T12:30:00", 20001),
)
create_assert_calls = (
    ("#pyconjp", "2021-10-15T13:30:00", 2),
    ("#pyconjp_1", "2021-10-15T12:30:00", 0),
)

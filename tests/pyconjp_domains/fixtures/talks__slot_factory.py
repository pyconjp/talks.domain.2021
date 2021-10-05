rooms_raw_data = [
    {"id": 20010, "name": "#pyconjp"},
    {"id": 20001, "name": "#pyconjp_1"},
]
starts_at_strings = set(
    ("2021-10-15T13:00:00", "2021-10-15T13:30:00", "2021-10-15T14:30:00")
)

room_id_to_name = {20010: "#pyconjp", 20001: "#pyconjp_1"}
start_to_slot_number = {
    "2021-10-15T13:00:00": 1,
    "2021-10-15T13:30:00": 2,
    "2021-10-15T14:30:00": 3,
}

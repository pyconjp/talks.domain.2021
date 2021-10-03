from pyconjp_domains.talks import Category

categories_raw_data = [
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

item_id_to_category_title = {
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

item_id_to_name = {
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

create_parameters = ([], [80004, 80013, 80021, 80032], [80013, 80022])

create_expecteds = (
    Category(None, None, None, None),
    Category("Track4", "Level3", "Language1", "Slide Language2"),
    Category(None, "Level3", "Language2", None),
)

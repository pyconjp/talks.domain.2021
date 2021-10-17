import pyconjp_domains.talks as t

id_to_raw_data_map = {
    "3be1e664-95bd-4bf0-bd51-6a642c643379": {
        "id": "3be1e664-95bd-4bf0-bd51-6a642c643379",
        "bio": "スピーカー1のすごい経歴",
        "fullName": "スピーカー1",
    },
    "186683ea-3f6d-4f95-b392-14cbf70758a1": {
        "id": "186683ea-3f6d-4f95-b392-14cbf70758a1",
        "bio": "スピーカー2の輝かしい経歴",
        "fullName": "スピーカー2",
    },
}

create_target_id = "186683ea-3f6d-4f95-b392-14cbf70758a1"
create_expected = t.Speaker("スピーカー2", "スピーカー2の輝かしい経歴")

speakers_raw_data = [
    {
        "id": "3be1e664-95bd-4bf0-bd51-6a642c643379",
        "bio": "スピーカー1のすごい経歴",
        "fullName": "スピーカー1",
    },
    {
        "id": "186683ea-3f6d-4f95-b392-14cbf70758a1",
        "bio": "スピーカー2の輝かしい経歴",
        "fullName": "スピーカー2",
    },
]

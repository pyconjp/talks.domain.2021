service_session_data = {
    "id": "d7eea897-5b5b-4cdb-8388-8af30174a875",
    "title": "サービス・セッション",
    "description": "サービス・セッションを表すテストデータ",
    "startsAt": "2021-10-15T15:00:00",
    "endsAt": "2021-10-15T15:30:00",
    "isServiceSession": True,
    "isPlenumSession": True,
    "speakers": [],
    "categoryItems": [],
    "questionAnswers": [],
    "roomId": 20001,
    "liveUrl": None,
    "recordingUrl": None,
}
expected_service_session_kwargs = {
    "id": "d7eea897-5b5b-4cdb-8388-8af30174a875",
    "title": "サービス・セッション",
    "description": "サービス・セッションを表すテストデータ",
    "category": None,
    "answer": None,
    "speakers": [],
}

talk_data = {
    "id": "203456",
    "title": "トーク",
    "description": "トークを表すテストデータ",
    "startsAt": "2021-10-16T13:30:00",
    "endsAt": "2021-10-16T14:00:00",
    "isServiceSession": False,
    "isPlenumSession": False,
    "speakers": ["c2719407-9d2a-42fc-aae8-2a3a3223f582"],
    "categoryItems": [80546, 80521, 80518, 80533],
    "questionAnswers": [
        {"questionId": 30014, "answerValue": "エレベータピッチ"},
        {"questionId": 30017, "answerValue": "持ち帰れるもの"},
        {"questionId": 30021, "answerValue": "前提知識"},
    ],
    "roomId": 20008,
    "liveUrl": "https://www.slideshare.net/somewhere",
    "recordingUrl": "https://youtu.be/somewhere",
}
expected_talk_kwargs = {
    "id": "203456",
    "title": "トーク",
    "description": "トークを表すテストデータ",
    "slide_url": "https://www.slideshare.net/somewhere",
    "recording_url": "https://youtu.be/somewhere",
}

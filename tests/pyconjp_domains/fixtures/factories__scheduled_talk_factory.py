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

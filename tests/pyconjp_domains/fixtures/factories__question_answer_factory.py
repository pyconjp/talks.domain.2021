from pyconjp_domains.talks import QuestionAnswer

question_value_to_id_map = {
    "Elevator Pitch": 30316,
    "オーディエンスが持って帰れる具体的な知識やノウハウ": 30327,
    "オーディエンスに求める前提知識": 30341,
}

question_answers_data = [
    {"questionId": 30316, "answerValue": "エレベータピッチ"},
    {"questionId": 30327, "answerValue": "持ち帰れるもの"},
    {"questionId": 30341, "answerValue": "前提知識"},
]
create_expected = QuestionAnswer("エレベータピッチ", "前提知識", "持ち帰れるもの")

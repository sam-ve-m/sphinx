import pytest

from src.exceptions.exceptions import InternalServerError
from src.services.builders.suitability.builder import SuitabilityAnswersProfileBuilder


fake_suitability = {
    "questions": [
        {
            "value_text": "primeira pergunta",
            "score": 20,
            "order": 1,
            "answers": [
                {"value_text": "primeira resposta", "weight": 20},
                {"value_text": "segunda resposta xxx", "weight": 25},
                {"value_text": "terceira resposta", "weight": 22},
            ],
        },
        {
            "value_text": "segunda pergunta",
            "score": 20,
            "order": 2,
            "answers": [
                {"value_text": "primeira resposta", "weight": 20},
                {"value_text": "segunda resposta yyy", "weight": 25},
                {"value_text": "terceira resposta", "weight": 22},
            ],
        },
    ],
}


def test_insert_suitability_with_invalid_value():
    builder = SuitabilityAnswersProfileBuilder()
    with pytest.raises(InternalServerError, match="common.process_issue"):
        builder.suitability = None

    with pytest.raises(InternalServerError, match="common.process_issue"):
        builder.suitability = []


def test_insert_suitability_with_valid_value():
    builder = SuitabilityAnswersProfileBuilder()
    builder.suitability = fake_suitability
    assert fake_suitability == fake_suitability


def test_get_questions_with_best_answer_with_fake_suitability():
    builder = SuitabilityAnswersProfileBuilder()
    builder.suitability = fake_suitability
    questions_with_best_answers = (
        builder._SuitabilityAnswersProfileBuilder__get_questions_with_best_answer()
    )
    assert (
        questions_with_best_answers[0]["answer"]
        == fake_suitability["questions"][0]["answers"][1]["value_text"]
    )
    assert (
        questions_with_best_answers[1]["answer"]
        == fake_suitability["questions"][1]["answers"][1]["value_text"]
    )


def test_calc_suitability_score_profile():
    builder = SuitabilityAnswersProfileBuilder()
    builder.suitability = fake_suitability
    questions_with_best_answers = (
        builder._SuitabilityAnswersProfileBuilder__get_questions_with_best_answer()
    )
    score = builder._SuitabilityAnswersProfileBuilder__calc_suitability_score_profile(
        questions_with_best_answers
    )
    assert score == 1.0
    assert type(score) is float


def test_profile_without_suitability():
    builder = SuitabilityAnswersProfileBuilder()
    with pytest.raises(InternalServerError, match="common.process_issue"):
        builder.profile


def test_profile_dictionary_keys_with_suitability():
    builder = SuitabilityAnswersProfileBuilder()
    builder.suitability = fake_suitability
    assert (
        "score"
        and "suitability_version"
        and "suitability_submission_date"
        and "answers" in builder.profile.keys()
    )

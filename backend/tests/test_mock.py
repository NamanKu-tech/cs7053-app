from unittest.mock import patch
from app.seed import seed


def test_grade_returns_score_and_feedback(client, auth_headers, db):
    seed(db)
    res = client.get("/topics/risk-analysis-process/questions", headers=auth_headers)
    question_id = res.json()[0]["id"]

    with patch("app.routers.mock._call_gemini", return_value=(7, "Good answer covering the main steps.")):
        res = client.post("/mock/grade", json={
            "question_id": question_id,
            "answer_text": "I would identify assets, classify risks, design mitigations, and iterate.",
        }, headers=auth_headers)

    assert res.status_code == 200
    assert res.json()["score"] == 7
    assert "feedback" in res.json()


def test_grade_stores_attempt_in_history(client, auth_headers, db):
    seed(db)
    res = client.get("/topics/risk-analysis-process/questions", headers=auth_headers)
    question_id = res.json()[0]["id"]

    with patch("app.routers.mock._call_gemini", return_value=(5, "Adequate.")):
        client.post("/mock/grade", json={"question_id": question_id, "answer_text": "Short answer"}, headers=auth_headers)

    history = client.get(f"/mock/history/{question_id}", headers=auth_headers).json()
    assert len(history) == 1
    assert history[0]["score"] == 5


def test_grade_handles_gemini_failure_gracefully(client, auth_headers, db):
    seed(db)
    res = client.get("/topics/risk-analysis-process/questions", headers=auth_headers)
    question_id = res.json()[0]["id"]

    with patch("app.routers.mock._call_gemini", return_value=(None, "Grading service unavailable. Try again.")):
        res = client.post("/mock/grade", json={"question_id": question_id, "answer_text": "Some answer"}, headers=auth_headers)

    assert res.status_code == 200
    assert res.json()["score"] is None
    assert "unavailable" in res.json()["feedback"]

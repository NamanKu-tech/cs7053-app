from app.seed import seed


def test_list_paths_requires_auth(client):
    res = client.get("/paths")
    assert res.status_code == 403


def test_list_paths_after_seed(client, auth_headers, db):
    seed(db)
    res = client.get("/paths", headers=auth_headers)
    assert res.status_code == 200
    slugs = [p["slug"] for p in res.json()]
    assert "q1-risk-analysis" in slugs
    assert len(res.json()) == 4


def test_path_topics_ordered(client, auth_headers, db):
    seed(db)
    res = client.get("/paths/q1-risk-analysis/topics", headers=auth_headers)
    assert res.status_code == 200
    topics = res.json()
    assert topics[0]["slug"] == "risk-analysis-process"
    assert topics[0]["completed"] == False


def test_toggle_progress_and_reflects_in_listing(client, auth_headers, db):
    seed(db)
    client.post("/topics/risk-analysis-process/progress",
                json={"completed": True}, headers=auth_headers)
    res = client.get("/paths/q1-risk-analysis/topics", headers=auth_headers)
    topic = next(t for t in res.json() if t["slug"] == "risk-analysis-process")
    assert topic["completed"] == True


def test_save_and_retrieve_user_note(client, auth_headers, db):
    seed(db)
    client.patch("/topics/risk-analysis-process/notes/user",
                 json={"content": "My study notes"}, headers=auth_headers)
    res = client.get("/topics/risk-analysis-process/notes/user", headers=auth_headers)
    assert res.json()["content"] == "My study notes"

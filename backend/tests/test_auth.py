def test_register_new_user(client):
    res = client.post("/auth/register", json={"email": "new@example.com", "password": "secret123"})
    assert res.status_code == 201
    assert "access_token" in res.json()


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "secret123"})
    res = client.post("/auth/register", json={"email": "dup@example.com", "password": "different"})
    assert res.status_code == 400


def test_login_valid(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "pass123"})
    res = client.post("/auth/login", json={"email": "user@example.com", "password": "pass123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "correct"})
    res = client.post("/auth/login", json={"email": "user@example.com", "password": "wrong"})
    assert res.status_code == 401


def test_health_no_auth_required(client):
    res = client.get("/health")
    assert res.status_code == 200

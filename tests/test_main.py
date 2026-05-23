import random
import string

import pytest


def rand_id():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=5))


@pytest.mark.asyncio
async def test_register_user(client):
    uid = rand_id()
    payload = {
        "username": f"user_{uid}",
        "password": "pass123",
        "email": f"test_{uid}@mail.com",
    }
    r = await client.post("/api/v1/users/register", json=payload)
    # ✅ Принимаем и 200, и 201
    assert r.status_code in [200, 201]
    data = r.json()
    assert data["username"] == payload["username"]


@pytest.mark.asyncio
async def test_register_duplicate_user(client):
    uid = rand_id()
    username = f"dup_{uid}"
    payload = {
        "username": username,
        "password": "pass123",
        "email": f"dup_{uid}@mail.com",
    }
    r1 = await client.post("/api/v1/users/register", json=payload)
    assert r1.status_code in [200, 201]

    r2 = await client.post("/api/v1/users/register", json=payload)
    # ✅ Дубликат должен вернуть 400 или 409
    assert r2.status_code in [400, 409]


@pytest.mark.asyncio
async def test_login_user_success(client):
    uid = rand_id()
    # Регистрируем
    await client.post(
        "/api/v1/users/register",
        json={
            "username": f"login_{uid}",
            "password": "pass123",
            "email": f"login_{uid}@mail.com",
        },
    )
    # Логинимся
    r = await client.post(
        "/api/v1/users/login", json={"username": f"login_{uid}", "password": "pass123"}
    )
    assert r.status_code == 200
    assert "access_token" in r.json()


@pytest.mark.asyncio
async def test_login_user_incorrect_password(client):
    uid = rand_id()
    username = f"bad_{uid}"
    await client.post(
        "/api/v1/users/register",
        json={
            "username": username,
            "password": "correct",
            "email": f"bad_{uid}@mail.com",
        },
    )
    r = await client.post(
        "/api/v1/users/login", json={"username": username, "password": "wrong"}
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_login_user_not_found(client):
    r = await client.post(
        "/api/v1/users/login",
        json={"username": f"noexist_{rand_id()}", "password": "any"},
    )
    assert r.status_code == 401

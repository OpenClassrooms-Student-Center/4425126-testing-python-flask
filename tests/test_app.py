""" App integration test """

import pytest
from app import create_app
from utilities import clear_all


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    clear_all()
    with app.test_client() as client:
        yield client


def _create_user(client, name, email, password):
    rv = client.post(
        "/register",
        data=dict(name=name, email=email, password=password),
        follow_redirects=True,
    )
    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find("Register User") == -1


def _login_user(client, email, password):
    rv = client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )
    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find("Login User") == -1


def _logout_user(client):
    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200


def test_home_without_login(client):
    rv = client.get("/", follow_redirects=True)
    data = rv.data.decode()
    assert data.find("Login User") != -1


def test_register_user_success(client):
    _create_user(client, "kashif", "email@gmail.com", "password")


def test_register_user_bad_input(client):
    rv = client.post("/register", follow_redirects=True)
    assert rv.status_code == 400


def test_register_user_email_exists(client):
    _create_user(client, "kashif", "email@gmail.com", "password")
    _logout_user(client)
    rv = client.post(
        "/register",
        data=dict(name="kashif", email="email@gmail.com", password="password"),
        follow_redirects=True,
    )
    assert rv.status_code == 403


def test_login_user_success(client):
    _create_user(client, "kashif", "email@gmail.com", "password")
    _logout_user(client)
    _login_user(client, "email@gmail.com", "password")


def test_login_user_invalid_credentials(client):
    rv = client.post(
        "/login",
        data=dict(email="abc@gmail.com", password="password"),
        follow_redirects=True,
    )
    assert rv.status_code == 403


def test_login_user_bad_data(client):
    rv = client.post("/login", follow_redirects=True)
    assert rv.status_code == 400


def test_calculation_hex(client):
    _create_user(client, "kashif", "email@gmail.com", "password")
    rv = client.post("/", data=dict(input="A", base="16"))
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("<p><b>Decimal:</b> 10</p>") != -1
    assert data.find("<p><b>Hexadecimal:</b> A</p>") != -1
    assert data.find("<p><b>Binary:</b> 1010</p>") != -1


def test_calculation_dec(client):
    _create_user(client, "kashif", "email@gmail.com", "password")
    rv = client.post("/", data=dict(input="10", base="10"))
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("<p><b>Decimal:</b> 10</p>") != -1
    assert data.find("<p><b>Hexadecimal:</b> A</p>") != -1
    assert data.find("<p><b>Binary:</b> 1010</p>") != -1


def test_calculation_bin(client):
    _create_user(client, "kashif", "email@gmail.com", "password")
    rv = client.post("/", data=dict(input="1010", base="2"))
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("<p><b>Decimal:</b> 10</p>") != -1
    assert data.find("<p><b>Hexadecimal:</b> A</p>") != -1
    assert data.find("<p><b>Binary:</b> 1010</p>") != -1


def test_calculation_bad_data(client):
    _create_user(client, "kashif", "email@gmail.com", "password")
    rv = client.post("/", data=dict(input="10", base="10A"))
    rv.data.decode()
    assert rv.status_code == 400


def test_history(client):
    _create_user(client, "kashif", "email@gmail.com", "password")
    rv = client.post("/", data=dict(input="ABCD", base="16"))
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("<p><b>Hexadecimal:</b> ABCD</p>") != -1

    rv = client.get("/dashboard")
    data = rv.data.decode()
    assert rv.status_code == 200
    assert data.find("ABCD") != -1

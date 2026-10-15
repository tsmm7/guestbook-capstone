from fastapi.testclient import TestClient

import main

# без `with` lifespan не запускается, подключение к БД не нужно
client = TestClient(main.app)


class FakeResult:
    def fetchall(self):
        return [("Ann", "hello")]


class FakeConn:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, *args, **kwargs):
        return FakeResult()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_index_returns_greeting():
    r = client.get("/")
    assert r.json() == {"message": "test"}


def test_list_messages(monkeypatch):
    monkeypatch.setattr(main, "connect", lambda: FakeConn())
    r = client.get("/messages")
    assert r.json() == [{"author": "Ann", "text": "hello"}]


def test_add_message(monkeypatch):
    monkeypatch.setattr(main, "connect", lambda: FakeConn())
    r = client.post("/messages", json={"author": "Ann", "text": "hi"})
    assert r.json() == {"ok": True}

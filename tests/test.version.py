from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_version():
    assert client.get("/version").json() == {"version": "1.1.0"}
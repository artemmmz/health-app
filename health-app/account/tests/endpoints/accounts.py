from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app=app)


class TestSignUp:
    @staticmethod
    def test_signup_correct():
        response = client.post('/api/authentication/signup', json={})

        print(response.json())

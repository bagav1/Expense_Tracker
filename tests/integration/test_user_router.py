import pytest


class TestRouterUser:
    def test_create_user(client):
        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer "},
        )
        assert response.status_code == 401
        assert response.json() == []

        response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "name": "Full Name Test",
                "password": "test",
            },
        )
        assert response.status_code == 200
        assert response.json().get("email") == "test@example.com"

        auth = client.post(
            "/auth/login/access-token",
            json={"username": "test@example.com", "password": "test"},
        )
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        response = client.get(
            f"/users/{response.json().get('user_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "user_id": response.json().get("user_id"),
            "name": "Full Name Test",
            "email": "test@test.com",
            "password": "hidden",
        }

        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

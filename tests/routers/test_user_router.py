class TestRouterUser:
    user = {
        "email": "test@example.com",
        "name": "Full Name Test",
        "password": "test",
    }
    credentials = {"username": "test@example.com", "password": "test"}

    def test_create_user(self, client):
        response = client.get("/users/", headers={"Authorization": f"Bearer "})
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}

        response = client.post("/users/", json=self.user)
        assert response.status_code == 200
        assert response.json().get("email") == "test@example.com"

    def test_get_user(self, client):
        new_user = client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        response = client.get(
            f"/users/{new_user.json().get('user_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "user_id": response.json().get("user_id"),
            "name": self.user.get("name"),
            "email": self.user.get("email"),
            "password": "hidden",
        }

    def test_get_all_users(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0].get("password") == "hidden"

    def test_update_user(self, client):
        new_user = client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        response = client.put(
            f"/users/{new_user.json().get('user_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={"name": "Updated Name", "email": self.user.get("email")},
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Updated Name"

        response = client.get(
            f"/users/{new_user.json().get('user_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Updated Name"

    def test_delete_user(self, client):
        new_user = client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        response = client.delete(
            f"/users/{new_user.json().get('user_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "user_id": new_user.json().get("user_id"),
            "name": self.user.get("name"),
            "email": self.user.get("email"),
            "password": "hidden",
        }

        response = client.get(
            f"/users/{new_user.json().get('user_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

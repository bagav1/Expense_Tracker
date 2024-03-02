class TestRouterCategory:
    user = {
        "email": "test@example.com",
        "name": "Full Name Test",
        "password": "test",
    }
    credentials = {"username": "test@example.com", "password": "test"}

    category = {
        "category_name": "Test Category",
        "category_type": "income",
    }

    def test_create_category(self, client):
        new_user = client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        response = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )
        assert response.status_code == 200
        assert response.json().get("category_name") == "Test Category"
        assert response.json().get("category_type") == "income"
        assert response.json().get("user_id") == new_user.json().get("user_id")

    def test_get_category(self, client):
        new_user = client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        response = client.get(
            f"/categories/{new_category.json().get('category_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )

        assert response.status_code == 200
        assert response.json().get("category_name") == "Test Category"
        assert response.json().get("category_type") == "income"

    def test_get_all_categories(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        response = client.get(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0].get("category_name") == "Test Category"
        assert response.json()[0].get("category_type") == "income"

    def test_update_category(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        response = client.put(
            f"/categories/{new_category.json().get('category_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={**self.category, **{"category_name": "Updated Category"}},
        )

        assert response.status_code == 200
        assert response.json().get("category_name") == "Updated Category"

    def test_delete_category(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        response = client.delete(
            f"/categories/{new_category.json().get('category_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )

        assert response.status_code == 200
        assert response.json().get("category_id") == new_category.json().get(
            "category_id"
        )

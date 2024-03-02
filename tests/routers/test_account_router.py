class TestRouterAccount:
    user = {
        "email": "test@example.com",
        "name": "Full Name Test",
        "password": "test",
    }
    credentials = {"username": "test@example.com", "password": "test"}
    account = {
        "account_name": "Test Account",
        "account_type": "savings",
        "initial_balance": 500.0,
        "currency": "COP",
    }

    def test_create_account(self, client):
        new_user = client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        response = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )
        assert response.status_code == 200
        assert response.json().get("account_name") == "Test Account"
        assert response.json().get("user_id") == new_user.json().get("user_id")

    def test_get_account(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        response = client.get(
            f"/accounts/{new_account.json().get('account_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert response.json().get("account_name") == "Test Account"

    def test_get_all_accounts(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        response = client.get(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_update_account(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        response = client.put(
            f"/accounts/{new_account.json().get('account_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={**self.account, **{"account_name": "Updated Account"}},
        )
        assert response.status_code == 200
        assert response.json().get("account_name") == "Updated Account"

    def test_delete_account(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        response = client.delete(
            f"/accounts/{new_account.json().get('account_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )

        assert response.status_code == 200
        assert response.json().get("account_id") == new_account.json().get("account_id")
        assert response.json().get("account_name") == "Test Account"

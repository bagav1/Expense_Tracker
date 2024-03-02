class TestRouterTransaction:
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
    category = {
        "category_name": "Test Category",
        "category_type": "income",
    }
    transaction = {
        "date": "2022-01-01",
        "description": "Test Transaction",
        "amount": 100.0,
        "transaction_type": "income",
        "notes": "Test Notes",
    }
    # account_id: str = Field(title="Account Transaction")
    # category_id: str = Field(title="Category Transaction")

    def test_create_transaction(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        response = client.post(
            "/transactions/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={
                "account_id": new_account.json().get("account_id"),
                "category_id": new_category.json().get("category_id"),
                **self.transaction,
            },
        )
        assert response.status_code == 200
        assert response.json().get("transaction_id") is not None

    def test_get_transaction(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        new_transaction = client.post(
            "/transactions/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={
                "account_id": new_account.json().get("account_id"),
                "category_id": new_category.json().get("category_id"),
                **self.transaction,
            },
        )

        response = client.get(
            f"/transactions/{new_transaction.json().get('transaction_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert response.json().get("transaction_id") == new_transaction.json().get(
            "transaction_id"
        )

    def test_get_all_transactions(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        client.post(
            "/transactions/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={
                "account_id": new_account.json().get("account_id"),
                "category_id": new_category.json().get("category_id"),
                **self.transaction,
            },
        )

        response = client.get(
            "/transactions/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_update_transaction(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        new_transaction = client.post(
            "/transactions/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={
                "account_id": new_account.json().get("account_id"),
                "category_id": new_category.json().get("category_id"),
                **self.transaction,
            },
        )

        response = client.put(
            f"/transactions/{new_transaction.json().get('transaction_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={
                **self.transaction,
                "account_id": new_account.json().get("account_id"),
                "category_id": new_category.json().get("category_id"),
                **{"notes": "Updated Notes"},
            },
        )
        assert response.status_code == 200
        assert response.json().get("notes") == "Updated Notes"

    def test_delete_transaction(self, client):
        client.post("/users/", json=self.user)
        auth = client.post("/auth/login/access-token", data=self.credentials)
        assert auth.status_code == 200
        assert auth.json().get("token_type") == "bearer"

        new_account = client.post(
            "/accounts/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.account,
        )

        new_category = client.post(
            "/categories/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json=self.category,
        )

        new_transaction = client.post(
            "/transactions/",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
            json={
                "account_id": new_account.json().get("account_id"),
                "category_id": new_category.json().get("category_id"),
                **self.transaction,
            },
        )

        response = client.delete(
            f"/transactions/{new_transaction.json().get('transaction_id')}",
            headers={"Authorization": f"Bearer {auth.json().get('access_token')}"},
        )
        assert response.status_code == 200
        assert response.json().get("transaction_id") == new_transaction.json().get(
            "transaction_id"
        )

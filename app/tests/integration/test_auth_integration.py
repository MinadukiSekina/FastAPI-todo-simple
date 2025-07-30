"""
認証機能の統合テスト

このモジュールは、Todoエンドポイントでの認証動作を確認する
統合テストを提供します。
"""

from datetime import timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response
from pytest_mock import MockerFixture
from sqlmodel import Session

from app.infrastructure.db import get_session
from app.routers import auth, todo, user


def get_test_app(session: Session) -> FastAPI:
    """テスト用のFastAPIアプリケーションを作成"""
    app = FastAPI()

    # 必要なルーターをすべて含める
    app.include_router(todo.router)
    app.include_router(auth.router)
    app.include_router(user.router)

    # データベースセッションの依存性を上書き
    app.dependency_overrides[get_session] = lambda: session

    return app


def make_request(
    client: TestClient,
    method: str,
    endpoint: str,
    data: dict | None = None,
    headers: dict | None = None,
) -> Response:
    """HTTPリクエストを実行するヘルパー関数"""
    if method == "GET":
        return client.get(endpoint, headers=headers)
    elif method == "POST":
        return client.post(endpoint, json=data or {}, headers=headers)
    elif method == "PUT":
        return client.put(endpoint, json=data or {}, headers=headers)
    elif method == "DELETE":
        return client.delete(endpoint, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")


# =============================================================================
# 正常ケースのテスト
# =============================================================================


class TestTodoAuthIntegrationSuccessCases:
    """Todoエンドポイントでの認証動作の統合テスト（正常ケース）"""

    # =============================================================================
    # ログインしてTodoエンドポイント(/todos)にアクセスするテスト
    # =============================================================================

    def test_login_and_access_todos_with_valid_token(
        self,
        get_test_session: Session,
    ) -> None:
        """有効なJWTトークンでログインしてTodoエンドポイント(/todos)にアクセスするテスト"""
        app = get_test_app(get_test_session)

        client = TestClient(app)

        # テストユーザーを作成
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 200

        # テストユーザーでログイン
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # APIを呼び出し
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/todos", headers=headers)

        # 結果を検証
        assert response.status_code == 200

    # =============================================================================
    # ログインしてTodoエンドポイント(/todos)にアクセスして作成するテスト
    # =============================================================================

    def test_login_and_create_todo_with_valid_token(
        self,
        get_test_session: Session,
    ) -> None:
        """有効なJWTトークンでログインしてTodoエンドポイント(/todos)にアクセスして作成するテスト"""
        app = get_test_app(get_test_session)

        client = TestClient(app)

        # テストユーザーを作成
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        user_id = response.json()["id"]

        # テストユーザーでログイン
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # ヘッダーを設定
        headers = {"Authorization": f"Bearer {token}"}

        # テストユーザーでTodoを作成
        todo_data = {
            "title": "testtodo",
            "description": "testdescription",
            "completed": False,
            "user_id": user_id,
        }
        response = client.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 200

    # =============================================================================
    # ログインしてTodoエンドポイント(/todos/{todo_id})にアクセスするテスト
    # =============================================================================

    def test_login_and_access_todo_with_valid_token(
        self,
        get_test_session: Session,
    ) -> None:
        """有効なJWTトークンでログインしてTodoエンドポイント(/todos/{todo_id})にアクセスするテスト"""
        app = get_test_app(get_test_session)

        client = TestClient(app)

        # テストユーザーを作成
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        user_id = response.json()["id"]

        # テストユーザーでログイン
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # ヘッダーを設定
        headers = {"Authorization": f"Bearer {token}"}

        # テストユーザーでTodoを作成
        todo_data = {
            "title": "testtodo",
            "description": "testdescription",
            "completed": False,
            "user_id": user_id,
        }
        response = client.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 200

        # 作成したTodoのIDを取得
        todo_id = response.json()["id"]
        # 作成したTodoのデータにIDを追加
        todo_data["id"] = todo_id

        # APIを呼び出し
        response = client.get(f"/todos/{todo_id}", headers=headers)

        # 結果を検証
        assert response.status_code == 200

    # =============================================================================
    # ログインしてTodoエンドポイント(/todos/{todo_id})にアクセスして更新するテスト
    # =============================================================================

    def test_login_and_update_todo_with_valid_token(
        self,
        get_test_session: Session,
    ) -> None:
        """有効なJWTトークンでログインしてTodoエンドポイント(/todos/{todo_id})にアクセスして更新するテスト"""
        app = get_test_app(get_test_session)

        client = TestClient(app)

        # テストユーザーを作成
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        user_id = response.json()["id"]

        # テストユーザーでログイン
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # ヘッダーを設定
        headers = {"Authorization": f"Bearer {token}"}

        # テストユーザーでTodoを作成
        todo_data = {
            "title": "testtodo",
            "description": "testdescription",
            "completed": False,
            "user_id": user_id,
        }
        response = client.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 200

        # 作成したTodoのIDを取得
        todo_id = response.json()["id"]

        # 更新するデータ
        update_data = {
            "title": "updatedtodo",
            "description": "updateddescription",
            "completed": True,
            "user_id": user_id,
            "id": todo_id,
        }

        # APIを呼び出し
        response = client.put(f"/todos/{todo_id}", json=update_data, headers=headers)

        # 結果を検証
        assert response.status_code == 200

    # =============================================================================
    # ログインしてTodoエンドポイント(/todos/{todo_id})にアクセスして削除するテスト
    # =============================================================================

    def test_login_and_delete_todo_with_valid_token(
        self,
        get_test_session: Session,
    ) -> None:
        """有効なJWTトークンでログインしてTodoエンドポイント(/todos/{todo_id})にアクセスして削除するテスト"""
        app = get_test_app(get_test_session)

        client = TestClient(app)

        # テストユーザーを作成
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        user_id = response.json()["id"]

        # テストユーザーでログイン
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # ヘッダーを設定
        headers = {"Authorization": f"Bearer {token}"}

        # テストユーザーでTodoを作成
        todo_data = {
            "title": "testtodo",
            "description": "testdescription",
            "completed": False,
            "user_id": user_id,
        }
        response = client.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 200

        # 作成したTodoのIDを取得
        todo_id = response.json()["id"]

        # APIを呼び出し
        response = client.delete(f"/todos/{todo_id}", headers=headers)

        # 結果を検証
        assert response.status_code == 200


# =============================================================================
# 異常ケースのテスト
# =============================================================================


class TestTodoAuthIntegrationErrorCases:
    """Todoエンドポイントでの認証動作の統合テスト（異常ケース）"""

    # =============================================================================
    # トークンがない場合のテスト
    # =============================================================================

    @pytest.mark.parametrize(
        "method, endpoint, data",
        [
            pytest.param("GET", "/todos", None, id="get_todos"),
            pytest.param("GET", "/todos/1", None, id="get_todo"),
            pytest.param(
                "POST",
                "/todos",
                {
                    "title": "test",
                    "description": "test",
                    "completed": False,
                    "user_id": 1,
                },
                id="post_todo",
            ),
            pytest.param("PUT", "/todos/1", {"title": "updated"}, id="put_todo"),
            pytest.param("DELETE", "/todos/1", None, id="delete_todo"),
            pytest.param("GET", "/auth/me", None, id="get_me"),
        ],
    )
    def test_access_todos_without_token(
        self,
        get_test_session: Session,
        method: str,
        endpoint: str,
        data: dict | None,
    ) -> None:
        """トークンがない場合のテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # ヘルパー関数を使用してAPIを呼び出し
        response = make_request(client, method, endpoint, data)

        # 結果を検証
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    # =============================================================================
    # トークンが無効な場合のテスト
    # =============================================================================

    @pytest.mark.parametrize(
        "method, endpoint, data",
        [
            pytest.param("GET", "/todos", None, id="get_todos"),
            pytest.param("GET", "/todos/1", None, id="get_todo"),
            pytest.param(
                "POST",
                "/todos",
                {
                    "title": "test",
                    "description": "test",
                    "completed": False,
                    "user_id": 1,
                },
                id="post_todo",
            ),
            pytest.param("PUT", "/todos/1", {"title": "updated"}, id="put_todo"),
            pytest.param("DELETE", "/todos/1", None, id="delete_todo"),
            pytest.param("GET", "/auth/me", None, id="get_me"),
        ],
    )
    def test_access_todos_with_invalid_token(
        self,
        get_test_session: Session,
        method: str,
        endpoint: str,
        data: dict | None,
    ) -> None:
        """トークンが無効な場合のテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # ヘルパー関数を使用してAPIを呼び出し（無効なトークン付き）
        headers = {"Authorization": "Bearer invalid_token"}
        response = make_request(client, method, endpoint, data, headers)

        # 結果を検証
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    # =============================================================================
    # トークンが期限切れの場合のテスト
    # =============================================================================

    @pytest.mark.parametrize(
        "method, endpoint, data",
        [
            pytest.param("GET", "/todos", None, id="get_todos"),
            pytest.param("GET", "/todos/1", None, id="get_todo"),
            pytest.param(
                "POST",
                "/todos",
                {
                    "title": "test",
                    "description": "test",
                    "completed": False,
                    "user_id": 1,
                },
                id="post_todo",
            ),
            pytest.param("PUT", "/todos/1", {"title": "updated"}, id="put_todo"),
            pytest.param("DELETE", "/todos/1", None, id="delete_todo"),
            pytest.param("GET", "/auth/me", None, id="get_me"),
        ],
    )
    def test_access_todos_with_expired_token(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
        method: str,
        endpoint: str,
        data: dict | None,
    ) -> None:
        """トークンが期限切れの場合のテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # テストユーザーを作成
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 200

        # テストユーザーでログイン
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        # JWTの有効期限を過去に設定
        mocker.patch(
            "app.usecases.auth_usecase.get_token_expires_delta",
            return_value=timedelta(seconds=-1),  # 1秒前に期限切れ
        )

        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # ヘルパー関数を使用してAPIを呼び出し（期限切れのトークン付き）
        headers = {"Authorization": f"Bearer {token}"}
        response = make_request(client, method, endpoint, data, headers)

        # 結果を検証
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    # =============================================================================
    # 認証情報が無効の場合のテスト
    # =============================================================================

    def test_access_todos_with_invalid_credentials(
        self,
        get_test_session: Session,
    ) -> None:
        """認証情報が無効の場合のテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # 無効な認証情報でログイン
        login_data = {
            "username": "invalid_username",
            "password": "invalid_password",
        }

        response = client.post("/auth/token", data=login_data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

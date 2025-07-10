import pytest
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.infrastructure.db import get_session
from app.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from app.routers.todo import router
from app.usecases.todoUsecase import TodoUsecase


def get_test_app(session: Session) -> FastAPI:
    """テスト用のFastAPIアプリケーションを作成"""
    app = FastAPI()
    app.include_router(router)

    # データベースセッションの依存性を上書き
    app.dependency_overrides[get_session] = lambda: session

    return app


# =============================================================================
# 正常ケースのテスト
# =============================================================================


class TestTodoRouterSuccessCases:
    # =============================================================================
    # GET /todos エンドポイントの正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_todo_data, expected_todo",
        [
            # 登録が0件
            pytest.param(
                [],
                [],
                id="no_todos",
            ),
            # 登録が1件
            pytest.param(
                [TodoCreate(title="test", description="test", completed=False)],
                [TodoRead(id=1, title="test", description="test", completed=False)],
                id="one_todo",
            ),
            # 登録が複数件
            pytest.param(
                [
                    TodoCreate(title="test", description="test", completed=False),
                    TodoCreate(title="test2", description="test2", completed=True),
                ],
                [
                    TodoRead(id=1, title="test", description="test", completed=False),
                    TodoRead(id=2, title="test2", description="test2", completed=True),
                ],
                id="multiple_todos",
            ),
        ],
        indirect=["create_test_todo_data"],
    )
    def test_get_todos(
        self,
        get_test_session: Session,
        create_test_todo_data: list[Todo],
        expected_todo: list[TodoRead],
    ) -> None:
        """GET /todos エンドポイントのテスト"""
        # テスト用アプリケーションを作成
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.get("/todos")

        # 結果を検証
        assert response.status_code == 200
        assert response.json() == jsonable_encoder(expected_todo)

    # =============================================================================
    # GET /todos/{todo_id} エンドポイントの正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data, expected_todo",
        [
            # 登録が1件
            pytest.param(
                1,
                [TodoCreate(title="test", description="test", completed=False)],
                TodoRead(id=1, title="test", description="test", completed=False),
                id="one_todo",
            ),
            # 登録が複数件
            pytest.param(
                1,
                [
                    TodoCreate(title="test", description="test", completed=False),
                    TodoCreate(title="test2", description="test2", completed=True),
                ],
                TodoRead(id=1, title="test", description="test", completed=False),
                id="multiple_todos",
            ),
        ],
        indirect=["create_test_todo_data"],
    )
    def test_get_todo(
        self,
        todo_id: int,
        get_test_session: Session,
        create_test_todo_data: list[Todo],
        expected_todo: TodoRead,
    ) -> None:
        """GET /todos/{todo_id} エンドポイントのテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.get(f"/todos/{todo_id}")

        # 結果を検証
        assert response.status_code == 200
        assert response.json() == jsonable_encoder(expected_todo)

    # =============================================================================
    # POST /todos エンドポイントの正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_create, expected_todo",
        [
            pytest.param(
                TodoCreate(title="test", description="test", completed=False),
                TodoRead(id=1, title="test", description="test", completed=False),
                id="create_todo",
            ),
            pytest.param(
                TodoCreate(title="test", description="test", completed=True),
                TodoRead(id=1, title="test", description="test", completed=True),
                id="create_todo_completed",
            ),
        ],
    )
    def test_create_todo(
        self,
        get_test_session: Session,
        todo_create: TodoCreate,
        expected_todo: TodoRead,
    ) -> None:
        """POST /todos エンドポイントのテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.post("/todos", json=jsonable_encoder(todo_create))

        # 結果を検証
        assert response.status_code == 200
        assert response.json() == jsonable_encoder(expected_todo)

    # =============================================================================
    # PUT /todos/{todo_id} エンドポイントの正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data, todo_update, expected_todo",
        [
            # タイトルのみ更新
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                TodoUpdate(title="updated"),
                TodoRead(id=1, title="updated", description="description", completed=False),
                id="update_todo_title",
            ),
            # 説明のみ更新
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                TodoUpdate(description="updated"),
                TodoRead(id=1, title="title", description="updated", completed=False),
                id="update_todo_description",
            ),
            # 完了状態のみ更新
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                TodoUpdate(completed=True),
                TodoRead(id=1, title="title", description="description", completed=True),
                id="update_todo_completed",
            ),
            # 全フィールドの更新
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                TodoUpdate(title="updated", description="updated", completed=True),
                TodoRead(id=1, title="updated", description="updated", completed=True),
                id="update_todo_all_fields",
            ),
        ],
        indirect=["create_test_todo_data"],
    )
    def test_update_todo(
        self,
        get_test_session: Session,
        todo_id: int,
        create_test_todo_data: list[Todo],
        todo_update: TodoUpdate,
        expected_todo: TodoRead,
    ) -> None:
        app = get_test_app(get_test_session)
        client = TestClient(app)
        # APIを呼び出し（exclude_unset=Trueを使用してNone値を除外）
        response = client.put(f"/todos/{todo_id}", json=todo_update.model_dump(exclude_unset=True))

        # 結果を検証
        assert response.status_code == 200
        assert response.json() == jsonable_encoder(expected_todo)

    # =============================================================================
    # DELETE /todos/{todo_id} エンドポイントの正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data",
        [
            pytest.param(
                1,
                [TodoCreate(title="test", description="test", completed=False)],
                id="delete_todo_in_single_todo",
            ),
            pytest.param(
                2,
                [
                    TodoCreate(title="test", description="test", completed=False),
                    TodoCreate(title="test2", description="test2", completed=False),
                ],
                id="delete_todo_in_multiple_todos",
            ),
        ],
        indirect=["create_test_todo_data"],
    )
    def test_delete_todo(
        self,
        get_test_session: Session,
        todo_id: int,
        create_test_todo_data: list[Todo],
    ) -> None:
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.delete(f"/todos/{todo_id}")

        # 結果を検証
        assert response.status_code == 200
        assert response.json() is True


class TestTodoRouterErrorCases:
    # =============================================================================
    # 異常ケースのテスト
    # =============================================================================

    # =============================================================================
    # GET /todos/{todo_id} エンドポイントの404エラーケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_id, expected_error_message",
        [
            pytest.param(999, "Todo with id 999 not found", id="not_found"),
            pytest.param(0, "Todo with id 0 not found", id="invalid_id"),
            pytest.param(-1, "Todo with id -1 not found", id="negative_id"),
        ],
    )
    def test_get_todo_not_found(
        self,
        get_test_session: Session,
        todo_id: int,
        expected_error_message: str,
    ) -> None:
        """GET /todos/{todo_id} エンドポイントの404エラーテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.get(f"/todos/{todo_id}")

        # 結果を検証
        assert response.status_code == 404
        assert response.json() == {"detail": expected_error_message}

    # =============================================================================
    # PUT /todos/{todo_id} エンドポイントの404エラーケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_id, expected_error_message",
        [
            pytest.param(999, "Todo with id 999 not found", id="not_found"),
            pytest.param(0, "Todo with id 0 not found", id="invalid_id"),
            pytest.param(-1, "Todo with id -1 not found", id="negative_id"),
        ],
    )
    def test_update_todo_not_found(
        self,
        get_test_session: Session,
        todo_id: int,
        expected_error_message: str,
    ) -> None:
        """PUT /todos/{todo_id} エンドポイントの404エラーテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.put(
            f"/todos/{todo_id}", json=TodoUpdate(title="updated").model_dump(exclude_unset=True)
        )

        # 結果を検証
        assert response.status_code == 404
        assert response.json() == {"detail": expected_error_message}

    # =============================================================================
    # DELETE /todos/{todo_id} エンドポイントの404エラーケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_id, expected_error_message",
        [
            pytest.param(999, "Todo with id 999 not found", id="not_found"),
            pytest.param(0, "Todo with id 0 not found", id="invalid_id"),
            pytest.param(-1, "Todo with id -1 not found", id="negative_id"),
        ],
    )
    def test_delete_todo_not_found(
        self,
        get_test_session: Session,
        todo_id: int,
        expected_error_message: str,
    ) -> None:
        """DELETE /todos/{todo_id} エンドポイントの404エラーテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.delete(f"/todos/{todo_id}")

        # 結果を検証
        assert response.status_code == 404
        assert response.json() == {"detail": expected_error_message}

    # =============================================================================
    # PUT /todos/{todo_id} エンドポイントのバリデーションエラーケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data, update_data, expected_error_message",
        [
            # 明示的にNone値を送信（タイトル）
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                {"title": None},
                "title cannot be null",
                id="explicit_none_title",
            ),
            # 明示的にNone値を送信（説明）
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                {"description": None},
                "description cannot be null",
                id="explicit_none_description",
            ),
            # 空文字列（タイトル）
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                {"title": ""},
                "title is required",
                id="empty_string_title",
            ),
            # 空文字列（説明）
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                {"description": ""},
                "description is required",
                id="empty_string_description",
            ),
            # 空白のみ（タイトル）
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                {"title": "   "},
                "title is required",
                id="whitespace_only_title",
            ),
            # 空白のみ（説明）
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                {"description": "   "},
                "description is required",
                id="whitespace_only_description",
            ),
            # 混在するケース（有効な値とNone値）
            pytest.param(
                1,
                [TodoCreate(title="title", description="description", completed=False)],
                {"title": "updated", "description": None},
                "description cannot be null",
                id="mixed_valid_and_none",
            ),
        ],
        indirect=["create_test_todo_data"],
    )
    def test_update_todo_validation_errors(
        self,
        get_test_session: Session,
        todo_id: int,
        create_test_todo_data: list[Todo],
        update_data: dict[str, str | None],
        expected_error_message: str,
    ) -> None:
        """PUT /todos/{todo_id} エンドポイントのバリデーションエラーテスト"""
        app = get_test_app(get_test_session)
        client = TestClient(app)

        # APIを呼び出し
        response = client.put(f"/todos/{todo_id}", json=update_data)

        # 結果を検証
        assert response.status_code == 422
        # バリデーションエラーメッセージを確認
        error_detail = response.json()["detail"]
        assert any(expected_error_message in str(error) for error in error_detail)

    # =============================================================================
    # POST /todos エンドポイントのIntegrityErrorケースのテスト
    # =============================================================================
    def test_create_todo_integrity_error(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        """POST /todos エンドポイントのIntegrityErrorテスト"""
        # モックのTodoUsecaseを作成
        mock_usecase = mocker.Mock(spec=TodoUsecase)
        mock_usecase.create_todo.side_effect = IntegrityError(
            "INSERT statement failed", "params", orig=Exception("Original error")
        )

        # アプリケーションを作成し、依存関係を上書き
        app = get_test_app(get_test_session)
        app.dependency_overrides[TodoUsecase] = lambda: mock_usecase
        client = TestClient(app)

        # APIを呼び出し
        todo_create = TodoCreate(title="test", description="test", completed=False)
        response = client.post("/todos", json=jsonable_encoder(todo_create))

        # 結果を検証
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Failed to create todo due to data constraint violation"
        }

    # =============================================================================
    # PUT /todos/{todo_id} エンドポイントのIntegrityErrorケースのテスト
    # =============================================================================
    def test_update_todo_integrity_error(
        self,
        get_test_session: Session,
        mocker: MockerFixture,
    ) -> None:
        """PUT /todos/{todo_id} エンドポイントのIntegrityErrorテスト"""
        # モックのTodoUsecaseを作成
        mock_usecase = mocker.Mock(spec=TodoUsecase)
        mock_usecase.update_todo.side_effect = IntegrityError(
            "UPDATE statement failed", "params", orig=Exception("Original error")
        )

        # アプリケーションを作成し、依存関係を上書き
        app = get_test_app(get_test_session)
        app.dependency_overrides[TodoUsecase] = lambda: mock_usecase
        client = TestClient(app)

        # APIを呼び出し
        todo_update = TodoUpdate(title="updated")
        response = client.put(
            "/todos/1", json=jsonable_encoder(todo_update.model_dump(exclude_unset=True))
        )

        # 結果を検証
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Failed to update todo due to data constraint violation"
        }

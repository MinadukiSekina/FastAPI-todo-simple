from typing import ClassVar

import pytest
from _pytest.mark import ParameterSet
from sqlmodel import Session

from app.infrastructure.auth import get_password_hash
from app.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate

# ruff: F401
# テスト用に参照だけ追加
from app.models.user import User
from app.repositories.todo_repository import TodoRepository

# =============================================================================
# 正常ケースのテスト
# =============================================================================


class TestTodoRepositorySuccessCases:
    # =============================================================================
    # get_all_todos()の正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, create_test_todo_data, user_id, expected_todos",
        [
            # 登録が0件
            pytest.param(
                [],
                [],
                1,
                [],
                id="no_todos",
            ),
            # 登録が1件
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                1,
                [TodoRead(id=1, title="test", description="test", completed=False, user_id=1)],
                id="one_todo",
            ),
            # 登録が複数件（すべて同じユーザー）
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                ],
                [
                    TodoCreate(title="test", description="test", completed=False, user_id=1),
                    TodoCreate(title="test2", description="test2", completed=False, user_id=1),
                    TodoCreate(title="test3", description="test3", completed=True, user_id=1),
                ],
                1,
                [
                    TodoRead(id=1, title="test", description="test", completed=False, user_id=1),
                    TodoRead(id=2, title="test2", description="test2", completed=False, user_id=1),
                    TodoRead(id=3, title="test3", description="test3", completed=True, user_id=1),
                ],
                id="multiple_todos",
            ),
            # 登録が複数件（異なるユーザー）
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                    {
                        "id": 2,
                        "username": "test2",
                        "email": "test2@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                ],
                [
                    TodoCreate(title="test", description="test", completed=False, user_id=1),
                    TodoCreate(title="test2", description="test2", completed=False, user_id=2),
                    TodoCreate(title="test3", description="test3", completed=True, user_id=1),
                ],
                1,
                [
                    TodoRead(id=1, title="test", description="test", completed=False, user_id=1),
                    TodoRead(id=3, title="test3", description="test3", completed=True, user_id=1),
                ],
                id="multiple_todos_different_user",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_get_all_todos_success_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        create_test_todo_data: list[Todo],
        user_id: int,
        expected_todos: list[TodoRead],
    ) -> None:
        """get_all_todos()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todos = repository.get_all_todos(user_id)

        # 結果を検証
        assert todos == expected_todos

    # =============================================================================
    # create_todo()の正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, todo_create, expected_todo",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                TodoCreate(title="test", description="test", completed=False, user_id=1),
                TodoRead(id=1, title="test", description="test", completed=False, user_id=1),
                id="create_todo",
            ),
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                TodoCreate(title="test2", description="test2", completed=True, user_id=1),
                TodoRead(id=1, title="test2", description="test2", completed=True, user_id=1),
                id="create_todo_completed",
            ),
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                TodoCreate(title="test3", description="test3", user_id=1),
                TodoRead(id=1, title="test3", description="test3", completed=False, user_id=1),
                id="create_todo_default_completed",
            ),
        ],
        indirect=["create_test_user_data"],
    )
    def test_create_todo_success_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_create: TodoCreate,
        expected_todo: TodoRead,
    ) -> None:
        """create_todo()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todo = repository.create_todo(todo_create)

        # 結果を検証
        assert todo == expected_todo

    # =============================================================================
    # _get_todo_by_id()の正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, todo_id, create_test_todo_data, user_id, expected_todo",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                1,
                Todo(id=1, title="test", description="test", completed=False, user_id=1),
                id="get_todo_in_single_todo",
            ),
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                2,
                [
                    TodoCreate(title="test", description="test", completed=False, user_id=1),
                    TodoCreate(title="test2", description="test2", completed=False, user_id=1),
                ],
                1,
                Todo(id=2, title="test2", description="test2", completed=False, user_id=1),
                id="get_todo_in_multiple_todos",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_get_todo_by_id_success_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        create_test_todo_data: list[Todo],
        todo_id: int,
        user_id: int,
        expected_todo: Todo,
    ) -> None:
        """_get_todo_by_id()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todo = repository._get_todo_by_id(todo_id, user_id)

        # 結果を検証
        assert todo == expected_todo

    # =============================================================================
    # get_todo()の正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, todo_id, create_test_todo_data, user_id, expected_todo",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                1,
                TodoRead(id=1, title="test", description="test", completed=False, user_id=1),
                id="get_todo_in_single_todo",
            ),
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                2,
                [
                    TodoCreate(title="test", description="test", completed=False, user_id=1),
                    TodoCreate(title="test2", description="test2", completed=False, user_id=1),
                ],
                1,
                TodoRead(id=2, title="test2", description="test2", completed=False, user_id=1),
                id="get_todo_in_multiple_todos",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_get_todo_success_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_id: int,
        create_test_todo_data: list[Todo],
        user_id: int,
        expected_todo: TodoRead,
    ) -> None:
        """get_todo()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todo = repository.get_todo(todo_id, user_id)

        # 結果を検証
        assert todo == expected_todo

    # =============================================================================
    # update_todo()の正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        """create_test_user_data, todo_id, create_test_todo_data, \
        todo_update, user_id, expected_todo""",
        [
            # タイトルのみ更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(title="updated", user_id=1),
                1,
                TodoRead(id=1, title="updated", description="test", completed=False, user_id=1),
                id="update_todo_title",
            ),
            # 説明のみ更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(description="updated", user_id=1),
                1,
                TodoRead(id=1, title="test", description="updated", completed=False, user_id=1),
                id="update_todo_description",
            ),
            # 完了状態のみ更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(completed=True, user_id=1),
                1,
                TodoRead(id=1, title="test", description="test", completed=True, user_id=1),
                id="update_todo_completed",
            ),
            # タイトルと完了状態のみ更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(title="updated", completed=True, user_id=1),
                1,
                TodoRead(id=1, title="updated", description="test", completed=True, user_id=1),
                id="update_todo_title_and_completed",
            ),
            # タイトルと説明のみ更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(title="updated", description="updated", user_id=1),
                1,
                TodoRead(id=1, title="updated", description="updated", completed=False, user_id=1),
                id="update_todo_title_and_description",
            ),
            # 説明と完了状態のみ更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(description="updated", completed=True, user_id=1),
                1,
                TodoRead(id=1, title="test", description="updated", completed=True, user_id=1),
                id="update_todo_description_and_completed",
            ),
            # すべて更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(title="updated", description="updated", completed=True, user_id=1),
                1,
                TodoRead(id=1, title="updated", description="updated", completed=True, user_id=1),
                id="update_todo_all",
            ),
            # 複数件ある内の１つの更新
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                2,
                [
                    TodoCreate(title="test", description="test", completed=False, user_id=1),
                    TodoCreate(title="test2", description="test2", completed=False, user_id=1),
                ],
                TodoUpdate(completed=True, user_id=1),
                1,
                TodoRead(id=2, title="test2", description="test2", completed=True, user_id=1),
                id="update_todo_multiple_one",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_update_todo_success_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_id: int,
        create_test_todo_data: list[Todo],
        user_id: int,
        todo_update: TodoUpdate,
        expected_todo: TodoRead,
    ) -> None:
        """update_todo()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todo = repository.update_todo(todo_id, todo_update, user_id)

        # 結果を検証
        assert todo == expected_todo

    # =============================================================================
    # delete_todo()の正常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, todo_id, create_test_todo_data, user_id",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                1,
                id="delete_todo_in_single_todo",
            ),
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    }
                ],
                2,
                [
                    TodoCreate(title="test", description="test", completed=False, user_id=1),
                    TodoCreate(title="test2", description="test2", completed=False, user_id=1),
                ],
                1,
                id="delete_todo_in_multiple_todos",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_delete_todo_success_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_id: int,
        create_test_todo_data: list[Todo],
        user_id: int,
    ) -> None:
        """delete_todo()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        result = repository.delete_todo(todo_id, user_id)

        # 戻り値の検証：Trueが返されることを確認
        assert result is True

        # 削除の検証：対象のTodoが実際に削除されていることを確認
        with pytest.raises(ValueError):
            repository.get_todo(todo_id, user_id)


# =============================================================================
# 異常ケースのテスト
# =============================================================================


class TestTodoRepositoryErrorCases:
    """TodoRepositoryの異常ケースのテスト"""

    # 異常ケース用のデータ。各ケースで使いまわすためにクラス変数に定義
    todo_error_data: ClassVar[list[ParameterSet]] = [
        pytest.param(999, 1, "Todo with id 999 not found", id="not_found"),
        pytest.param(0, 1, "Todo with id 0 not found", id="invalid_id"),
        pytest.param(-1, 1, "Todo with id -1 not found", id="negative_id"),
    ]

    # =============================================================================
    # _get_todo_by_id()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, user_id, error_message", todo_error_data)
    def test_get_todo_by_id_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        user_id: int,
        error_message: str,
    ) -> None:
        """_get_todo_by_id()の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository._get_todo_by_id(todo_id, user_id)

    # =============================================================================
    # get_todo()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, user_id, error_message", todo_error_data)
    def test_get_todo_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        user_id: int,
        error_message: str,
    ) -> None:
        """get_todo()の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository.get_todo(todo_id, user_id)

    # =============================================================================
    # update_todo()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, user_id, error_message", todo_error_data)
    def test_update_todo_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        user_id: int,
        error_message: str,
    ) -> None:
        """update_todo()の異常ケースのテスト"""
        todo_update = TodoUpdate(title="updated")
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository.update_todo(todo_id, todo_update, user_id)

    # =============================================================================
    # delete_todo()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, user_id, error_message", todo_error_data)
    def test_delete_todo_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        user_id: int,
        error_message: str,
    ) -> None:
        """delete_todo()の異常ケースのテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository.delete_todo(todo_id, user_id)

    # =============================================================================
    # get_todoで違うユーザーのTodoを取得しようとした場合の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, todo_id, create_test_todo_data, user_id, expected_error_message",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                    {
                        "id": 2,
                        "username": "test2",
                        "email": "test2@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                2,
                "Todo with id 1 not found",
                id="get_todo_different_user",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_get_todo_different_user_error_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_id: int,
        create_test_todo_data: list[Todo],
        user_id: int,
        expected_error_message: str,
    ) -> None:
        """get_todoで違うユーザーのTodoを取得しようとした場合の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)
        with pytest.raises(ValueError, match=expected_error_message):
            repository.get_todo(todo_id, user_id)

    # =============================================================================
    # get_todo_by_idで違うユーザーのTodoを取得しようとした場合の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, todo_id, create_test_todo_data, user_id, expected_error_message",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                    {
                        "id": 2,
                        "username": "test2",
                        "email": "test2@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                2,
                "Todo with id 1 not found",
                id="get_todo_by_id_different_user",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_get_todo_by_id_different_user_error_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_id: int,
        create_test_todo_data: list[Todo],
        user_id: int,
        expected_error_message: str,
    ) -> None:
        """get_todo_by_idで違うユーザーのTodoを取得しようとした場合の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)
        with pytest.raises(ValueError, match=expected_error_message):
            repository.get_todo_by_id(todo_id, user_id)

    # =============================================================================
    # update_todoで違うユーザーのTodoを更新しようとした場合の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        """create_test_user_data, todo_id, create_test_todo_data, \
        todo_update, user_id, expected_error_message""",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                    {
                        "id": 2,
                        "username": "test2",
                        "email": "test2@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                TodoUpdate(title="updated", user_id=2),
                2,
                "Todo with id 1 not found",
                id="update_todo_different_user",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_update_todo_different_user_error_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_id: int,
        create_test_todo_data: list[Todo],
        todo_update: TodoUpdate,
        user_id: int,
        expected_error_message: str,
    ) -> None:
        """update_todoで違うユーザーのTodoを更新しようとした場合の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)
        with pytest.raises(ValueError, match=expected_error_message):
            repository.update_todo(todo_id, todo_update, user_id)

    # =============================================================================
    # delete_todoで違うユーザーのTodoを削除しようとした場合の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize(
        "create_test_user_data, todo_id, create_test_todo_data, user_id, expected_error_message",
        [
            pytest.param(
                [
                    {
                        "id": 1,
                        "username": "test",
                        "email": "test@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                    {
                        "id": 2,
                        "username": "test2",
                        "email": "test2@example.com",
                        "disabled": False,
                        "hashed_password": get_password_hash("password"),
                    },
                ],
                1,
                [TodoCreate(title="test", description="test", completed=False, user_id=1)],
                2,
                "Todo with id 1 not found",
                id="delete_todo_different_user",
            ),
        ],
        indirect=["create_test_user_data", "create_test_todo_data"],
    )
    def test_delete_todo_different_user_error_cases(
        self,
        get_test_session: Session,
        create_test_user_data: list[User],
        todo_id: int,
        create_test_todo_data: list[Todo],
        user_id: int,
        expected_error_message: str,
    ) -> None:
        """delete_todoで違うユーザーのTodoを削除しようとした場合の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)
        with pytest.raises(ValueError, match=expected_error_message):
            repository.delete_todo(todo_id, user_id)

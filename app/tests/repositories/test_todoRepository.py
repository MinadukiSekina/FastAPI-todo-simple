from typing import ClassVar

import pytest
from _pytest.mark import ParameterSet
from sqlmodel import Session

from app.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from app.repositories.todoRepository import TodoRepository

# =============================================================================
# 正常ケースのテスト
# =============================================================================


class TestTodoRepositorySuccessCases:
    # =============================================================================
    # get_all_todos()の正常ケースのテスト
    # =============================================================================

    # get_all_todos()の正常ケースのテスト用データ
    get_all_todos_success_data: ClassVar[list[ParameterSet]] = [
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
                TodoCreate(title="test2", description="test2", completed=False),
                TodoCreate(title="test3", description="test3", completed=True),
            ],
            [
                TodoRead(id=1, title="test", description="test", completed=False),
                TodoRead(id=2, title="test2", description="test2", completed=False),
                TodoRead(id=3, title="test3", description="test3", completed=True),
            ],
            id="multiple_todos",
        ),
    ]

    # get_all_todos()の正常ケースのテスト
    @pytest.mark.parametrize(
        "create_test_todo_data, expected_todos",
        get_all_todos_success_data,
        indirect=["create_test_todo_data"],
    )
    def test_get_all_todos_success_cases(
        self,
        get_test_session: Session,
        create_test_todo_data: list[Todo],
        expected_todos: list[TodoRead],
    ) -> None:
        """get_all_todos()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todos = repository.get_all_todos()

        # 結果を検証
        assert todos == expected_todos

    # =============================================================================
    # create_todo()の正常ケースのテスト
    # =============================================================================

    # create_todo()の正常ケースのテスト用データ
    create_todo_success_data: ClassVar[list[ParameterSet]] = [
        pytest.param(
            TodoCreate(title="test", description="test", completed=False),
            TodoRead(id=1, title="test", description="test", completed=False),
            id="create_todo",
        ),
    ]

    # create_todo()の正常ケースのテスト
    @pytest.mark.parametrize(
        "todo_create, expected_todo",
        create_todo_success_data,
    )
    def test_create_todo_success_cases(
        self,
        get_test_session: Session,
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
    # _get_todo_by_id()の異常ケースのテスト
    # =============================================================================

    # _get_todo_by_id()の異常ケースのテスト用データ
    _get_todo_by_id_error_data: ClassVar[list[ParameterSet]] = [
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            Todo(id=1, title="test", description="test", completed=False),
            id="get_todo",
        ),
        pytest.param(
            2,
            [
                TodoCreate(title="test", description="test", completed=False),
                TodoCreate(title="test2", description="test2", completed=False),
            ],
            Todo(id=2, title="test2", description="test2", completed=False),
            id="get_todo_multiple",
        ),
    ]

    # _get_todo_by_id()の正常ケースのテスト
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data, expected_todo",
        _get_todo_by_id_error_data,
        indirect=["create_test_todo_data"],
    )
    def test_get_todo_by_id_success_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        create_test_todo_data: list[Todo],
        expected_todo: Todo,
    ) -> None:
        """_get_todo_by_id()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todo = repository._get_todo_by_id(todo_id)

        # 結果を検証
        assert todo == expected_todo

    # =============================================================================
    # get_todo()の正常ケースのテスト
    # =============================================================================

    # get_todo()の正常ケースのテスト用データ
    get_todo_success_data: ClassVar[list[ParameterSet]] = [
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoRead(id=1, title="test", description="test", completed=False),
            id="get_todo",
        ),
        pytest.param(
            2,
            [
                TodoCreate(title="test", description="test", completed=False),
                TodoCreate(title="test2", description="test2", completed=False),
            ],
            TodoRead(id=2, title="test2", description="test2", completed=False),
            id="get_todo_multiple",
        ),
    ]

    # get_todo()の正常ケースのテスト
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data, expected_todo",
        get_todo_success_data,
        indirect=["create_test_todo_data"],
    )
    def test_get_todo_success_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        create_test_todo_data: list[Todo],
        expected_todo: TodoRead,
    ) -> None:
        """get_todo()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todo = repository.get_todo(todo_id)

        # 結果を検証
        assert todo == expected_todo

    # =============================================================================
    # update_todo()の正常ケースのテスト
    # =============================================================================

    # update_todo()の正常ケースのテスト用データ
    update_todo_success_data: ClassVar[list[ParameterSet]] = [
        # タイトルのみ更新
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoUpdate(title="updated"),
            TodoRead(id=1, title="updated", description="test", completed=False),
            id="update_todo_title",
        ),
        # 説明のみ更新
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoUpdate(description="updated"),
            TodoRead(id=1, title="test", description="updated", completed=False),
            id="update_todo_description",
        ),
        # 完了状態のみ更新
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoUpdate(completed=True),
            TodoRead(id=1, title="test", description="test", completed=True),
            id="update_todo_completed",
        ),
        # タイトルと完了状態のみ更新
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoUpdate(title="updated", completed=True),
            TodoRead(id=1, title="updated", description="test", completed=True),
            id="update_todo_title_and_completed",
        ),
        # タイトルと説明のみ更新
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoUpdate(title="updated", description="updated"),
            TodoRead(id=1, title="updated", description="updated", completed=False),
            id="update_todo_title_and_description",
        ),
        # 説明と完了状態のみ更新
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoUpdate(description="updated", completed=True),
            TodoRead(id=1, title="test", description="updated", completed=True),
            id="update_todo_description_and_completed",
        ),
        # すべて更新
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            TodoUpdate(title="updated", description="updated", completed=True),
            TodoRead(id=1, title="updated", description="updated", completed=True),
            id="update_todo_all",
        ),
        # 複数件ある内の１つの更新
        pytest.param(
            2,
            [
                TodoCreate(title="test", description="test", completed=False),
                TodoCreate(title="test2", description="test2", completed=False),
            ],
            TodoUpdate(completed=True),
            TodoRead(id=2, title="test2", description="test2", completed=True),
            id="update_todo_multiple_one",
        ),
    ]

    # update_todo()の正常ケースのテスト
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data, todo_update, expected_todo",
        update_todo_success_data,
        indirect=["create_test_todo_data"],
    )
    def test_update_todo_success_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        create_test_todo_data: list[Todo],
        todo_update: TodoUpdate,
        expected_todo: TodoRead,
    ) -> None:
        """update_todo()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        todo = repository.update_todo(todo_id, todo_update)

        # 結果を検証
        assert todo == expected_todo

    # =============================================================================
    # delete_todo()の正常ケースのテスト
    # =============================================================================

    # delete_todo()の正常ケースのテスト用データ
    delete_todo_success_data: ClassVar[list[ParameterSet]] = [
        pytest.param(
            1,
            [TodoCreate(title="test", description="test", completed=False)],
            None,
            id="delete_todo",
        ),
        pytest.param(
            2,
            [
                TodoCreate(title="test", description="test", completed=False),
                TodoCreate(title="test2", description="test2", completed=False),
            ],
            None,
            id="delete_todo_multiple",
        ),
    ]

    # delete_todo()の正常ケースのテスト
    @pytest.mark.parametrize(
        "todo_id, create_test_todo_data, expected_todo",
        delete_todo_success_data,
        indirect=["create_test_todo_data"],
    )
    def test_delete_todo_success_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        create_test_todo_data: list[Todo],
        expected_todo: None,
    ) -> None:
        """delete_todo()をテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        # メソッドを実行
        repository.delete_todo(todo_id)

        # 結果を検証
        with pytest.raises(ValueError):
            repository.get_todo(todo_id)


# =============================================================================
# 異常ケースのテスト
# =============================================================================


class TestTodoRepositoryErrorCases:
    """TodoRepositoryの異常ケースのテスト"""

    todo_error_data: ClassVar[list[ParameterSet]] = [
        pytest.param(999, "Todo with id 999 not found", id="not_found"),
        pytest.param(0, "Todo with id 0 not found", id="invalid_id"),
        pytest.param(-1, "Todo with id -1 not found", id="negative_id"),
    ]

    # =============================================================================
    # _get_todo_by_id()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, error_message", todo_error_data)
    def test_get_todo_by_id_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        error_message: str,
    ) -> None:
        """_get_todo_by_id()の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository._get_todo_by_id(todo_id)

    # =============================================================================
    # get_todo()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, error_message", todo_error_data)
    def test_get_todo_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        error_message: str,
    ) -> None:
        """get_todo()の異常ケースのテスト"""
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository.get_todo(todo_id)

    # =============================================================================
    # update_todo()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, error_message", todo_error_data)
    def test_update_todo_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        error_message: str,
    ) -> None:
        """update_todo()の異常ケースのテスト"""
        todo_update = TodoUpdate(title="updated")
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository.update_todo(todo_id, todo_update)

    # =============================================================================
    # delete_todo()の異常ケースのテスト
    # =============================================================================
    @pytest.mark.parametrize("todo_id, error_message", todo_error_data)
    def test_delete_todo_error_cases(
        self,
        get_test_session: Session,
        todo_id: int,
        error_message: str,
    ) -> None:
        """delete_todo()の異常ケースのテスト"""
        # リポジトリを作成
        repository = TodoRepository(get_test_session)

        with pytest.raises(ValueError, match=error_message):
            repository.delete_todo(todo_id)

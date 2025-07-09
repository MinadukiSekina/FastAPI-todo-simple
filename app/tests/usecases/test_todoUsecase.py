from typing import ClassVar

import pytest
from pytest_mock import MockerFixture

from app.models.todo import TodoCreate, TodoRead, TodoUpdate
from app.usecases.todoUsecase import TodoUsecase


class TestTodoUsecase:
    """TodoUsecaseのテストクラス"""

    # =============================================================================
    # get_todos()の正常ケースのテスト
    # =============================================================================

    # get_todos()の正常ケースのテスト用データ
    todos_data: ClassVar[list[list[TodoRead]]] = [
        # 空のリスト
        [],
        # 単一のTodo
        [TodoRead(id=1, title="test", description="test", completed=False)],
        # 複数のTodo
        [
            TodoRead(id=1, title="task1", description="desc1", completed=False),
            TodoRead(id=2, title="task2", description="desc2", completed=True),
            TodoRead(id=3, title="task3", description="desc3", completed=False),
        ],
    ]

    @pytest.mark.parametrize("todos_data", todos_data)
    def test_get_todos_success_cases(
        self,
        mocker: MockerFixture,
        todos_data: list[TodoRead],
    ) -> None:
        """get_todos()の正常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()
        mock_repository.get_all_todos.return_value = todos_data

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        result = usecase.get_todos()

        # 結果を検証
        assert result == todos_data

        # モックの呼び出しを検証
        mock_repository.get_all_todos.assert_called_once()

    # =============================================================================
    # get_todo()の正常ケースのテスト
    # =============================================================================

    # get_todo()の正常ケースのテスト用データ
    get_todo_success_data: ClassVar[list[tuple[int, TodoRead]]] = [
        (1, TodoRead(id=1, title="test", description="test", completed=False)),
        (999, TodoRead(id=999, title="important", description="urgent task", completed=True)),
    ]

    @pytest.mark.parametrize("todo_id, expected_todo", get_todo_success_data)
    def test_get_todo_success_cases(
        self,
        mocker: MockerFixture,
        todo_id: int,
        expected_todo: TodoRead,
    ) -> None:
        """get_todo()の正常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()
        mock_repository.get_todo.return_value = expected_todo

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        result = usecase.get_todo(todo_id)

        # 結果を検証
        assert result == expected_todo

        # モックの呼び出しを検証
        mock_repository.get_todo.assert_called_once_with(todo_id)

    # create_todo()の正常ケースのテスト用データ
    create_todo_success_data: ClassVar[list[tuple[TodoCreate, TodoRead]]] = [
        (
            TodoCreate(title="new task", description="new description"),
            TodoRead(id=1, title="new task", description="new description", completed=False),
        ),
        (
            TodoCreate(title="new task", description="new description", completed=False),
            TodoRead(id=1, title="new task", description="new description", completed=False),
        ),
        (
            TodoCreate(title="urgent", description="do it now", completed=True),
            TodoRead(id=2, title="urgent", description="do it now", completed=True),
        ),
    ]

    @pytest.mark.parametrize("todo_create,expected_todo", create_todo_success_data)
    def test_create_todo_success_cases(
        self,
        mocker: MockerFixture,
        todo_create: TodoCreate,
        expected_todo: TodoRead,
    ) -> None:
        """create_todo()の正常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()
        mock_repository.create_todo.return_value = expected_todo

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        result = usecase.create_todo(todo_create)

        # 結果を検証
        assert result == expected_todo

        # モックの呼び出しを検証
        mock_repository.create_todo.assert_called_once_with(todo_create)

    # =============================================================================
    # update_todo()の正常ケースのテスト
    # =============================================================================

    # update_todo()の正常ケースのテスト用データ
    update_todo_success_data: ClassVar[list[tuple[int, TodoUpdate, TodoRead]]] = [
        (
            1,
            TodoUpdate(title="updated"),
            TodoRead(id=1, title="updated", description="old desc", completed=False),
        ),
        (
            2,
            TodoUpdate(completed=True),
            TodoRead(id=2, title="old title", description="old desc", completed=True),
        ),
    ]

    @pytest.mark.parametrize("todo_id,todo_update,expected_todo", update_todo_success_data)
    def test_update_todo_success_cases(
        self,
        mocker: MockerFixture,
        todo_id: int,
        todo_update: TodoUpdate,
        expected_todo: TodoRead,
    ) -> None:
        """update_todo()の正常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()
        mock_repository.update_todo.return_value = expected_todo

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        result = usecase.update_todo(todo_id, todo_update)

        # 結果を検証
        assert result == expected_todo

        # モックの呼び出しを検証
        mock_repository.update_todo.assert_called_once_with(todo_id, todo_update)

    # =============================================================================
    # delete_todo()の正常ケースのテスト
    # =============================================================================

    # delete_todo()の正常ケースのテスト用データ
    delete_todo_success_data: ClassVar[list[int]] = [1, 999]

    @pytest.mark.parametrize("todo_id", delete_todo_success_data)
    def test_delete_todo_success_cases(self, mocker: MockerFixture, todo_id: int) -> None:
        """delete_todo()の正常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()
        mock_repository.delete_todo.return_value = None

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        result = usecase.delete_todo(todo_id)

        # 結果を検証
        assert result is None

        # モックの呼び出しを検証
        mock_repository.delete_todo.assert_called_once_with(todo_id)

    # =============================================================================
    # 異常ケースのテスト
    # =============================================================================

    # =============================================================================
    # get_todo()の異常ケースのテスト
    # =============================================================================

    # get_todo()の異常ケースのテスト用データ
    get_todo_error_data: ClassVar[list[tuple[int, str]]] = [
        (999, "Todo not found"),
        (0, "Invalid ID"),
        (-1, "Negative ID not allowed"),
    ]

    @pytest.mark.parametrize("todo_id,error_message", get_todo_error_data)
    def test_get_todo_error_cases(
        self,
        mocker: MockerFixture,
        todo_id: int,
        error_message: str,
    ) -> None:
        """get_todo()の異常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()
        mock_repository.get_todo.side_effect = ValueError(error_message)

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        with pytest.raises(ValueError, match=error_message):
            usecase.get_todo(todo_id)

        # モックの呼び出しを検証
        mock_repository.get_todo.assert_called_once_with(todo_id)

    # =============================================================================
    # update_todo()の異常ケースのテスト
    # =============================================================================

    # update_todo()の異常ケースのテスト用データ
    update_todo_error_data: ClassVar[list[tuple[int, TodoUpdate, str]]] = [
        (999, TodoUpdate(title="updated"), "Todo not found"),
        (0, TodoUpdate(completed=True), "Invalid ID"),
        (-1, TodoUpdate(title="test"), "Negative ID not allowed"),
    ]

    @pytest.mark.parametrize("todo_id,todo_update,error_message", update_todo_error_data)
    def test_update_todo_error_cases(
        self,
        mocker: MockerFixture,
        todo_id: int,
        todo_update: TodoUpdate,
        error_message: str,
    ) -> None:
        """update_todo()の異常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()

        # モックのside_effectを設定
        mock_repository.update_todo.side_effect = ValueError(error_message)

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        with pytest.raises(ValueError, match=error_message):
            usecase.update_todo(todo_id, todo_update)

        # モックの呼び出しを検証
        mock_repository.update_todo.assert_called_once_with(todo_id, todo_update)

    # =============================================================================
    # delete_todo()の異常ケースのテスト
    # =============================================================================

    # delete_todo()の異常ケースのテスト用データ
    delete_todo_error_data: ClassVar[list[tuple[int, str]]] = [
        (999, "Todo not found"),
        (0, "Invalid ID"),
        (-1, "Negative ID not allowed"),
    ]

    @pytest.mark.parametrize("todo_id,error_message", delete_todo_error_data)
    def test_delete_todo_error_cases(
        self, mocker: MockerFixture, todo_id: int, error_message: str
    ) -> None:
        """delete_todo()の異常ケースをテスト"""
        # モックを作成
        mock_repository = mocker.Mock()

        # モックのside_effectを設定
        mock_repository.delete_todo.side_effect = ValueError(error_message)

        # モックを使用してUsecaseを作成
        usecase = TodoUsecase(mock_repository)

        # メソッドを実行
        with pytest.raises(ValueError, match=error_message):
            usecase.delete_todo(todo_id)

        # モックの呼び出しを検証
        mock_repository.delete_todo.assert_called_once_with(todo_id)

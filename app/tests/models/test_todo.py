from typing import Any

import pytest
from pydantic import ValidationError

from app.models.todo import Todo, TodoBase, TodoCreate, TodoRead, TodoUpdate

# ruff: noqa: F401
from app.models.user import User


class TestTodoBaseSuccessCases:
    """TodoBaseクラスの正常ケースのテスト"""

    # TodoBase作成時の正常ケース
    @pytest.mark.parametrize(
        "args, expected",
        [
            # 通常
            pytest.param(
                {
                    "title": "test title1",
                    "description": "test description1",
                    "completed": False,
                    "user_id": 1,
                },
                TodoBase(
                    title="test title1",
                    description="test description1",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_base_no_completed",
            ),
            # completedがTrue
            pytest.param(
                {
                    "title": "test title2",
                    "description": "test description2",
                    "completed": True,
                    "user_id": 1,
                },
                TodoBase(
                    title="test title2",
                    description="test description2",
                    completed=True,
                    user_id=1,
                ),
                id="valid_todo_base_completed",
            ),
            # completedがデフォルト値
            pytest.param(
                {
                    "title": "test title3",
                    "description": "test description3",
                    "user_id": 1,
                },
                TodoBase(
                    title="test title3",
                    description="test description3",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_base_default_completed",
            ),
        ],
    )
    def test_valid_todo_base(self, args: dict[str, Any], expected: TodoBase) -> None:
        """有効なTodoBaseの作成をテスト"""
        todo_base = TodoBase(**args)

        assert todo_base == expected


class TestTodoSuccessCases:
    """Todoデータベースモデルの正常ケースのテスト"""

    # Todo作成時の正常ケース
    @pytest.mark.parametrize(
        "args, expected",
        [
            # IDを指定したTodoの作成
            pytest.param(
                {
                    "id": 1,
                    "title": "test title",
                    "description": "test description",
                    "completed": False,
                    "user_id": 1,
                },
                Todo(
                    id=1,
                    title="test title",
                    description="test description",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_with_id",
            ),
            # IDを指定しないTodoの作成
            pytest.param(
                {
                    "title": "test title",
                    "description": "test description",
                    "completed": True,
                    "user_id": 1,
                },
                Todo(
                    id=None,
                    title="test title",
                    description="test description",
                    completed=True,
                    user_id=1,
                ),
                id="valid_todo_without_id",
            ),
            # IDを指定しないTodoの作成（completedがデフォルト値）
            pytest.param(
                {
                    "title": "test title",
                    "description": "test description",
                    "user_id": 1,
                },
                Todo(
                    id=None,
                    title="test title",
                    description="test description",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_without_id_and_completed",
            ),
        ],
    )
    def test_valid_todo(self, args: dict[str, Any], expected: Todo) -> None:
        """有効なTodoの作成をテスト"""
        todo = Todo(**args)

        assert todo == expected


class TestTodoCreateSuccessCases:
    """TodoCreateの正常ケースのテスト"""

    # TodoCreate作成時の正常ケース
    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param(
                {
                    "title": "test title1",
                    "description": "test description1",
                    "completed": False,
                    "user_id": 1,
                },
                TodoCreate(
                    title="test title1",
                    description="test description1",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_create_no_completed",
            ),
            pytest.param(
                {
                    "title": "test title2",
                    "description": "test description2",
                    "completed": True,
                    "user_id": 1,
                },
                TodoCreate(
                    title="test title2",
                    description="test description2",
                    completed=True,
                    user_id=1,
                ),
                id="valid_todo_create_completed",
            ),
            pytest.param(
                {
                    "title": "test title3",
                    "description": "test description3",
                    "user_id": 1,
                },
                TodoCreate(
                    title="test title3",
                    description="test description3",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_create_default_completed",
            ),
        ],
    )
    def test_valid_todo_create(self, args: dict[str, Any], expected: TodoCreate) -> None:
        """有効なTodoCreateの作成をテスト"""
        todo_create = TodoCreate(**args)

        assert todo_create == expected


class TestTodoCreate_ErrorCases:
    """TodoCreateの異常ケースのテスト"""

    # タイトルが必須であることをテスト
    @pytest.mark.parametrize(
        "args, error_message",
        [
            # 空文字列のタイトル
            pytest.param(
                {
                    "title": "",
                    "description": "test description",
                    "completed": False,
                    "user_id": 1,
                },
                "title is required",
                id="empty_string_title",
            ),
            # スペースのみのタイトル
            pytest.param(
                {
                    "title": "   ",
                    "description": "test description",
                    "completed": False,
                    "user_id": 1,
                },
                "title is required",
                id="whitespace_only_title",
            ),
            # 型エラーメッセージを期待（タイトル）
            pytest.param(
                {
                    "title": None,
                    "description": "test description",
                    "completed": False,
                    "user_id": 1,
                },
                "Input should be a valid string",
                id="none_title",
            ),
            # 空文字列の説明
            pytest.param(
                {
                    "title": "test title",
                    "description": "",
                    "completed": False,
                    "user_id": 1,
                },
                "description is required",
                id="empty_description",
            ),
            # スペースのみの説明
            pytest.param(
                {
                    "title": "test title",
                    "description": "   ",
                    "completed": False,
                    "user_id": 1,
                },
                "description is required",
                id="whitespace_only_description",
            ),
            # 型エラーメッセージを期待（説明）
            pytest.param(
                {
                    "title": "test title",
                    "description": None,
                    "completed": False,
                    "user_id": 1,
                },
                "Input should be a valid string",
                id="none_description",
            ),
        ],
    )
    def test_title_validation(
        self,
        args: dict[str, Any],
        error_message: str,
    ) -> None:
        """
        必須項目が空にならないことをテスト

        空文字列、スペースのみのタイトル・説明は無効です。
        """
        with pytest.raises(ValidationError, match=error_message):
            TodoCreate(**args)


class TestTodoReadSuccessCases:
    """TodoReadの正常ケースのテスト"""

    # TodoRead作成時の正常ケース
    @pytest.mark.parametrize(
        "args, expected",
        [
            # completedがFalseのTodoReadの作成
            pytest.param(
                {
                    "id": 1,
                    "title": "test title",
                    "description": "test description",
                    "completed": False,
                    "user_id": 1,
                },
                TodoRead(
                    id=1,
                    title="test title",
                    description="test description",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_read_no_completed",
            ),
            # completedがTrueのTodoReadの作成
            pytest.param(
                {
                    "id": 1,
                    "title": "test title",
                    "description": "test description",
                    "completed": True,
                    "user_id": 1,
                },
                TodoRead(
                    id=1,
                    title="test title",
                    description="test description",
                    completed=True,
                    user_id=1,
                ),
                id="valid_todo_read_completed",
            ),
            # completedがデフォルト値のTodoReadの作成
            pytest.param(
                {
                    "id": 1,
                    "title": "test title",
                    "description": "test description",
                    "user_id": 1,
                },
                TodoRead(
                    id=1,
                    title="test title",
                    description="test description",
                    completed=False,
                    user_id=1,
                ),
                id="valid_todo_read_default_completed",
            ),
        ],
    )
    def test_valid_todo_read(self, args: dict[str, Any], expected: TodoRead) -> None:
        """有効なTodoReadの作成をテスト"""
        todo_read = TodoRead(**args)

        assert todo_read == expected


class TestTodoUpdateSuccessCases:
    """TodoUpdateの正常ケースのテスト"""

    # TodoUpdate作成時の正常ケース
    @pytest.mark.parametrize(
        "args, expected",
        [
            # タイトルのみの更新
            pytest.param(
                {
                    "title": "updated title",
                    "user_id": 1,
                },
                TodoUpdate(title="updated title", user_id=1),
                id="valid_todo_update_title_only",
            ),
            # 説明のみの更新
            pytest.param(
                {
                    "description": "updated description",
                    "user_id": 1,
                },
                TodoUpdate(description="updated description", user_id=1),
                id="valid_todo_update_description_only",
            ),
            # 完了状態のみの更新
            pytest.param(
                {
                    "completed": True,
                    "user_id": 1,
                },
                TodoUpdate(completed=True, user_id=1),
                id="valid_todo_update_completed",
            ),
            # 全フィールドの更新
            pytest.param(
                {
                    "title": "updated title",
                    "description": "updated description",
                    "completed": True,
                    "user_id": 1,
                },
                TodoUpdate(
                    title="updated title",
                    description="updated description",
                    completed=True,
                    user_id=1,
                ),
                id="valid_todo_update_all_fields",
            ),
            # 更新対象なし
            pytest.param(
                {
                    "user_id": 1,
                },
                TodoUpdate(user_id=1),
                id="valid_todo_update_no_fields",
            ),
        ],
    )
    def test_valid_todo_update(self, args: dict[str, Any], expected: TodoUpdate) -> None:
        """有効なTodoUpdateの作成をテスト"""
        todo_update = TodoUpdate(**args)

        assert todo_update == expected


class TestTodoUpdateErrorCases:
    """TodoUpdateの異常ケースのテスト"""

    # 必須項目が空にならないことをテスト
    @pytest.mark.parametrize(
        "args, expected",
        [
            # 空文字列のテスト
            pytest.param(
                {"title": ""},
                "title is required",
                id="empty_string_title",
            ),
            pytest.param(
                {"title": "  "},
                "title is required",
                id="whitespace_only_title",
            ),
            pytest.param(
                {"description": ""},
                "description is required",
                id="empty_string_description",
            ),
            pytest.param(
                {"description": "  "},
                "description is required",
                id="whitespace_only_description",
            ),
            # 明示的なNone値のテスト
            pytest.param(
                {"title": None},
                "title cannot be null",
                id="explicit_none_title",
            ),
            pytest.param(
                {"description": None},
                "description cannot be null",
                id="explicit_none_description",
            ),
        ],
    )
    def test_validation_errors(self, args: dict[str, Any], expected: str) -> None:
        """
        バリデーションエラーのテスト

        空文字列、スペースのみ、明示的なNone値は無効です。
        """
        with pytest.raises(ValidationError, match=expected):
            TodoUpdate(**args)

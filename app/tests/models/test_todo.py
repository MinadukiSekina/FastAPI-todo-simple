import pytest
from pydantic import ValidationError

from app.models.todo import TodoCreate


class TestTodoCreateSuccessCases:
    """TodoCreateの正常ケースのテスト"""

    # TodoCreate作成時の正常ケース
    @pytest.mark.parametrize(
        "title, description, completed",
        [
            pytest.param(
                "test title1",
                "test description1",
                False,
                id="valid_todo_create_no_completed",
            ),
            pytest.param(
                "test title2",
                "test description2",
                True,
                id="valid_todo_create_completed",
            ),
        ],
    )
    def test_valid_todo_create(self, title: str, description: str, completed: bool) -> None:
        """有効なTodoCreateの作成をテスト"""
        # 正常なデータ
        todo_create = TodoCreate(title=title, description=description, completed=completed)

        assert todo_create.title == title
        assert todo_create.description == description
        assert todo_create.completed is completed

    # TodoCreate作成時のcompletedのデフォルト値をテスト
    def test_default_completed_value(self) -> None:
        """completedのデフォルト値をテスト"""
        todo_create = TodoCreate(title="test title", description="test description")

        assert todo_create.completed is False


class TestTodoCreate_ErrorCases:
    """TodoCreateの異常ケースのテスト"""

    # タイトルが必須であることをテスト
    @pytest.mark.parametrize(
        "title, description, completed, error_message",
        [
            pytest.param("", "test", False, "Title is required", id="empty_title"),
            pytest.param("   ", "test", False, "Title is required", id="whitespace_only_title"),
            # 型エラーメッセージを期待
            pytest.param(None, "test", False, "Input should be a valid string", id="none_title"),
        ],
    )
    def test_title_validation(
        self,
        title: str,
        description: str,
        completed: bool,
        error_message: str,
    ) -> None:
        """
        タイトルが必須であることをテスト

        空文字列、スペースのみのタイトルは無効です。
        """
        # 空文字列のタイトル
        with pytest.raises(ValidationError, match=error_message):
            TodoCreate(title=title, description=description, completed=completed)

    # 説明が必須であることをテスト
    @pytest.mark.parametrize(
        "title, description, completed, error_message",
        [
            pytest.param("test", "", False, "description is required", id="empty_description"),
            pytest.param(
                "test", "   ", False, "description is required", id="whitespace_only_description"
            ),
            pytest.param(
                "test", None, False, "Input should be a valid string", id="none_description"
            ),
        ],
    )
    def test_description_validation(
        self,
        title: str,
        description: str,
        completed: bool,
        error_message: str,
    ) -> None:
        """
        説明が必須であることをテスト

        空文字列、スペースのみの説明は無効です。
        """
        with pytest.raises(ValidationError, match=error_message):
            TodoCreate(title=title, description=description, completed=completed)

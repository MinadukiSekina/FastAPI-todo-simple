"""
Todoアプリケーションのデータモデル定義

このモジュールはSQLModelを使用してTodoアイテムのデータベースモデルと
API用のPydanticモデルを定義します。
"""

from typing import TYPE_CHECKING

from pydantic import ValidationInfo, field_validator
from sqlmodel import Field, Relationship, SQLModel

# 循環参照エラー回避
if TYPE_CHECKING:
    from app.models.user import User


class TodoBase(SQLModel):
    """
    Todoアイテムの基本データ構造

    全てのTodoモデルで共通して使用される、基本的なフィールドを定義します。
    """

    title: str  # Todoアイテムのタイトル
    description: str  # Todoアイテムの詳細説明
    completed: bool = False  # 完了状態（デフォルト: False）
    user_id: int = Field(foreign_key="user.id")


class Todo(TodoBase, table=True):
    """
    データベーステーブル用のTodoモデル

    実際のデータベーステーブルとして使用されるモデルです。
    SQLModelの`table=True`によってテーブルとして認識されます。
    """

    id: int | None = Field(default=None, primary_key=True)  # 主キー（自動採番）
    user: "User" = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    """
    Todo作成時のリクエストモデル

    新しいTodoアイテムを作成する際のAPIリクエストで使用されます。
    idフィールドは含まれません（自動採番のため）。
    """

    @field_validator("title", "description")
    @classmethod
    def validate_title(cls, v: str, info: ValidationInfo) -> str:
        """タイトルが空文字列でないことを検証する"""
        if not v or v.strip() == "":
            raise ValueError(f"{info.field_name} is required")
        return v


class TodoRead(TodoBase):
    """
    Todo読み取り用のレスポンスモデル

    APIレスポンスでTodoアイテムを返す際に使用されます。
    idフィールドが含まれます。
    """

    id: int  # Todoアイテムの一意識別子


class TodoUpdate(TodoBase):
    """
    Todo更新時のリクエストモデル

    既存のTodoアイテムを更新する際のAPIリクエストで使用されます。
    """

    title: str | None = None  # 更新するタイトル
    description: str | None = None  # 更新する説明
    completed: bool | None = None  # 更新する完了状態

    @field_validator("title", "description")
    @classmethod
    def validate_string_field(cls, v: str | None, info: ValidationInfo) -> str | None:
        """タイトルと説明のバリデーション"""
        # 明示的にNoneが送信された場合はエラー
        if v is None:
            raise ValueError(f"{info.field_name} cannot be null")
        # 空文字列や空白のみの場合もエラー
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} is required")
        return v

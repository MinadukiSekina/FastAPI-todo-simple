"""
Todoアプリケーションのデータモデル定義（ユーザー）

このモジュールはSQLModelを使用してユーザーのデータベースモデルと
API用のPydanticモデルを定義します。
"""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

# 循環参照エラー回避
# https://sqlmodel.dokyumento.jp/tutorial/code-structure/#circular-imports-and-type-annotations
if TYPE_CHECKING:
    from app.models.todo import Todo


class UserBase(SQLModel):
    """
    ユーザーの基本データ構造

    全てのユーザーモデルで共通して使用される、基本的なフィールドを定義します。
    """

    username: str
    email: str | None = None
    disabled: bool = False  # デフォルトで有効


class User(UserBase, table=True):
    """ユーザーのデータベースモデル"""

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    todos: list["Todo"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """ユーザー作成時のリクエストモデル"""

    password: str


class UserRead(UserBase):
    """ユーザー読み取り用のレスポンスモデル"""

    id: int


class UserReadWithPassword(UserBase):
    """ユーザー読み取り用のレスポンスモデル（パスワードを含む）"""

    id: int
    hashed_password: str


class UserUpdate(UserBase):
    """ユーザー更新時のリクエストモデル"""

    username: str | None = None
    email: str | None = None
    disabled: bool | None = None

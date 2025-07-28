"""
Todoアプリケーションのデータモデル定義（ユーザー）

このモジュールはSQLModelを使用してユーザーのデータベースモデルと
API用のPydanticモデルを定義します。
"""

from sqlmodel import Field, SQLModel


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

"""
ユーザーリポジトリ

このモジュールはユーザーのデータベース操作を担当します。
SQLModelを使用してユーザーのCRUD操作を提供します。
"""

from typing import Any

from fastapi import Depends
from sqlmodel import Session, select

from app.infrastructure.db import get_session
from app.models.user import User, UserRead, UserReadWithPassword


class UserRepository:
    """ユーザーのデータベース操作を担当するリポジトリクラス。

    このクラスは、ユーザーに関するデータベース操作を担当します。
    Clean Architectureのリポジトリ層として機能し、
    SQLModelを使用してデータベースアクセスを抽象化します。

    Attributes:
        session (Session): SQLModelのセッション

    Examples:
        FastAPIでの使用例:
        >>> from fastapi import Depends
        >>> from app.repositories.user_repository import UserRepository
        >>>
        >>> def get_users(repo: UserRepository = Depends()):
        ...     return repo.get_users()
    """

    def __init__(self, session: Session = Depends(get_session)) -> None:
        """UserRepositoryを初期化します。

        Args:
            session (Session): SQLModelのセッション
        """
        self.session = session

    """ 一時的にコメントアウト
    def get_users(self) -> list[UserRead]:
        \"""全てのユーザーを取得する。

        Returns:
            list[User]: 全てのユーザーを含むリスト
        \"""
        users = self.session.exec(select(User)).all()
        return [UserRead.model_validate(user) for user in users]

    def get_user(self, user_id: int) -> UserRead:
        \"""指定されたIDのユーザーを取得する。

        Args:
            user_id (int): 取得するユーザーのID

        Returns:
            User: 指定されたユーザー

        Raises:
            ValueError: 指定されたIDのユーザーが見つからない場合
        \"""
        user = self.session.get(User, user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        return UserRead.model_validate(user)

    def get_user_by_username(self, username: str) -> UserRead | None:
        \"""指定されたユーザー名のユーザーを取得する。

        Args:
            username (str): 取得するユーザーのユーザー名

        Returns:
            UserRead: 指定されたユーザー、見つからない場合はエラーを返す
        \"""
        statement = select(User).where(User.username == username)
        user = self.session.exec(statement).first()
        if user is None:
            raise ValueError(f"User with username {username} not found")
        return UserRead.model_validate(user)
    """

    def get_user_by_username_with_password(self, username: str) -> UserReadWithPassword:
        """指定されたユーザー名のユーザーを取得する。（パスワードを含む）

        Args:
            username (str): 取得するユーザーのユーザー名

        Returns:
            UserReadWithPassword: 指定されたユーザー、見つからない場合はエラーを返す
        """
        statement = select(User).where(User.username == username)
        user = self.session.exec(statement).first()
        if user is None:
            raise ValueError(f"User with username {username} not found")
        return UserReadWithPassword.model_validate(user)

    def create_user(self, user_data: dict[str, Any]) -> UserRead:
        """新しいユーザーを作成する。

        Args:
            user_data (dict[str, Any]): 作成するユーザーのデータ

        Returns:
            User: 作成されたユーザー
        """
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return UserRead.model_validate(user)

    """ 一時的にコメントアウト
    def update_user(self, user_id: int, user_data: dict[str, Any]) -> UserRead:
        \"""指定されたIDのユーザーを更新する。

        Args:
            user_id (int): 更新するユーザーのID
            user_data (dict[str, Any]): 更新するユーザーのデータ

        Returns:
            User: 更新されたユーザー

        Raises:
            ValueError: 指定されたIDのユーザーが見つからない場合
        \"""
        user = self.get_user(user_id)
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return UserRead.model_validate(user)

    def delete_user(self, user_id: int) -> bool:
        \"""指定されたIDのユーザーを削除する。

        Args:
            user_id (int): 削除するユーザーのID

        Returns:
            bool: 削除が成功した場合True

        Raises:
            ValueError: 指定されたIDのユーザーが見つからない場合
        \"""
        user = self.get_user(user_id)
        self.session.delete(user)
        self.session.commit()
        return True
    """

"""
認証のユースケース

このモジュールは認証に関するビジネスロジックを担当します。
ユーザー認証、トークン生成、ユーザー検証などの機能を提供します。
"""

from fastapi import Depends, HTTPException, status

from app.infrastructure.auth import (
    create_access_token,
    decode_access_token,
    get_token_expires_delta,
    verify_password,
)
from app.models.token import Token
from app.models.user import UserReadWithPassword
from app.repositories.user_repository import UserRepository


class AuthUsecase:
    """認証操作のためのユースケースクラス。

    このクラスは、認証に関連するビジネスロジックを担当します。
    Clean Architectureのユースケース層として機能し、
    FastAPIの依存性注入システムを通じて提供されます。

    UserRepositoryを通じてデータベース操作を行い、
    認証に関するビジネスロジックを適用します。

    Attributes:
        user_repository (UserRepository): Userのデータベース操作を担当するリポジトリ

    Examples:
        FastAPIルーターでの使用例:
        >>> from fastapi import Depends
        >>> from app.usecases.auth_usecase import AuthUsecase
        >>>
        >>> @router.post("/token")
        >>> def login(usecase: AuthUsecase = Depends()):
        ...     return usecase.authenticate_user(username, password)
    """

    def __init__(self, user_repository: UserRepository = Depends(UserRepository)) -> None:
        """AuthUsecaseを初期化します。

        Args:
            user_repository (UserRepository): Userのデータベース操作を担当するリポジトリ
        """
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str) -> UserReadWithPassword | None:
        """ユーザーを認証する。

        指定されたユーザー名とパスワードでユーザーを認証します。

        Args:
            username (str): ユーザー名
            password (str): パスワード

        Returns:
            User | None: 認証が成功した場合Userオブジェクト、失敗した場合None
        """
        try:
            user = self.user_repository.get_user_by_username_with_password(username)
            if not user:
                return None
            if not verify_password(password, user.hashed_password):
                return None
            return user
        except Exception:
            return None

    def create_access_token_for_user(self, user: UserReadWithPassword) -> Token:
        """ユーザーのアクセストークンを作成する。

        Args:
            user (User): トークンを作成するユーザー

        Returns:
            Token: 作成されたアクセストークン
        """
        access_token_expires = get_token_expires_delta()
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    def get_current_user_from_token(self, token: str) -> UserReadWithPassword:
        """トークンから現在のユーザーを取得する。

        Args:
            token (str): JWTトークン

        Returns:
            User: 現在のユーザー

        Raises:
            HTTPException: トークンが無効な場合
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = self.user_repository.get_user_by_username_with_password(username)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(self, user: UserReadWithPassword) -> UserReadWithPassword:
        """現在のアクティブユーザーを取得する。

        Args:
            user (User): 検証するユーザー

        Returns:
            User: アクティブなユーザー

        Raises:
            HTTPException: ユーザーが無効な場合
        """
        if user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

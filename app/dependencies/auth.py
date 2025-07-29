"""
認証の依存性注入

このモジュールはFastAPIの依存性注入システムで使用される
認証関連の関数を提供します。
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.user import UserRead, UserReadWithPassword
from app.usecases.auth_usecase import AuthUsecase

# OAuth2スキームの設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ruff: noqa: RUF029
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_usecase: AuthUsecase = Depends(),
) -> UserReadWithPassword:
    """現在のユーザーを取得する。

    JWTトークンから現在のユーザーを取得します。
    FastAPIの依存性注入システムで使用されます。

    Args:
        token (str): JWTトークン
        auth_usecase (AuthUsecase): 認証ユースケース

    Returns:
        User: 現在のユーザー

    Raises:
        HTTPException: トークンが無効な場合
    """
    return auth_usecase.get_current_user_from_token(token)


async def get_current_active_user(
    current_user: Annotated[UserReadWithPassword, Depends(get_current_user)],
    auth_usecase: AuthUsecase = Depends(),
) -> UserReadWithPassword:
    """現在のアクティブユーザーを取得する。

    現在のユーザーがアクティブかどうかを確認します。
    FastAPIの依存性注入システムで使用されます。

    Args:
        current_user (User): 現在のユーザー
        auth_usecase (AuthUsecase): 認証ユースケース

    Returns:
        User: アクティブなユーザー

    Raises:
        HTTPException: ユーザーが無効な場合
    """
    return auth_usecase.get_current_active_user(current_user)


async def get_current_active_user_read(
    current_user: Annotated[UserReadWithPassword, Depends(get_current_active_user)],
) -> UserRead:
    """現在のアクティブユーザーを読み取り用モデルで取得する。

    Args:
        current_user (User): 現在のアクティブユーザー

    Returns:
        UserRead: 読み取り用のユーザーモデル
    """
    return UserRead.model_validate(current_user)

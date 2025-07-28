"""
認証ルーター

このモジュールは認証関連のAPIエンドポイントを提供します。
ログイン、ユーザー登録、ユーザー情報取得などの機能を含みます。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import get_current_active_user_read
from app.models.token import Token
from app.models.user import UserRead
from app.usecases.auth_usecase import AuthUsecase

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_usecase: Annotated[AuthUsecase, Depends()],
) -> Token:
    """アクセストークンを取得する。

    ユーザー名とパスワードで認証し、JWTアクセストークンを返します。

    Args:
        form_data (OAuth2PasswordRequestForm): ログインフォームデータ
        auth_usecase (AuthUsecase): 認証ユースケース

    Returns:
        Token: アクセストークン

    Raises:
        HTTPException: 認証に失敗した場合
    """
    user = auth_usecase.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_usecase.create_access_token_for_user(user)


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_active_user_read)],
) -> UserRead:
    """現在のユーザー情報を取得する。

    Args:
        current_user (UserRead): 現在のアクティブユーザー

    Returns:
        UserRead: 現在のユーザー情報
    """
    return current_user

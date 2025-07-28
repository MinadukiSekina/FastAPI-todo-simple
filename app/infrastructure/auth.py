"""
認証の基盤機能

このモジュールは認証に関する基盤的な機能を提供します。
パスワードのハッシュ化、JWTトークンの処理、ユーザー検証などが含まれます。
"""

from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import jwt
from passlib.context import CryptContext

# JWT設定
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワードハッシュ化の設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証する。

    Args:
        plain_password (str): 平文のパスワード
        hashed_password (str): ハッシュ化されたパスワード

    Returns:
        bool: パスワードが一致する場合True
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化する。

    Args:
        password (str): ハッシュ化するパスワード

    Returns:
        str: ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """アクセストークンを作成する。

    Args:
        data (dict[str, Any]): トークンに含めるデータ
        expires_delta (timedelta | None, optional): 有効期限。デフォルトは15分

    Returns:
        str: エンコードされたJWTトークン
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(ZoneInfo("UTC")) + expires_delta
    else:
        expire = datetime.now(ZoneInfo("UTC")) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """アクセストークンをデコードする。

    Args:
        token (str): デコードするJWTトークン

    Returns:
        dict[str, Any]: デコードされたトークンデータ

    Raises:
        InvalidTokenError: トークンが無効な場合
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_token_expires_delta() -> timedelta:
    """トークンの有効期限を取得する。

    Returns:
        timedelta: トークンの有効期限
    """
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

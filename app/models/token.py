from pydantic import BaseModel


class Token(BaseModel):
    """認証トークンのレスポンスモデル"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """トークンデータのモデル"""

    username: str | None = None

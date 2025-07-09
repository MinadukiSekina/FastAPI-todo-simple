import os
from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import Engine
from sqlmodel import Session, create_engine


@lru_cache
def get_database_engine() -> Engine:
    """データベースエンジンを取得する（キャッシュあり）。

    環境変数からデータベース接続情報を取得し、SQLAlchemyエンジンを作成します。
    @lru_cacheデコレータにより、一度作成されたエンジンは再利用されます。

    Returns:
        Engine: SQLAlchemyのエンジンインスタンス

    Raises:
        KeyError: 必要な環境変数が設定されていない場合
        ValueError: データベース接続文字列の構築に失敗した場合
    """
    try:
        postgres_user = os.environ["POSTGRES_USER"]
        postgres_password = os.environ["POSTGRES_PASSWORD"]
        postgres_server = os.environ["POSTGRES_SERVER"]
        postgres_port = os.environ["POSTGRES_PORT"]
        postgres_db = os.environ["POSTGRES_DB"]
    except KeyError as e:
        raise KeyError(f"Required environment variable not set: {e}") from e

    if not all([postgres_user, postgres_password, postgres_server, postgres_port, postgres_db]):
        raise ValueError("One or more database environment variables are empty")

    database_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_server}:{postgres_port}/{postgres_db}"
    return create_engine(database_url)


def get_session() -> Generator[Session, None, None]:
    """データベースセッションを提供する。

    FastAPIの依存性注入システムで使用されるジェネレータ関数です。
    with文とyieldを組み合わせることで、セッションの自動クローズを保証します。

    Yields:
        Session: SQLModelのセッションインスタンス

    Examples:
        FastAPIでの使用例:
        >>> from fastapi import Depends
        >>> def get_todos(session: Session = Depends(get_session)):
        ...     return session.exec(select(Todo)).all()

    Notes:
        - セッションは自動的にクローズされるため、手動でclose()を呼ぶ必要はありません
        - エラーが発生した場合も、with文によりセッションは適切にクローズされます
    """
    engine = get_database_engine()
    with Session(engine) as session:
        yield session

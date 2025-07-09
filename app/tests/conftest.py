import os
from collections.abc import Generator
from typing import Any

import pytest
from pytest_postgresql import factories
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.models.todo import Todo

# 環境変数を取得
postgres_user = os.environ["POSTGRES_USER"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_server = os.environ["POSTGRES_SERVER"]
postgres_port = os.environ["POSTGRES_PORT"]
postgres_db = os.environ["POSTGRES_DB"]

# ライブラリを使ってテスト用のDBをセットアップするためのfixtureを作成
# 既定ではdbname=testでDBが作成されテストケースの実行毎にDBは削除され１から再作成される
postgresql_noproc = factories.postgresql_noproc(
    user=postgres_user,
    password=postgres_password,
    host=postgres_server,
    port=postgres_port,
)
postgresql_fixture = factories.postgresql(
    "postgresql_noproc",
)


@pytest.fixture
def get_test_engine(postgresql_fixture: Any) -> Engine:
    """テスト用のEngineを取得するFixture"""
    # 接続URIを作成
    uri = (
        f"postgresql://"
        f"{postgresql_fixture.info.user}:{postgresql_fixture.info.password}@{postgresql_fixture.info.host}:{postgresql_fixture.info.port}"
        f"/{postgresql_fixture.info.dbname}"
    )
    return create_engine(uri)


@pytest.fixture
def get_test_session(get_test_engine: Engine) -> Generator[Session, None, None]:
    """テスト用のSessionを取得するFixture"""
    # テーブルを作成する
    SQLModel.metadata.create_all(get_test_engine)

    with Session(get_test_engine) as session:
        yield session


@pytest.fixture
def create_test_todo_data(get_test_session: Session, request: pytest.FixtureRequest) -> list[Todo]:
    """テスト用のTodoデータを作成するFixture"""
    todos = [Todo.model_validate(t) for t in request.param]
    for todo in todos:
        get_test_session.add(todo)
        get_test_session.commit()
        get_test_session.refresh(todo)

    return todos

import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlmodel import Session

from app.infrastructure.db import get_database_engine, get_session


# Todo: claudeが生成したコードなので、概要を把握する
class TestGetDatabaseEngine:
    """get_database_engine()関数のテスト"""

    def setup_method(self) -> None:
        """各テストメソッド実行前にキャッシュをクリア"""
        get_database_engine.cache_clear()

    def teardown_method(self) -> None:
        """各テストメソッド実行後にキャッシュをクリア"""
        get_database_engine.cache_clear()

    def test_success_case(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """正常ケース: 有効な環境変数でエンジンが作成される"""
        # 環境変数をセット
        env_vars = {
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
            "POSTGRES_SERVER": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "test_db",
        }
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # エンジンを取得
        engine = get_database_engine()

        # 検証
        assert isinstance(engine, Engine)
        # SQLAlchemyはセキュリティのためパスワードを***でマスクするため、それを考慮してチェック
        engine_url_str = str(engine.url)
        assert "postgresql://test_user:" in engine_url_str
        assert "@localhost:5432/test_db" in engine_url_str

    @pytest.mark.parametrize(
        "missing_var",
        [
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_SERVER",
            "POSTGRES_PORT",
            "POSTGRES_DB",
        ],
    )
    def test_missing_environment_variable(
        self, monkeypatch: pytest.MonkeyPatch, missing_var: str
    ) -> None:
        """KeyError: 必要な環境変数が不足している場合"""
        # 必要な環境変数をセット（欠落する変数以外）
        env_vars = {
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
            "POSTGRES_SERVER": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "test_db",
        }
        # 指定された変数を削除
        del env_vars[missing_var]

        # 環境変数をセット
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # 欠落した変数を環境から削除
        monkeypatch.delenv(missing_var, raising=False)

        # エラーが発生することを検証
        with pytest.raises(KeyError) as exc_info:
            get_database_engine()

        assert f"Required environment variable not set: '{missing_var}'" in str(exc_info.value)

    @pytest.mark.parametrize(
        "empty_var, empty_value",
        [
            ("POSTGRES_USER", ""),
            ("POSTGRES_PASSWORD", ""),
            ("POSTGRES_SERVER", ""),
            ("POSTGRES_PORT", ""),
            ("POSTGRES_DB", ""),
        ],
    )
    def test_empty_environment_variable(
        self, monkeypatch: pytest.MonkeyPatch, empty_var: str, empty_value: str
    ) -> None:
        """ValueError: 環境変数が空文字列の場合"""
        # 環境変数をセット（1つだけ空文字列）
        env_vars = {
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
            "POSTGRES_SERVER": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "test_db",
        }
        env_vars[empty_var] = empty_value

        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # エラーが発生することを検証
        with pytest.raises(ValueError) as exc_info:
            get_database_engine()

        assert "One or more database environment variables are empty" in str(exc_info.value)

    def test_cache_behavior(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """@lru_cache: 同じエンジンが再利用されること"""
        # 環境変数をセット
        env_vars = {
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
            "POSTGRES_SERVER": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "test_db",
        }
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # 2回呼び出し
        engine1 = get_database_engine()
        engine2 = get_database_engine()

        # 同じインスタンスが返されることを検証
        assert engine1 is engine2

        # キャッシュ情報を確認
        cache_info = get_database_engine.cache_info()
        assert cache_info.hits == 1
        assert cache_info.misses == 1


class TestGetSession:
    """get_session()関数のテスト"""

    def test_session_yields_and_closes(self, mocker: MockerFixture) -> None:
        """セッションが適切にyieldされ、自動的にクローズされること"""
        # モックエンジンを作成
        mock_engine = mocker.Mock(spec=Engine)
        mock_get_database_engine = mocker.patch("app.infrastructure.db.get_database_engine")
        mock_get_database_engine.return_value = mock_engine

        # モックセッションを作成
        mock_session = mocker.Mock(spec=Session)

        # Session()コンストラクタをモック化
        mock_session_class = mocker.patch("app.infrastructure.db.Session")
        # contextmanagerとしてのモックセッションを設定
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = None

        # ジェネレータからセッションを取得
        session_generator = get_session()
        session = next(session_generator)

        # セッションが正しく返されることを検証
        assert session is mock_session

        # Session()が正しいエンジンで呼ばれることを検証
        mock_session_class.assert_called_once_with(mock_engine)

        # ジェネレータを終了（with文の終了をシミュレート）
        try:
            next(session_generator)
        except StopIteration:
            pass

        # __enter__と__exit__が呼ばれることを検証（with文の動作）
        mock_session_class.return_value.__enter__.assert_called_once()
        mock_session_class.return_value.__exit__.assert_called_once()

    def test_session_cleanup_on_exception(self, mocker: MockerFixture) -> None:
        """例外が発生してもセッションが適切にクローズされること"""
        # モックエンジンを作成
        mock_engine = mocker.Mock(spec=Engine)
        mock_get_database_engine = mocker.patch("app.infrastructure.db.get_database_engine")
        mock_get_database_engine.return_value = mock_engine

        # Session()コンストラクタをモック化
        mock_session_class = mocker.patch("app.infrastructure.db.Session")
        # contextmanagerとしてのモックセッションを設定
        mock_session_class.return_value.__enter__.return_value = mocker.Mock(spec=Session)
        mock_session_class.return_value.__exit__.return_value = None

        # ジェネレータを開始
        session_generator = get_session()
        session = next(session_generator)

        # セッションが返されることを確認
        assert session is not None

        # 例外を投げてジェネレータを終了
        try:
            session_generator.throw(Exception("Test exception"))
        except Exception:
            pass

        # __exit__が例外時でも呼ばれることを検証
        mock_session_class.return_value.__exit__.assert_called_once()

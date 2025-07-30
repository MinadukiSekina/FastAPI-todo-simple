from fastapi import Depends

from app.infrastructure.auth import get_password_hash
from app.models.user import UserCreate, UserRead
from app.repositories.user_repository import UserRepository


class UserUsecase:
    """User操作のためのユースケースクラス。

    このクラスは、Userに関連するビジネスロジックを担当します。
    Clean Architectureのユースケース層として機能し、
    FastAPIの依存性注入システムを通じて提供されます。

    UserRepositoryを通じてデータベース操作を行い、
    必要に応じてビジネスロジックを適用します。

    Attributes:
        user_repository (UserRepository): Userのデータベース操作を担当するリポジトリ

    Examples:
        FastAPIルーターでの使用例:
        >>> from fastapi import Depends
        >>> from app.usecases.userUsecase import get_userUsecase, UserUsecase
        >>>
        >>> @router.get("/users")
        >>> def get_all_users(usecase: UserUsecase = Depends(get_userUsecase)):
        ...     return usecase.get_todos()

    Notes:
        - このクラスは依存性注入パターンで使用されます
        - UserRepositoryを通じてデータベース操作を実行します
        - 各メソッドは適切なエラーハンドリングとバリデーションを含みます
    """

    def __init__(self, user_repository: UserRepository = Depends(UserRepository)) -> None:
        """UserUsecaseを初期化します。

        Args:
            user_repository (UserRepository): Userのデータベース操作を担当するリポジトリ
        """
        self.user_repository = user_repository

    """ 一時的にコメントアウト
    def get_users(self) -> list[UserRead]:
        \"""全てのUserを取得する。

        データベースから全てのUserを取得し、
        表示用のモデルとして返します。

        Returns:
            list[UserRead]: 全てのUserを含むリスト。

        Raises:
            データベースアクセスエラーなどの例外が発生する可能性があります。
        \"""
        users = self.user_repository.get_users()
        return [UserRead.model_validate(user) for user in users]

    def get_user(self, user_id: int) -> UserRead:
        \"""指定されたIDのUserを取得する。

        データベースから指定されたIDのUserを取得し、
        表示用のモデルとして返します。

        Args:
            user_id (int): 取得するUserのID。

        Returns:
            UserRead: 指定されたUser。

        Raises:
            ValueError: 指定されたIDのUserが見つからない場合
            データベースアクセスエラーなどの例外が発生する可能性があります。
        \"""
        user = self.user_repository.get_user(user_id)
        return UserRead.model_validate(user)
    """

    def create_user(self, user_create: UserCreate) -> UserRead:
        """新しいUserを作成する。

        入力された情報を基に新しいUserを作成し、
        データベースに保存します。パスワードは自動的にハッシュ化されます。

        Args:
            user_create (UserCreate): 作成するUserの情報。

        Returns:
            UserRead: 作成されたUser。

        Raises:
            データベースアクセスエラーなどの例外が発生する可能性があります。
        """
        # パスワードをハッシュ化
        hashed_password = get_password_hash(user_create.password)

        # ユーザー作成用のデータを準備
        user_data = user_create.model_dump(exclude={"password"})
        user_data["hashed_password"] = hashed_password

        user = self.user_repository.create_user(user_data)
        return UserRead.model_validate(user)

    """ 一時的にコメントアウト
    def update_user(self, user_id: int, user_update: UserBase) -> UserRead:
        \"""指定されたIDのUserを更新する。

        指定されたIDのUserを更新し、
        データベースに変更を保存します。

        Args:
            user_id (int): 更新するUserのID。
            user_update (UserBase): 更新するUserの内容。

        Returns:
            UserRead: 更新されたUser。

        Raises:
            ValueError: 指定されたIDのUserが見つからない場合
            データベースアクセスエラーなどの例外が発生する可能性があります。
        \"""
        user_data = user_update.model_dump()
        user = self.user_repository.update_user(user_id, user_data)
        return UserRead.model_validate(user)

    def delete_user(self, user_id: int) -> bool:
        \"""指定されたIDのUserを削除する。

        指定されたIDのTodoアイテムをデータベースから削除します。

        Args:
            user_id (int): 削除するUserのID。

        Returns:
            bool: 削除が成功した場合True

        Raises:
            ValueError: 指定されたIDのUserが見つからない場合
            データベースアクセスエラーなどの例外が発生する可能性があります。
        \"""
        return self.user_repository.delete_user(user_id)
    """

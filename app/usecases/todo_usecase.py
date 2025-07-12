from fastapi import Depends

from app.models.todo import TodoCreate, TodoRead, TodoUpdate
from app.repositories.todo_repository import TodoRepository


class TodoUsecase:
    """Todo操作のためのユースケースクラス。

    このクラスは、Todoに関連するビジネスロジックを担当します。
    Clean Architectureのユースケース層として機能し、
    FastAPIの依存性注入システムを通じて提供されます。

    TodoRepositoryを通じてデータベース操作を行い、
    必要に応じてビジネスロジックを適用します。

    Attributes:
        todo_repository (TodoRepository): Todoのデータベース操作を担当するリポジトリ

    Examples:
        FastAPIルーターでの使用例:
        >>> from fastapi import Depends
        >>> from app.usecases.todoUsecase import get_todoUsecase, TodoUsecase
        >>>
        >>> @router.get("/todos")
        >>> def get_all_todos(usecase: TodoUsecase = Depends(get_todoUsecase)):
        ...     return usecase.get_todos()

    Notes:
        - このクラスは依存性注入パターンで使用されます
        - TodoRepositoryを通じてデータベース操作を実行します
        - 各メソッドは適切なエラーハンドリングとバリデーションを含みます
    """

    def __init__(self, todo_repository: TodoRepository = Depends(TodoRepository)) -> None:
        """TodoUsecaseを初期化します。

        Args:
            todo_repository (TodoRepository): Todoのデータベース操作を担当するリポジトリ
        """
        self.todo_repository = todo_repository

    def get_todos(self) -> list[TodoRead]:
        """全てのTodoを取得する。

        データベースから全てのTodoアイテムを取得し、
        表示用のモデルとして返します。

        Returns:
            list[TodoRead]: 全てのTodoを含むリスト。

        Raises:
            データベースアクセスエラーなどの例外が発生する可能性があります。
        """
        return self.todo_repository.get_all_todos()

    def get_todo(self, todo_id: int) -> TodoRead:
        """指定されたIDのTodoを取得する。

        データベースから指定されたIDのTodoアイテムを取得し、
        表示用のモデルとして返します。

        Args:
            todo_id (int): 取得するTodoのID。

        Returns:
            TodoRead: 指定されたTodoアイテム。

        Raises:
            ValueError: 指定されたIDのTodoが見つからない場合
            データベースアクセスエラーなどの例外が発生する可能性があります。
        """
        return self.todo_repository.get_todo(todo_id)

    def create_todo(self, todo_create: TodoCreate) -> TodoRead:
        """新しいTodoを作成する。

        入力された情報を基に新しいTodoアイテムを作成し、
        データベースに保存します。

        Args:
            todo_create (TodoCreate): 作成するTodoの情報。

        Returns:
            TodoRead: 作成されたTodoアイテム。

        Raises:
            データベースアクセスエラーなどの例外が発生する可能性があります。
        """
        return self.todo_repository.create_todo(todo_create)

    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> TodoRead:
        """指定されたIDのTodoを更新する。

        指定されたIDのTodoアイテムを更新し、
        データベースに変更を保存します。

        Args:
            todo_id (int): 更新するTodoのID。
            todo_update (TodoUpdate): 更新するTodoの内容。

        Returns:
            TodoRead: 更新されたTodoアイテム。

        Raises:
            ValueError: 指定されたIDのTodoが見つからない場合
            データベースアクセスエラーなどの例外が発生する可能性があります。
        """
        return self.todo_repository.update_todo(todo_id, todo_update)

    def delete_todo(self, todo_id: int) -> bool:
        """指定されたIDのTodoを削除する。

        指定されたIDのTodoアイテムをデータベースから削除します。

        Args:
            todo_id (int): 削除するTodoのID。

        Returns:
            bool: 削除が成功した場合True

        Raises:
            ValueError: 指定されたIDのTodoが見つからない場合
            データベースアクセスエラーなどの例外が発生する可能性があります。
        """
        return self.todo_repository.delete_todo(todo_id)

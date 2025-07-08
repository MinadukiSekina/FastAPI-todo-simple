from fastapi import Depends

from app.models.todo import TodoCreate, TodoRead, TodoUpdate
from app.repositories.todoRepository import TodoRepository, get_todo_repository


class TodoUsecase:
    """Todo操作のためのユースケースクラス。

    このクラスは、Todoに関連するビジネスロジックを担当します。
    Clean Architectureのユースケース層として機能し、
    FastAPIの依存性注入システムを通じて提供されます。

    現在の実装は基本的なCRUD操作のスケルトンを提供し、
    実際のデータベース操作や複雑なビジネスロジックは
    今後の実装で追加される予定です。

    Attributes:
        なし（現在の実装では状態を持たない）

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
        - 現在はモックデータを返しますが、将来的にはデータベース操作を含む実装に拡張されます
        - 各メソッドは適切なエラーハンドリングとバリデーションを含む必要があります
    """

    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    def get_todos(self) -> list[TodoRead]:
        """全てのTodoを取得する。

        Returns:
            list[TodoRead]: 全てのTodoを含むリスト。

        Raises:
            将来的には適切な例外を発生させる予定。
        """
        return self.todo_repository.get_all_todos()

    def get_todo(self, todo_id: int) -> TodoRead:
        """指定されたIDのTodoを取得する。

        Args:
            todo_id (int): 取得するTodoのID。

        Returns:
            dict: 指定されたTodoを含む辞書。
                現在の実装では {"message": f"Get a todo {todo_id}"} を返す。

        Raises:
            将来的には適切な例外を発生させる予定（例：TodoNotFound）。
        """
        return self.todo_repository.get_todo(todo_id)

    def create_todo(self, todo_create: TodoCreate) -> TodoRead:
        """新しいTodoを作成する。

        Returns:
            dict: 作成結果を含む辞書。
                現在の実装では {"message": "Create a todo"} を返す。

        Raises:
            将来的には適切な例外を発生させる予定。
        """
        return self.todo_repository.create_todo(todo_create)

    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> TodoRead:
        """指定されたIDのTodoを更新する。

        Args:
            todo_id (int): 更新するTodoのID。
            todo_update (TodoUpdate): 更新するTodoの内容。

        Returns:
            dict: 更新結果を含む辞書。
                現在の実装では {"message": f"Update a todo {todo_id}"} を返す。

        Raises:
            将来的には適切な例外を発生させる予定（例：TodoNotFound）。
        """
        return self.todo_repository.update_todo(todo_id, todo_update)

    def delete_todo(self, todo_id: int) -> None:
        """指定されたIDのTodoを削除する。

        Args:
            todo_id (int): 削除するTodoのID。

        Returns:
            dict: 削除結果を含む辞書。
                現在の実装では {"message": f"Delete a todo {todo_id}"} を返す。

        Raises:
            将来的には適切な例外を発生させる予定（例：TodoNotFound）。
        """
        return self.todo_repository.delete_todo(todo_id)


def get_todoUsecase(todo_repository: TodoRepository = Depends(get_todo_repository)) -> TodoUsecase:
    """TodoUsecaseのインスタンスを取得する。

    FastAPIの依存性注入システムで使用されるファクトリー関数です。
    現在の実装では新しいインスタンスを毎回作成しますが、
    将来的にはシングルトンパターンや他の依存性注入パターンを
    実装する可能性があります。

    Returns:
        TodoUsecase: TodoUsecaseのインスタンス。

    Examples:
        FastAPIルーターでの使用例:
        >>> from fastapi import Depends
        >>>
        >>> @router.get("/todos")
        >>> def get_all_todos(usecase: TodoUsecase = Depends(get_todoUsecase)):
        ...     return usecase.get_todos()
    """
    return TodoUsecase(todo_repository)

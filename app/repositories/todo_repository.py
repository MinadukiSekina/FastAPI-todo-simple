from fastapi import Depends
from sqlmodel import Session, select

from app.infrastructure.db import get_session
from app.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate


class TodoRepository:
    """
    Todoアイテムのデータベース操作を担当するリポジトリクラス

    このクラスはTodoアイテムのCRUD操作（作成、読み取り、更新、削除）を提供します。
    """

    def __init__(self, session: Session = Depends(get_session)) -> None:
        """
        TodoRepositoryを初期化します

        Args:
            session: データベースセッション
        """
        self.session = session

    def get_all_todos(self, user_id: int) -> list[TodoRead]:
        """
        すべてのTodoアイテムを取得します

        Returns:
            list[TodoRead]: すべてのTodoアイテムのリスト
        """
        todos = self.session.exec(select(Todo).where(Todo.user_id == user_id)).all()
        return [TodoRead.model_validate(todo) for todo in todos]

    def create_todo(self, todo: TodoCreate) -> TodoRead:
        """
        新しいTodoアイテムを作成します

        Args:
            todo: 作成するTodoアイテムの情報

        Returns:
            TodoRead: 作成されたTodoアイテム
        """
        # 保存用のモデルを作成
        new_todo = Todo.model_validate(todo)

        # データベースに保存
        self.session.add(new_todo)
        self.session.commit()
        self.session.refresh(new_todo)

        # 保存後のデータで表示用のモデルを返却
        return TodoRead.model_validate(new_todo)

    def _get_todo_by_id(self, todo_id: int, user_id: int) -> Todo:
        """
        指定されたIDのTodoアイテムを取得します

        Args:
            todo_id: 取得するTodoアイテムのID
            user_id: ユーザーのID

        Returns:
            Todo: 指定されたTodoアイテム

        Raises:
            ValueError: 指定されたIDのTodoアイテムが見つからない場合
        """
        todo = self.session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        ).first()
        if not todo:
            raise ValueError(f"Todo with id {todo_id} not found")
        return todo

    def get_todo(self, todo_id: int, user_id: int) -> TodoRead:
        """
        指定されたIDのTodoアイテムを取得します

        Args:
            todo_id: 取得するTodoアイテムのID
            user_id: ユーザーのID

        Returns:
            TodoRead: 指定されたTodoアイテム

        Raises:
            ValueError: 指定されたIDのTodoアイテムが見つからない場合
        """
        todo = self._get_todo_by_id(todo_id, user_id)
        return TodoRead.model_validate(todo)

    def update_todo(self, todo_id: int, todo: TodoUpdate, user_id: int) -> TodoRead:
        """
        指定されたIDのTodoアイテムを更新します

        Args:
            todo_id: 更新するTodoアイテムのID
            todo: 更新する内容
            user_id: ユーザーID

        Returns:
            TodoRead: 更新されたTodoアイテム

        Raises:
            ValueError: 指定されたIDのTodoアイテムが見つからない場合
        """
        # 対象データの取得
        target = self._get_todo_by_id(todo_id, user_id)

        # 更新するデータの取得
        update_data = todo.model_dump(exclude_unset=True)

        # 更新するデータを適用
        target.sqlmodel_update(update_data)

        # データベースに保存
        self.session.add(target)
        self.session.commit()
        self.session.refresh(target)

        # 更新後のデータで表示用のモデルを返却
        return TodoRead.model_validate(target)

    def delete_todo(self, todo_id: int, user_id: int) -> bool:
        """
        指定されたIDのTodoアイテムを削除します

        Args:
            todo_id: 削除するTodoアイテムのID
            user_id: ユーザーID

        Returns:
            bool: 削除が成功した場合True

        Raises:
            ValueError: 指定されたIDのTodoアイテムが見つからない場合
        """
        # 対象データの取得
        todo = self._get_todo_by_id(todo_id, user_id)

        # データベースから削除
        self.session.delete(todo)
        self.session.commit()

        return True

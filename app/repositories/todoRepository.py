from fastapi import Depends
from sqlmodel import Session, select

from app.infrastructure.db import get_session
from app.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate


class TodoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_todos(self) -> list[TodoRead]:
        todos = self.session.exec(select(Todo)).all()
        return [TodoRead.model_validate(todo) for todo in todos]

    def create_todo(self, todo: TodoCreate) -> TodoRead:
        new_todo = Todo.model_validate(todo)
        self.session.add(new_todo)
        self.session.commit()
        self.session.refresh(new_todo)
        return TodoRead.model_validate(new_todo)

    def get_todo(self, todo_id: int) -> TodoRead:
        todo = self.session.get(Todo, todo_id)
        return TodoRead.model_validate(todo)

    def update_todo(self, todo_id: int, todo: TodoUpdate) -> TodoRead:
        target = self.session.get(Todo, todo_id)
        if not target:
            raise ValueError(f"Todo with id {todo_id} not found")
        update_data = todo.model_dump(exclude_unset=True)
        target.sqlmodel_update(update_data)
        self.session.add(target)
        self.session.commit()
        self.session.refresh(target)
        return TodoRead.model_validate(target)

    def delete_todo(self, todo_id: int) -> None:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            raise ValueError(f"Todo with id {todo_id} not found")
        self.session.delete(todo)
        self.session.commit()


def get_todo_repository(session: Session = Depends(get_session)) -> TodoRepository:
    return TodoRepository(session)

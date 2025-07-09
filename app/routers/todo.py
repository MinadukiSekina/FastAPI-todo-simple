from fastapi import APIRouter, Depends

from app.models.todo import TodoCreate, TodoRead, TodoUpdate
from app.usecases.todoUsecase import TodoUsecase

router = APIRouter(prefix="/todos", tags=["todos"])


# ruff: noqa
@router.get("/", response_model=list[TodoRead])
def get_todos(todo_usecase: TodoUsecase = Depends()) -> list[TodoRead]:
    return todo_usecase.get_todos()


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int, todo_usecase: TodoUsecase = Depends()) -> TodoRead:
    return todo_usecase.get_todo(todo_id)


@router.post("/", response_model=TodoRead)
def create_todo(todo_create: TodoCreate, todo_usecase: TodoUsecase = Depends()) -> TodoRead:
    return todo_usecase.create_todo(todo_create)


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int, todo_update: TodoUpdate, todo_usecase: TodoUsecase = Depends()
) -> TodoRead:
    return todo_usecase.update_todo(todo_id, todo_update)


@router.delete("/{todo_id}", response_model=None)
def delete_todo(todo_id: int, todo_usecase: TodoUsecase = Depends()) -> None:
    return todo_usecase.delete_todo(todo_id)

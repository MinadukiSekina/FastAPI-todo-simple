from fastapi import APIRouter, Depends
from app.usecases.todoUsecase import get_todoUsecase, TodoUsecase

router = APIRouter(prefix="/todos", tags=["todos"])


# ruff: noqa
@router.get("/")
def get_todos(todo_usecase: TodoUsecase = Depends(get_todoUsecase)) -> dict:
    return todo_usecase.get_todos()


@router.get("/{todo_id}")
def get_todo(todo_id: int, todo_usecase: TodoUsecase = Depends(get_todoUsecase)) -> dict:
    return todo_usecase.get_todo(todo_id)


@router.post("/")
def create_todo(todo_usecase: TodoUsecase = Depends(get_todoUsecase)) -> dict:
    return todo_usecase.create_todo()


@router.put("/{todo_id}")
def update_todo(todo_id: int, todo_usecase: TodoUsecase = Depends(get_todoUsecase)) -> dict:
    return todo_usecase.update_todo(todo_id)


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, todo_usecase: TodoUsecase = Depends(get_todoUsecase)) -> dict:
    return todo_usecase.delete_todo(todo_id)

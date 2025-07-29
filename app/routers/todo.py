from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from app.dependencies.auth import get_current_active_user_read
from app.models.todo import TodoCreate, TodoRead, TodoUpdate
from app.models.user import UserRead
from app.usecases.todo_usecase import TodoUsecase

router = APIRouter(prefix="/todos", tags=["todos"])


# ruff: noqa
@router.get("/", response_model=list[TodoRead])
def get_todos(
    todo_usecase: Annotated[TodoUsecase, Depends()],
    current_user: Annotated[UserRead, Depends(get_current_active_user_read)],
) -> list[TodoRead]:
    return todo_usecase.get_todos(current_user.id)


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int,
    todo_usecase: Annotated[TodoUsecase, Depends()],
    current_user: Annotated[UserRead, Depends(get_current_active_user_read)],
) -> TodoRead:
    try:
        return todo_usecase.get_todo(todo_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=TodoRead)
def create_todo(
    todo_create: TodoCreate,
    todo_usecase: Annotated[TodoUsecase, Depends()],
    current_user: Annotated[UserRead, Depends(get_current_active_user_read)],
) -> TodoRead:
    try:
        return todo_usecase.create_todo(todo_create)
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="Failed to create todo due to data constraint violation"
        )


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    todo_usecase: Annotated[TodoUsecase, Depends()],
    current_user: Annotated[UserRead, Depends(get_current_active_user_read)],
) -> TodoRead:
    try:
        return todo_usecase.update_todo(todo_id, todo_update, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="Failed to update todo due to data constraint violation"
        )


@router.delete("/{todo_id}", response_model=bool)
def delete_todo(
    todo_id: int,
    todo_usecase: Annotated[TodoUsecase, Depends()],
    current_user: Annotated[UserRead, Depends(get_current_active_user_read)],
) -> bool:
    try:
        return todo_usecase.delete_todo(todo_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

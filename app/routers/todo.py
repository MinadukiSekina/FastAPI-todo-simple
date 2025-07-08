from fastapi import APIRouter

router = APIRouter(prefix="/todos", tags=["todos"])


# ruff: noqa
@router.get("/")
def get_todos():
    return {"message": "Get all todos"}


@router.get("/{todo_id}")
def get_todo(todo_id: int):
    return {"message": "Get a todo"}


@router.post("/")
def create_todo():
    return {"message": "Create a todo"}


@router.put("/{todo_id}")
def update_todo(todo_id: int):
    return {"message": "Update a todo"}


@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    return {"message": "Delete a todo"}

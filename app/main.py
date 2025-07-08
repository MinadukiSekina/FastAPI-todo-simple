from fastapi import FastAPI
from app.routers import todo

app = FastAPI()

app.include_router(todo.router)


# ruff: noqa
@app.get("/")
def read_root():
    return {"message": "Hello World"}

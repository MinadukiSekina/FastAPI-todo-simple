"""
FastAPIアプリケーションのメインモジュール

このモジュールはFastAPIアプリケーションのエントリーポイントです。
各ルーターを統合し、アプリケーションの設定を行います。
"""

from fastapi import FastAPI

from app.routers import todo, auth, user

app = FastAPI(
    title="Todo API",
    description="Clean Architectureを使用したTodoアプリケーションのAPI",
    version="1.0.0",
)

# ルーターの登録
app.include_router(todo.router)
app.include_router(auth.router)
app.include_router(user.router)


# ruff: noqa
@app.get("/")
def read_root():
    return {"message": "Hello World"}

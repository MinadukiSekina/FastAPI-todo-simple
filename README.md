# FastApiによるTodoアプリ

## 起動方法

### 開発サーバーの起動
```bash
uv run fastapi dev app/main.py
```

### 本番サーバーの起動
```bash
uv run fastapi run app/main.py
```

## エンドポイント

- **ベースURL**: http://127.0.0.1:8000
- **APIドキュメント**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 利用可能なAPIエンドポイント

- `GET /`: Hello Worldメッセージを返す


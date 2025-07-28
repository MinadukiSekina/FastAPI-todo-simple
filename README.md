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
- `GET /todos`: すべてのTodoを取得
- `GET /todos/{todo_id}`: 指定されたIDのTodoを取得
- `POST /todos`: 新しいTodoを作成
- `PUT /todos/{todo_id}`: 指定されたIDのTodoを更新
- `DELETE /todos/{todo_id}`: 指定されたIDのTodoを削除

## アーキテクチャ

本プロジェクトはクリーンアーキテクチャパターンを採用しています。各レイヤーは単一の責務を持ち、依存関係が一方向になるよう設計されています。

### レイヤー構成

1. **プレゼンテーション層** (`routers/`)
   - FastAPIルーターによるHTTPエンドポイント
   - HTTPリクエスト/レスポンスの処理

2. **アプリケーション層** (`usecases/`)
   - ビジネスロジックの実装
   - ユースケースの実行

3. **リポジトリ層** (`repositories/`)
   - データアクセスの抽象化
   - データベース操作の実装

4. **インフラストラクチャ層** (`infrastructure/`)
   - データベース接続の管理
   - 外部サービスとの統合

5. **ドメインモデル層** (`models/`)
   - ビジネスドメインの概念をモデル化
   - データの構造と制約を定義

## クラス間の依存関係図

```mermaid
classDiagram
    class TodoRouter {
        +get_todos()
        +get_todo(todo_id)
        +create_todo(todo_create)
        +update_todo(todo_id, todo_update)
        +delete_todo(todo_id)
    }
    
    class TodoUsecase {
        -todo_repository: TodoRepository
        +get_todos()
        +get_todo(todo_id)
        +create_todo(todo_create)
        +update_todo(todo_id, todo_update)
        +delete_todo(todo_id)
    }
    
    class TodoRepository {
        -session: Session
        +get_all_todos()
        +get_todo(todo_id)
        +create_todo(todo)
        +update_todo(todo_id, todo)
        +delete_todo(todo_id)
        -_get_todo_by_id(todo_id)
    }
    
    class TodoBase {
        +title: str
        +description: str
        +completed: bool
    }
    
    class Todo {
        +id: int
        +title: str
        +description: str
        +completed: bool
    }
    
    class TodoCreate {
        +title: str
        +description: str
        +completed: bool
        +validate_title()
    }
    
    class TodoRead {
        +id: int
        +title: str
        +description: str
        +completed: bool
    }
    
    class TodoUpdate {
        +title: str
        +description: str
        +completed: bool
        +validate_string_field()
    }
    
    class DatabaseSession {
        +get_session()
        +get_database_engine()
    }
    
    %% 依存関係
    TodoRouter --> TodoUsecase : "depends on"
    TodoUsecase --> TodoRepository : "depends on"
    TodoRepository --> DatabaseSession : "depends on"
    
    %% モデル継承
    Todo --|> TodoBase : "inherits"
    TodoCreate --|> TodoBase : "inherits"
    TodoRead --|> TodoBase : "inherits"
    TodoUpdate --|> TodoBase : "inherits"
    
    %% モデル使用関係
    TodoRouter ..> TodoCreate : "uses"
    TodoRouter ..> TodoRead : "uses"
    TodoRouter ..> TodoUpdate : "uses"
    
    TodoUsecase ..> TodoCreate : "uses"
    TodoUsecase ..> TodoRead : "uses"
    TodoUsecase ..> TodoUpdate : "uses"
    
    TodoRepository ..> Todo : "uses"
    TodoRepository ..> TodoCreate : "uses"
    TodoRepository ..> TodoRead : "uses"
    TodoRepository ..> TodoUpdate : "uses"
    
    %% アーキテクチャ層の分類
    class ArchitectureLayer {
        <<interface>>
    }
    
    note for TodoRouter "プレゼンテーション層<br/>APIエンドポイント"
    note for TodoUsecase "アプリケーション層<br/>ビジネスロジック"
    note for TodoRepository "リポジトリ層<br/>データアクセス"
    note for DatabaseSession "インフラストラクチャ層<br/>データベース接続"
    note for TodoBase "ドメインモデル層<br/>データ構造定義"
```

### 設計の特徴

- **依存関係の逆転**: 各層は抽象化に依存し、具象に依存しない設計
- **関心の分離**: 各レイヤーが単一の責務を持つ
- **テスタビリティ**: 依存性注入により、単体テストが容易
- **保守性**: 各レイヤーの変更が他のレイヤーに影響しにくい構造


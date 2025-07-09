import pytest
from sqlmodel import Session

from app.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from app.repositories.todoRepository import TodoRepository

# =============================================================================
# get_all_todos()の正常ケースのテスト
# =============================================================================

# get_all_todos()の正常ケースのテスト用データ
get_all_todos_success_data: list[tuple[list[TodoCreate], list[TodoRead]]] = [
    # 登録が0件
    (
        [],
        [],
    ),
    # 登録が1件
    (
        [TodoCreate(title="test", description="test", completed=False)],
        [TodoRead(id=1, title="test", description="test", completed=False)],
    ),
    # 登録が複数件
    (
        [
            TodoCreate(title="test", description="test", completed=False),
            TodoCreate(title="test2", description="test2", completed=False),
            TodoCreate(title="test3", description="test3", completed=True),
        ],
        [
            TodoRead(id=1, title="test", description="test", completed=False),
            TodoRead(id=2, title="test2", description="test2", completed=False),
            TodoRead(id=3, title="test3", description="test3", completed=True),
        ],
    ),
]


@pytest.mark.parametrize(
    "create_test_todo_data, expected_todos",
    get_all_todos_success_data,
    indirect=["create_test_todo_data"],
)
def test_get_all_todos_success_cases(
    get_test_session: Session,
    create_test_todo_data: list[Todo],
    expected_todos: list[TodoRead],
) -> None:
    """get_all_todos()をテスト"""
    # リポジトリを作成
    repository = TodoRepository(get_test_session)

    # メソッドを実行
    todos = repository.get_all_todos()

    # 結果を検証
    assert todos == expected_todos


# =============================================================================
# create_todo()の正常ケースのテスト
# =============================================================================

# create_todo()の正常ケースのテスト用データ
create_todo_success_data: list[tuple[TodoCreate, TodoRead]] = [
    (
        TodoCreate(title="test", description="test", completed=False),
        TodoRead(id=1, title="test", description="test", completed=False),
    ),
]


@pytest.mark.parametrize(
    "todo_create, expected_todo",
    create_todo_success_data,
)
def test_create_todo_success_cases(
    get_test_session: Session,
    todo_create: TodoCreate,
    expected_todo: TodoRead,
) -> None:
    """create_todo()をテスト"""
    # リポジトリを作成
    repository = TodoRepository(get_test_session)

    # メソッドを実行
    todo = repository.create_todo(todo_create)

    # 結果を検証
    assert todo == expected_todo


# =============================================================================
# get_todo()の正常ケースのテスト
# =============================================================================

# get_todo()の正常ケースのテスト用データ
get_todo_success_data: list[tuple[int, list[TodoCreate], TodoRead]] = [
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoRead(id=1, title="test", description="test", completed=False),
    ),
    (
        2,
        [
            TodoCreate(title="test", description="test", completed=False),
            TodoCreate(title="test2", description="test2", completed=False),
        ],
        TodoRead(id=2, title="test2", description="test2", completed=False),
    ),
]


@pytest.mark.parametrize(
    "todo_id, create_test_todo_data, expected_todo",
    get_todo_success_data,
    indirect=["create_test_todo_data"],
)
def test_get_todo_success_cases(
    get_test_session: Session,
    todo_id: int,
    create_test_todo_data: list[Todo],
    expected_todo: TodoRead,
) -> None:
    """get_todo()をテスト"""
    # リポジトリを作成
    repository = TodoRepository(get_test_session)

    # メソッドを実行
    todo = repository.get_todo(todo_id)

    # 結果を検証
    assert todo == expected_todo


# =============================================================================
# update_todo()の正常ケースのテスト
# =============================================================================

# update_todo()の正常ケースのテスト用データ
update_todo_success_data: list[tuple[int, list[TodoCreate], TodoUpdate, TodoRead]] = [
    # タイトルのみ更新
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoUpdate(title="updated"),
        TodoRead(id=1, title="updated", description="test", completed=False),
    ),
    # 説明のみ更新
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoUpdate(description="updated"),
        TodoRead(id=1, title="test", description="updated", completed=False),
    ),
    # 完了状態のみ更新
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoUpdate(completed=True),
        TodoRead(id=1, title="test", description="test", completed=True),
    ),
    # タイトルと完了状態のみ更新
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoUpdate(title="updated", completed=True),
        TodoRead(id=1, title="updated", description="test", completed=True),
    ),
    # タイトルと説明のみ更新
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoUpdate(title="updated", description="updated"),
        TodoRead(id=1, title="updated", description="updated", completed=False),
    ),
    # 説明と完了状態のみ更新
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoUpdate(description="updated", completed=True),
        TodoRead(id=1, title="test", description="updated", completed=True),
    ),
    # すべて更新
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        TodoUpdate(title="updated", description="updated", completed=True),
        TodoRead(id=1, title="updated", description="updated", completed=True),
    ),
    # 複数件ある内の１つの更新
    (
        2,
        [
            TodoCreate(title="test", description="test", completed=False),
            TodoCreate(title="test2", description="test2", completed=False),
        ],
        TodoUpdate(completed=True),
        TodoRead(id=2, title="test2", description="test2", completed=True),
    ),
]


@pytest.mark.parametrize(
    "todo_id, create_test_todo_data, todo_update, expected_todo",
    update_todo_success_data,
    indirect=["create_test_todo_data"],
)
def test_update_todo_success_cases(
    get_test_session: Session,
    todo_id: int,
    create_test_todo_data: list[Todo],
    todo_update: TodoUpdate,
    expected_todo: TodoRead,
) -> None:
    """update_todo()をテスト"""
    # リポジトリを作成
    repository = TodoRepository(get_test_session)

    # メソッドを実行
    todo = repository.update_todo(todo_id, todo_update)

    # 結果を検証
    assert todo == expected_todo


# =============================================================================
# delete_todo()の正常ケースのテスト
# =============================================================================

# delete_todo()の正常ケースのテスト用データ
delete_todo_success_data: list[tuple[int, list[TodoCreate], None]] = [
    (
        1,
        [TodoCreate(title="test", description="test", completed=False)],
        None,
    ),
    (
        2,
        [
            TodoCreate(title="test", description="test", completed=False),
            TodoCreate(title="test2", description="test2", completed=False),
        ],
        None,
    ),
]


@pytest.mark.parametrize(
    "todo_id, create_test_todo_data, expected_todo",
    delete_todo_success_data,
    indirect=["create_test_todo_data"],
)
def test_delete_todo_success_cases(
    get_test_session: Session,
    todo_id: int,
    create_test_todo_data: list[Todo],
    expected_todo: None,
) -> None:
    """delete_todo()をテスト"""
    # リポジトリを作成
    repository = TodoRepository(get_test_session)

    # メソッドを実行
    repository.delete_todo(todo_id)

    # 結果を検証
    with pytest.raises(ValueError):
        repository.get_todo(todo_id)

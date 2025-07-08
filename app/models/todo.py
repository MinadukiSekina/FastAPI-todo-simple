from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    title: str
    description: str
    completed: bool = False


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int


class TodoUpdate(TodoBase):
    title: str
    description: str
    completed: bool = False

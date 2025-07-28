"""
ユーザー管理ルーター

このモジュールはユーザー管理に関するAPIエンドポイントを提供します。
ユーザーのCRUD操作を含みます。
"""

from fastapi import APIRouter, Depends

from app.models.user import UserBase, UserRead
from app.usecases.user_usecase import UserUsecase

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def get_users(
    user_usecase: UserUsecase = Depends(),
) -> list[UserRead]:
    """全てのユーザーを取得する。

    Args:
        user_usecase (UserUsecase): ユーザー管理ユースケース

    Returns:
        list[UserRead]: 全てのユーザーのリスト
    """
    return user_usecase.get_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_usecase: UserUsecase = Depends(),
) -> UserRead:
    """指定されたIDのユーザーを取得する。

    Args:
        user_id (int): 取得するユーザーのID
        user_usecase (UserUsecase): ユーザー管理ユースケース

    Returns:
        UserRead: 指定されたユーザー

    Raises:
        HTTPException: ユーザーが見つからない場合
    """
    return user_usecase.get_user(user_id)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserBase,
    user_usecase: UserUsecase = Depends(),
) -> UserRead:
    """指定されたIDのユーザーを更新する。

    Args:
        user_id (int): 更新するユーザーのID
        user_update (UserBase): 更新するユーザーの情報
        user_usecase (UserUsecase): ユーザー管理ユースケース

    Returns:
        UserRead: 更新されたユーザー

    Raises:
        HTTPException: ユーザーが見つからない場合
    """
    return user_usecase.update_user(user_id, user_update)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user_usecase: UserUsecase = Depends(),
) -> dict[str, str]:
    """指定されたIDのユーザーを削除する。

    Args:
        user_id (int): 削除するユーザーのID
        user_usecase (UserUsecase): ユーザー管理ユースケース

    Returns:
        dict[str, str]: 削除結果のメッセージ

    Raises:
        HTTPException: ユーザーが見つからない場合
    """
    user_usecase.delete_user(user_id)
    return {"message": f"User {user_id} deleted successfully"}

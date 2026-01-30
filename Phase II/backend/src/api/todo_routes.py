from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from src.database import get_session
from src.models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from src.services.todo_service import (
    create_todo_for_user,
    get_todos_by_user,
    get_todo_by_id_and_user,
    update_todo_by_user,
    delete_todo_by_user,
    toggle_todo_completion_status
)
from src.api.deps import get_current_user
from src.models.user import User

router = APIRouter()


@router.get("/", response_model=List[TodoRead])
def read_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve all todos for the authenticated user.
    """
    todos = get_todos_by_user(user_id=current_user.id, session=session)
    return todos


@router.post("/", response_model=TodoRead)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the authenticated user.
    """
    db_todo = create_todo_for_user(
        todo=todo,
        user_id=current_user.id,
        session=session
    )
    return db_todo


@router.get("/{todo_id}", response_model=TodoRead)
def read_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific todo for the authenticated user.
    """
    db_todo = get_todo_by_id_and_user(
        todo_id=todo_id,
        user_id=current_user.id,
        session=session
    )

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return db_todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing todo for the authenticated user.
    """
    # Convert TodoUpdate to dictionary, excluding unset fields
    update_data = todo_update.dict(exclude_unset=True)

    # Create TodoUpdate instance with the validated data
    validated_update = TodoUpdate(**update_data)

    db_todo = update_todo_by_user(
        todo_id=todo_id,
        user_id=current_user.id,
        todo_update=validated_update,
        session=session
    )

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return db_todo


@router.patch("/{todo_id}/complete")
def toggle_complete(
    todo_id: int,
    completed: bool,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a todo for the authenticated user.
    """
    db_todo = toggle_todo_completion_status(
        todo_id=todo_id,
        user_id=current_user.id,
        completed=completed,
        session=session
    )

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return db_todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo for the authenticated user.
    """
    success = delete_todo_by_user(
        todo_id=todo_id,
        user_id=current_user.id,
        session=session
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {"message": "Todo deleted successfully"}
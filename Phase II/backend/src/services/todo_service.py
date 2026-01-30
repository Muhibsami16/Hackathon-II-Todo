from sqlmodel import Session, select
from typing import List, Optional
from src.models.todo import Todo, TodoCreate, TodoUpdate
from src.models.user import User


def create_todo_for_user(*, todo: TodoCreate, user_id: int, session: Session) -> Todo:
    """
    Create a new todo for a specific user.

    Args:
        todo: TodoCreate object with title, description, and completion status
        user_id: ID of the user who owns the todo
        session: Database session

    Returns:
        Todo: The created todo object
    """
    # Create a new Todo instance using the validated data
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=user_id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def get_todos_by_user(*, user_id: int, session: Session) -> List[Todo]:
    """
    Get all todos for a specific user.

    Args:
        user_id: ID of the user whose todos to retrieve
        session: Database session

    Returns:
        List[Todo]: List of todos owned by the user
    """
    statement = select(Todo).where(Todo.user_id == user_id)
    results = session.exec(statement)
    return results.all()


def get_todo_by_id_and_user(*, todo_id: int, user_id: int, session: Session) -> Optional[Todo]:
    """
    Get a specific todo by its ID and user ID.

    Args:
        todo_id: ID of the todo to retrieve
        user_id: ID of the user who should own the todo
        session: Database session

    Returns:
        Todo: The todo object if found and owned by the user, None otherwise
    """
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = session.exec(statement).first()
    return result


def update_todo_by_user(*, todo_id: int, user_id: int, todo_update: TodoUpdate, session: Session) -> Optional[Todo]:
    """
    Update a todo if it belongs to the specified user.

    Args:
        todo_id: ID of the todo to update
        user_id: ID of the user who owns the todo
        todo_update: TodoUpdate object with fields to update
        session: Database session

    Returns:
        Todo: The updated todo object if found and owned by the user, None otherwise
    """
    db_todo = get_todo_by_id_and_user(todo_id=todo_id, user_id=user_id, session=session)

    if not db_todo:
        return None

    # Update the todo with the provided values
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def delete_todo_by_user(*, todo_id: int, user_id: int, session: Session) -> bool:
    """
    Delete a todo if it belongs to the specified user.

    Args:
        todo_id: ID of the todo to delete
        user_id: ID of the user who owns the todo
        session: Database session

    Returns:
        bool: True if the todo was deleted, False if not found or not owned by user
    """
    db_todo = get_todo_by_id_and_user(todo_id=todo_id, user_id=user_id, session=session)

    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True


def toggle_todo_completion_status(*, todo_id: int, user_id: int, completed: bool, session: Session) -> Optional[Todo]:
    """
    Toggle the completion status of a todo.

    Args:
        todo_id: ID of the todo to update
        user_id: ID of the user who owns the todo
        completed: New completion status
        session: Database session

    Returns:
        Todo: The updated todo object if found and owned by the user, None otherwise
    """
    db_todo = get_todo_by_id_and_user(todo_id=todo_id, user_id=user_id, session=session)

    if not db_todo:
        return None

    db_todo.completed = completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
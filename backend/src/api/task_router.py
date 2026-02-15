import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from typing import Optional
from ..database.connection import get_session
from ..models.task import TaskCreate, TaskUpdate
from ..models.response import TaskResponse, TaskListResponse
from ..services.task_service import TaskService
from ..services.auth_service import AuthService
from ..config import settings


task_router = APIRouter()
auth_scheme = HTTPBearer()
auth_service = AuthService()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_session)
) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        token_type = payload.get("token_type", "access")

        # Only allow access tokens for getting current user, not refresh tokens
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token required for this operation",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Check if token has expired
        import time
        exp = payload.get("exp")
        if exp and exp < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Log the decoded user_email for debugging
        print(f"Decoded user_email from token: {user_email}")
    except JWTError as e:
        print(f"JWT decode error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth_service.get_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str = str(user.id)
    print(f"Fetched user_id from DB: {user_id_str}")
    return user_id_str


@task_router.get("/", response_model=TaskListResponse)
def list_tasks(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session),
    status_filter: Optional[str] = Query(None, description="Filter by status: all, completed, pending"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort: str = Query("created", description="Sort by: created, due_date, priority")
):
    # Get tasks with pagination and sorting
    from ..models.task import Task

    # Log for debugging
    print(f"Fetching tasks for user_id: {current_user_id} (type: {type(current_user_id)})")

    # Convert string user_id to UUID for proper comparison
    try:
        user_uuid = uuid.UUID(current_user_id) if isinstance(current_user_id, str) else current_user_id
        print(f"Converted user_id to UUID: {user_uuid}")
    except ValueError:
        print(f"Invalid user ID format: {current_user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Get tasks for the authenticated user
    tasks = TaskService.get_tasks_by_user(
        db=db,
        user_id=current_user_id,
        skip=offset,
        limit=limit,
        status_filter=status_filter,
        sort_by=sort
    )

    # Calculate total count for the authenticated user - use same user identifier
    total_query = db.query(Task)
    total_query = total_query.filter(Task.user_id == user_uuid)

    if status_filter:
        if status_filter == "completed":
            total_query = total_query.filter(Task.is_completed == True)
        elif status_filter == "pending":
            total_query = total_query.filter(Task.is_completed == False)

    total_count = total_query.count()
    print(f"Found {len(tasks)} tasks for user {current_user_id}, total count: {total_count}")

    # Convert to response format
    task_responses = [
        TaskResponse(
            id=str(task.id),  # Ensure ID is string
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            due_date=task.due_date,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=str(task.user_id)  # Ensure user_id is string
        )
        for task in tasks
    ]

    return TaskListResponse(
        tasks=task_responses,
        total_count=total_count,
        limit=limit,
        offset=offset
    )


@task_router.post("/", response_model=TaskResponse)
def create_task(
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    db_task = TaskService.create_task(db, task_create, current_user_id)

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        is_completed=db_task.is_completed,
        due_date=db_task.due_date,
        priority=db_task.priority,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        user_id=db_task.user_id
    )


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    db_task = TaskService.get_task_by_id(db, task_id, current_user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        is_completed=db_task.is_completed,
        due_date=db_task.due_date,
        priority=db_task.priority,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        user_id=db_task.user_id
    )


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    db_task = TaskService.update_task(db, task_id, task_update, current_user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        is_completed=db_task.is_completed,
        due_date=db_task.due_date,
        priority=db_task.priority,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        user_id=db_task.user_id
    )


@task_router.patch("/{task_id}/complete", response_model=TaskResponse)
def update_task_completion(
    task_id: str,
    is_completed: bool,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    db_task = TaskService.toggle_task_completion(db, task_id, current_user_id, is_completed)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        is_completed=db_task.is_completed,
        due_date=db_task.due_date,
        priority=db_task.priority,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        user_id=db_task.user_id
    )


@task_router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_completion(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    # First get the current task
    db_task = TaskService.get_task_by_id(db, task_id, current_user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status
    new_status = not db_task.is_completed

    # Update the task with the new completion status
    updated_task = TaskService.toggle_task_completion(db, task_id, current_user_id, new_status)

    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        is_completed=updated_task.is_completed,
        due_date=updated_task.due_date,
        priority=updated_task.priority,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at,
        user_id=updated_task.user_id
    )


@task_router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    success = TaskService.delete_task(db, task_id, current_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}


@task_router.delete("/")
def delete_completed_tasks(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    deleted_count = TaskService.delete_completed_tasks(db, current_user_id)
    return {"message": f"{deleted_count} completed tasks deleted successfully"}
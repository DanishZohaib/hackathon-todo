from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from typing import Optional
from ..database.connection import get_db
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
    db: Session = Depends(get_db)
) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
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
    return str(user.id)


@task_router.get("/", response_model=TaskListResponse)
def list_tasks(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query(None, description="Filter by status: all, completed, pending"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort: str = Query("created", description="Sort by: created, due_date, priority")
):
    tasks = TaskService.get_tasks_by_user(
        db=db,
        user_id=current_user_id,
        skip=offset,
        limit=limit,
        status_filter=status_filter
    )

    # Get total count for pagination
    total_count = len(tasks)

    # Convert to response format
    task_responses = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            due_date=task.due_date,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=task.user_id
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
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
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
def toggle_task_completion(
    task_id: str,
    is_completed: bool,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
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


@task_router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    success = TaskService.delete_task(db, task_id, current_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}